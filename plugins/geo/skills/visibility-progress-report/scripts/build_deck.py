#!/usr/bin/env python3
"""
GEO visibility progress 9-slide deck generator (PowerPoint + optional PDF).

Reads a CSV of LLM prompt execution data and produces a 9-slide widescreen deck
that tells the progress story: where the brand stands today, the visibility
trend, where the conversation is concentrated, week-1 vs latest delta per
topic, what content shipped and what it earned, the under-cited verticals as
the next lever, the platform breakdown, and where to focus next.

Usage:
    python build_deck.py <csv_path> <brand_name> <output.pptx> \
        [--brand-domain-keyword keyword] \
        [--published-count N] [--drafts-count N] [--total-article-citations N] \
        [--article-titles-json PATH] \
        --assets-dir PATH

The PDF is generated alongside the .pptx via LibreOffice headless when available.
By default the deck uses the Yolando logo from the styleguide plugin and a dark
background. Pass --assets-dir to override bg.png, bg_cover.png, or logo_light.png.
"""
import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR


# ============ TOKENS ============
INK         = RGBColor(0x16, 0x15, 0x18)
CARD_BG     = RGBColor(0x18, 0x17, 0x1B)
CARD_BG_2   = RGBColor(0x1F, 0x1E, 0x23)
CARD_BORDER = RGBColor(0x2A, 0x29, 0x2D)
WHITE       = RGBColor(0xFA, 0xFA, 0xFA)
FG_2        = RGBColor(0xA3, 0xA3, 0xA6)
FG_3        = RGBColor(0x7E, 0x7E, 0x80)
ACCENT      = RGBColor(0xA7, 0xA6, 0xFE)
ACCENT_DEEP = RGBColor(0x8B, 0x7B, 0xDB)
ACCENT_DARK = RGBColor(0x55, 0x52, 0x9C)
GREEN_BRIGHT= RGBColor(0x4A, 0xE3, 0x7A)
GREEN_BG    = RGBColor(0x1B, 0x2B, 0x1A)
RED         = RGBColor(0xE7, 0x4C, 0x3C)
ORANGE      = RGBColor(0xEA, 0x9E, 0x59)
COMP_BAR    = RGBColor(0x33, 0x32, 0x37)

SLIDE_W = 13.333
SLIDE_H = 7.5

PLATFORM_NAMES = {
    "ANTHROPIC": "Claude",
    "OPEN_AI":   "OpenAI/GPT",
    "GOOGLE":    "Gemini",
    "PERPLEXITY":"Perplexity",
}


# ============ DATA ============
def parse_bool(v):
    return str(v).strip().upper() in ("YES", "TRUE", "1")


def normalize_url(u):
    return u.strip().split("?")[0].split("#")[0].rstrip("/")


def derive_brand_keyword(brand_name, override=None):
    """Return a single lowercase substring used to identify the brand's own
    URLs in the citation list. The default:
    lowercase the brand name and strip spaces. Override via CLI for brands
    where this default is too narrow or too broad (e.g. multi-word brand on
    a short domain)."""
    if override:
        return override.lower().strip()
    return brand_name.lower().strip().replace(" ", "")


def url_belongs_to_brand(url, brand_keyword):
    return brand_keyword in url.lower()


def title_from_url(url, title_map):
    """Look up a title from the map first, fall back to slug-cased URL."""
    canon = url.replace("https://www.", "https://")
    if canon in title_map:
        return title_map[canon]
    if url in title_map:
        return title_map[url]
    slug = canon.rstrip("/").split("/")[-1]
    return slug.replace("-", " ").replace("_", " ").title()


def load_and_analyze(csv_path, brand_name, brand_keyword=None,
                    inventory=None, title_map=None):
    """Read the CSV and compute every metric the deck needs."""
    csv.field_size_limit(10 ** 7)
    keyword = derive_brand_keyword(brand_name, brand_keyword)
    title_map = title_map or {}

    rows = []
    with open(csv_path, encoding="utf-8-sig") as f:
        rdr = csv.DictReader(f)
        for r in rdr:
            rows.append(r)

    daily = defaultdict(lambda: {"total": 0, "mentioned": 0, "blog_cit": 0})
    weekly = defaultdict(lambda: {"total": 0, "mentioned": 0})
    topic_stats = defaultdict(lambda: {"total": 0, "mentioned": 0})
    topic_weekly = defaultdict(lambda: defaultdict(lambda: {"total": 0, "mentioned": 0}))
    platform_stats = defaultdict(lambda: {"total": 0, "mentioned": 0})

    article_citations = Counter()
    article_first_seen = {}
    competitor_counts = Counter()
    total_brand_citations = 0
    total_blog_cited_mentions = 0

    for r in rows:
        d = r.get("Execution Date", "") or r.get("Date", "")
        topic = r.get("Topic", "") or r.get("Category", "")
        plat = r.get("Platform", "")
        try:
            dt = datetime.strptime(d, "%Y-%m-%d")
            wk = (dt - timedelta(days=dt.weekday())).strftime("%Y-%m-%d")
        except Exception:
            continue
        m = parse_bool(r.get("Workspace Brand Mentioned", ""))
        daily[d]["total"] += 1
        weekly[wk]["total"] += 1
        topic_stats[topic]["total"] += 1
        topic_weekly[topic][wk]["total"] += 1
        platform_stats[plat]["total"] += 1
        if m:
            daily[d]["mentioned"] += 1
            weekly[wk]["mentioned"] += 1
            topic_stats[topic]["mentioned"] += 1
            topic_weekly[topic][wk]["mentioned"] += 1
            platform_stats[plat]["mentioned"] += 1
            cits = r.get("Citations (Links)", "") or r.get("Citations", "")
            urls = [normalize_url(u) for u in cits.split("|") if u.strip()]
            had_blog = False
            for u in urls:
                if url_belongs_to_brand(u, keyword):
                    total_brand_citations += 1
                    if "/blog/" in u.lower() or "/articles/" in u.lower():
                        had_blog = True
                        canon = u.lower().replace("https://www.", "https://")
                        article_citations[canon] += 1
                        if canon not in article_first_seen or d < article_first_seen[canon]:
                            article_first_seen[canon] = d
            if had_blog:
                total_blog_cited_mentions += 1
                daily[d]["blog_cit"] += 1
            comps = r.get("Competitor Mentions", "")
            for c in comps.split("|"):
                c = c.strip()
                if c:
                    competitor_counts[c] += 1

    sd = sorted(daily.keys())
    if not sd:
        raise ValueError("No valid date rows found in CSV")
    fw_dates = sd[:7]
    lw_dates = sd[-7:]
    fw_t = sum(daily[d]["total"] for d in fw_dates)
    fw_m = sum(daily[d]["mentioned"] for d in fw_dates)
    lw_t = sum(daily[d]["total"] for d in lw_dates)
    lw_m = sum(daily[d]["mentioned"] for d in lw_dates)
    first_week_rate = fw_m / fw_t * 100 if fw_t else 0
    last_week_rate = lw_m / lw_t * 100 if lw_t else 0

    sorted_weeks = sorted(weekly.keys())
    fw_key = sorted_weeks[0]
    lw_key = sorted_weeks[-1]
    topic_delta = []
    for topic, ws in topic_weekly.items():
        if not topic:
            continue
        fw = ws.get(fw_key, {"total": 0, "mentioned": 0})
        lw = ws.get(lw_key, {"total": 0, "mentioned": 0})
        fw_rate = fw["mentioned"] / fw["total"] * 100 if fw["total"] else 0
        lw_rate = lw["mentioned"] / lw["total"] * 100 if lw["total"] else 0
        cur_rate = topic_stats[topic]["mentioned"] / topic_stats[topic]["total"] * 100 \
            if topic_stats[topic]["total"] else 0
        topic_delta.append({
            "topic": topic,
            "first_rate": fw_rate,
            "last_rate": lw_rate,
            "current_rate": cur_rate,
            "delta": lw_rate - fw_rate,
            "mentioned": topic_stats[topic]["mentioned"],
        })

    # Inventory: fall back to data-derived values when not supplied
    inv = inventory or {}
    distinct_articles_cited = len(article_citations)
    inventory_resolved = {
        "published": inv.get("published", distinct_articles_cited),
        "drafts": inv.get("drafts", 0),
        "total_citations": inv.get("total_citations",
                                   sum(article_citations.values())),
    }

    return {
        "total_executions": len(rows),
        "date_range": (sd[0], sd[-1]),
        "days": len(sd),
        "total_mentions": sum(daily[d]["mentioned"] for d in sd),
        "total_brand_citations": total_brand_citations,
        "total_blog_cited_mentions": total_blog_cited_mentions,
        "first_week_rate": first_week_rate,
        "last_week_rate": last_week_rate,
        "daily": dict(daily),
        "weekly": dict(weekly),
        "topic_stats": dict(topic_stats),
        "topic_delta": topic_delta,
        "platform_stats": dict(platform_stats),
        "article_citations": article_citations,
        "article_first_seen": article_first_seen,
        "competitor_counts": competitor_counts,
        "inventory": inventory_resolved,
        "title_map": title_map,
    }


# ============ CHARTS ============
def make_chart_visibility_trend(metrics, tmpdir):
    daily = metrics["daily"]
    sd = sorted(daily.keys())
    dts = [datetime.strptime(d, "%Y-%m-%d") for d in sd]
    rates = [daily[d]["mentioned"] / daily[d]["total"] * 100
             if daily[d]["total"] else 0 for d in sd]
    ma = [sum(rates[max(0, i - 6):i + 1]) / len(rates[max(0, i - 6):i + 1])
          for i in range(len(rates))]

    fig, ax = plt.subplots(figsize=(12.5, 3.8))
    fig.patch.set_alpha(0.0)
    ax.set_facecolor("none")
    ax.fill_between(dts, ma, color="#A7A6FE", alpha=0.18)
    ax.scatter(dts, rates, s=10, color="#A7A6FE", alpha=0.35, zorder=2)
    ax.plot(dts, ma, color="#C8C7FF", linewidth=3.5, zorder=3)
    ax.annotate(f"{ma[-1]:.1f}%", xy=(dts[-1], ma[-1]),
                xytext=(8, 0), textcoords="offset points",
                ha="left", va="center",
                color="#FAFAFA", fontsize=18, fontweight="bold")
    ax.annotate(f"{ma[0]:.1f}%", xy=(dts[0], ma[0]),
                xytext=(0, -16), textcoords="offset points",
                ha="left", va="top",
                color="#FAFAFA", fontsize=12)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(labelsize=11, colors="#FAFAFA", length=0)
    ax.set_yticks([])
    ax.set_ylim(0, max(rates) * 1.15)
    plt.tight_layout(pad=0.4)
    p = os.path.join(tmpdir, "trend.png")
    fig.savefig(p, dpi=200, transparent=True, bbox_inches="tight")
    plt.close()
    return p


# ============ DECK HELPERS ============
def _wrap_topic_label(label):
    """Always wrap multi-word topic names into 2 balanced lines for visual alignment."""
    words = label.split()
    if len(words) <= 1:
        return label
    best = None
    for i in range(1, len(words)):
        line1 = " ".join(words[:i])
        line2 = " ".join(words[i:])
        score = (max(len(line1), len(line2)), abs(len(line1) - len(line2)))
        if best is None or score < best[0]:
            best = (score, line1, line2)
    return best[1] + "\n" + best[2]


class Deck:
    def __init__(self, prs, total_slides, asset_dir):
        self.prs = prs
        self.total = total_slides
        self.asset_dir = Path(asset_dir)
        self.bg = str(self.asset_dir / "bg.png")
        self.bg_cover = str(self.asset_dir / "bg_cover.png")
        self.logo = str(self.asset_dir / "logo_light.png")
        if not Path(self.logo).exists():
            self.logo = str(self.asset_dir / "yolando-full-light.png")
        self.blank_layout = prs.slide_layouts[6]

    def add_slide(self):
        return self.prs.slides.add_slide(self.blank_layout)

    def full_bg(self, slide, cover=False):
        path = self.bg_cover if cover else self.bg
        if Path(path).exists():
            slide.shapes.add_picture(path, 0, 0,
                                     self.prs.slide_width, self.prs.slide_height)
        else:
            slide.background.fill.solid()
            slide.background.fill.fore_color.rgb = INK

    def picture(self, slide, path, x, y, w=None, h=None):
        kw = {}
        if w: kw["width"] = Inches(w)
        if h: kw["height"] = Inches(h)
        return slide.shapes.add_picture(path, Inches(x), Inches(y), **kw)

    def text(self, slide, x, y, w, h, runs, *, font="Inter", size=14, color=WHITE,
             bold=False, italic=False, align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.TOP,
             char_spacing=None, line_spacing=None):
        tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = 0
        tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = valign
        if isinstance(runs, str):
            runs = [(runs, {})]

        # Split runs on \n into multiple paragraphs so alignment + line spacing
        # apply to every visual line.
        paragraphs = [[]]
        for t, opts in runs:
            parts = t.split("\n")
            for i, part in enumerate(parts):
                if i > 0:
                    paragraphs.append([])
                paragraphs[-1].append((part, opts))

        for p_i, p_runs in enumerate(paragraphs):
            p = tf.paragraphs[0] if p_i == 0 else tf.add_paragraph()
            p.alignment = align
            if line_spacing:
                p.line_spacing = line_spacing
            for rt, opts in p_runs:
                run = p.add_run()
                run.text = rt
                f = run.font
                f.name = opts.get("font", font)
                f.size = Pt(opts.get("size", size))
                f.bold = opts.get("bold", bold)
                f.italic = opts.get("italic", italic)
                f.color.rgb = opts.get("color", color)
                cs = opts.get("char_spacing", char_spacing)
                if cs:
                    rPr = run._r.get_or_add_rPr()
                    rPr.set("spc", str(int(cs * 100)))
        return tb

    def rect(self, slide, x, y, w, h, fill, line=None, line_w=0.75,
             rounded=False, radius=0.06):
        st = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
        s = slide.shapes.add_shape(st, Inches(x), Inches(y), Inches(w), Inches(h))
        if rounded:
            s.adjustments[0] = radius
        s.fill.solid()
        s.fill.fore_color.rgb = fill
        if line is None:
            s.line.fill.background()
        else:
            s.line.color.rgb = line
            s.line.width = Pt(line_w)
        s.shadow.inherit = False
        return s

    def oval(self, slide, x, y, w, h, fill, line=None):
        s = slide.shapes.add_shape(MSO_SHAPE.OVAL,
                                   Inches(x), Inches(y), Inches(w), Inches(h))
        s.fill.solid()
        s.fill.fore_color.rgb = fill
        if line is None:
            s.line.fill.background()
        else:
            s.line.color.rgb = line
        s.shadow.inherit = False
        return s

    def chrome(self, slide, n):
        self.picture(slide, self.logo, 0.5, 6.85, h=0.4)
        self.text(slide, 12.0, 7.05, 1.3, 0.3, f"{n} of {self.total}",
                  font="Inter", size=11, color=FG_2, align=PP_ALIGN.RIGHT)

    def title(self, slide, runs, *, x=0.6, y=0.55, w=12.2, size=38, h=0.85):
        out = []
        for txt, accent in runs:
            out.append((txt, {"size": size, "color": ACCENT if accent else WHITE,
                              "bold": True, "font": "Inter"}))
        self.text(slide, x, y, w, h, out, line_spacing=1.1)

    def subtitle(self, slide, text, *, x=0.6, y=1.55, w=12.2, h=0.5, size=15):
        self.text(slide, x, y, w, h, text, font="Inter", size=size, color=FG_2,
                  line_spacing=1.4)


# ============ SLIDES ============
def slide_cover(deck, m, brand):
    s = deck.add_slide()
    deck.full_bg(s, cover=True)
    deck.picture(s, deck.logo, 0.65, 0.7, h=0.50)
    deck.text(s, 0.65, 3.20, 11, 1.5, brand,
              font="Inter", size=92, color=WHITE, bold=True, line_spacing=1.0)
    days = m["days"]
    deck.text(s, 0.65, 5.10, 11, 0.6,
              [("AI visibility update — ", {"size": 26, "color": WHITE, "font": "Inter"}),
               (f"{days} days of progress",
                {"size": 26, "color": ACCENT, "bold": True, "font": "Inter"})])
    dr = f"{m['date_range'][0]} – {m['date_range'][1]}"
    deck.text(s, 0.65, 6.85, 12, 0.3,
              f"GEO visibility report  ·  {dr}",
              font="Inter", size=11, color=FG_2)


def slide_stands_today(deck, m, brand):
    s = deck.add_slide()
    deck.full_bg(s)
    deck.title(s, [(f"Where {brand} stands ", False), ("today", True)],
               y=0.55, size=38, h=0.85)
    n_topics = len([t for t in m["topic_stats"] if t])
    n_plats = len([p for p in m["platform_stats"] if p])
    sub = (f"Across {m['total_executions']:,} prompt executions, "
           f"{n_topics} verticals, and {n_plats} AI platforms — "
           f"tracked over {m['days']} days "
           f"({m['date_range'][0]} – {m['date_range'][1]}).")
    deck.subtitle(s, sub, y=1.55, size=15)

    card_w = 4.0
    card_h = 4.05
    card_y = 2.30
    gap = 0.18
    x0 = (SLIDE_W - (3 * card_w + 2 * gap)) / 2

    def stat_card(x, big, label, sub_text, big_size=58):
        deck.rect(s, x, card_y, card_w, card_h, CARD_BG, line=ACCENT, line_w=1.2,
                  rounded=True, radius=0.05)
        deck.text(s, x + 0.15, card_y + 0.55, card_w - 0.30, 1.20, big,
                  font="Inter", size=big_size, color=WHITE, bold=True,
                  align=PP_ALIGN.CENTER, line_spacing=1.0)
        deck.text(s, x + 0.4, card_y + 2.05, card_w - 0.8, 0.4, label,
                  font="Inter", size=15, color=FG_2,
                  align=PP_ALIGN.CENTER)
        deck.text(s, x + 0.4, card_y + 2.80, card_w - 0.8, card_h - 3.0, sub_text,
                  font="Inter", size=12, color=FG_2,
                  align=PP_ALIGN.CENTER, line_spacing=1.4)

    fw = m["first_week_rate"]
    lw = m["last_week_rate"]
    delta = lw - fw
    rel = (lw / fw - 1) * 100 if fw else 0
    inv = m["inventory"]

    stat_card(x0, f"{lw:.1f}%", "AI visibility",
              f"Climbed from {fw:.1f}% in week one — +{delta:.1f}pp ({rel:.0f}% relative lift).",
              big_size=58)

    if inv["drafts"] > 0:
        sub2 = (f"{inv['published']} live · {inv['drafts']} drafts in pipeline, "
                f"ready to ship next quarter.")
    else:
        sub2 = f"{inv['published']} articles cited in the dataset to date."
    stat_card(x0 + (card_w + gap), f"{inv['published']}", "Articles published",
              sub2, big_size=66)

    stat_card(x0 + 2 * (card_w + gap),
              f"{m['total_brand_citations']:,}", "URL citations earned",
              f"{brand} pages cited inside AI responses across the tracking window.",
              big_size=58)

    deck.text(s, 0.6, 6.50, 12.2, 0.3,
              [("AI visibility = ", {"size": 11, "color": FG_2, "font": "Inter"}),
               (f"the share of AI prompts in which {brand} is mentioned in the response.",
                {"size": 11, "color": FG_2, "italic": True, "font": "Inter"})],
              align=PP_ALIGN.CENTER)
    deck.chrome(s, 2)


def slide_visibility_trend(deck, m, chart_path):
    s = deck.add_slide()
    deck.full_bg(s)
    delta = m["last_week_rate"] - m["first_week_rate"]
    sign = "+" if delta >= 0 else ""
    deck.title(s, [("AI visibility climbed ", False),
                   (f"{sign}{delta:.1f}pp in {m['days']} days", True)],
               y=0.55, size=38, h=0.85)
    deck.subtitle(s,
                  "7-day moving average — daily mention rate across all tracked prompts.",
                  y=1.55, size=15)
    deck.picture(s, chart_path, 0.65, 2.40, w=12.0, h=4.10)
    deck.chrome(s, 3)


def slide_topic_concentration(deck, m):
    s = deck.add_slide()
    deck.full_bg(s)
    deck.title(s, [("Where the conversation ", False),
                   ("is most concentrated", True)],
               y=0.55, size=34, h=0.85)
    deck.subtitle(s,
                  "Top topics ranked by current visibility — the higher the bar, "
                  "the more mindshare we own.",
                  y=1.55, size=15)

    items = sorted(m["topic_delta"], key=lambda t: -t["current_rate"])[:7]
    chart_x = 0.7
    chart_y = 3.00
    chart_w = SLIDE_W - 1.4
    n = len(items)
    col_gap = 0.20
    col_w = (chart_w - (n - 1) * col_gap) / n
    bar_area_h = 2.55
    bar_max_h = bar_area_h
    label_y = chart_y + bar_area_h + 0.20
    max_pct = max(t["current_rate"] for t in items) * 1.05 if items else 1
    palette = [ACCENT, ACCENT, ACCENT_DEEP, ACCENT_DEEP, ACCENT_DARK,
               COMP_BAR, COMP_BAR, COMP_BAR]

    for i, t in enumerate(items):
        cx = chart_x + i * (col_w + col_gap)
        bar_h = max(0.15, bar_max_h * (t["current_rate"] / max_pct))
        bar_y = chart_y + (bar_area_h - bar_h)
        color = palette[i] if i < len(palette) else COMP_BAR
        deck.rect(s, cx, bar_y, col_w, bar_h, color, rounded=True, radius=0.10)
        d = t["delta"]
        if d > 0.5:
            d_color, d_txt = GREEN_BRIGHT, f"+{d:.1f}pp"
        elif d < -0.5:
            d_color, d_txt = RED, f"{d:.1f}pp"
        else:
            d_color, d_txt = FG_2, f"{d:+.1f}pp"
        deck.text(s, cx, bar_y - 0.85, col_w, 0.35, d_txt,
                  font="Inter", size=12, color=d_color, bold=True,
                  align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        deck.text(s, cx, bar_y - 0.50, col_w, 0.40, f"{t['current_rate']:.1f}%",
                  font="Inter", size=18, color=WHITE, bold=True,
                  align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        deck.text(s, cx, label_y, col_w, 0.80, _wrap_topic_label(t["topic"]),
                  font="Inter", size=10, color=WHITE,
                  align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.TOP, line_spacing=1.20)

    deck.chrome(s, 4)


def slide_topic_delta(deck, m):
    s = deck.add_slide()
    deck.full_bg(s)
    deck.title(s, [("Topic-level progress — ", False),
                   ("90-day delta", True)],
               y=0.55, size=38, h=0.85)
    items = sorted(m["topic_delta"], key=lambda t: -t["current_rate"])[:7]
    n_up = sum(1 for t in items if t["delta"] > 0)
    n_down = sum(1 for t in items if t["delta"] < 0)
    sub = (f"Week-1 baseline (left bars) vs. most recent week (right bars). "
           f"{n_up} of {len(items)} topics are up, {n_down} are down.")
    deck.subtitle(s, sub, y=1.55, size=15)

    leg_y = 2.05
    leg_x = 9.4
    deck.rect(s, leg_x, leg_y + 0.06, 0.30, 0.20, COMP_BAR, rounded=True, radius=0.3)
    deck.text(s, leg_x + 0.40, leg_y, 1.4, 0.30, "Week 1",
              font="Inter", size=11, color=FG_2, valign=MSO_ANCHOR.MIDDLE)
    deck.rect(s, leg_x + 1.85, leg_y + 0.06, 0.30, 0.20, ACCENT, rounded=True, radius=0.3)
    deck.text(s, leg_x + 2.25, leg_y, 1.5, 0.30, "Most recent week",
              font="Inter", size=11, color=FG_2, valign=MSO_ANCHOR.MIDDLE)

    chart_x = 0.7
    chart_y = 3.00
    chart_w = SLIDE_W - 1.4
    n = len(items)
    group_gap = 0.18
    pair_gap = 0.12
    group_w = (chart_w - (n - 1) * group_gap) / n
    bar_w = (group_w - pair_gap) / 2
    bar_area_h = 2.55
    label_y = chart_y + bar_area_h + 0.20
    max_pct = max(max(t["last_rate"], t["first_rate"]) for t in items) * 1.10 if items else 1

    for i, t in enumerate(items):
        gx = chart_x + i * (group_w + group_gap)
        h1 = max(0.10, bar_area_h * (t["first_rate"] / max_pct))
        y1 = chart_y + (bar_area_h - h1)
        deck.rect(s, gx, y1, bar_w, h1, COMP_BAR, rounded=True, radius=0.10)
        h2 = max(0.10, bar_area_h * (t["last_rate"] / max_pct))
        y2 = chart_y + (bar_area_h - h2)
        deck.rect(s, gx + bar_w + pair_gap, y2, bar_w, h2, ACCENT,
                  rounded=True, radius=0.10)
        d = t["delta"]
        if d > 0.5:
            d_color, d_txt = GREEN_BRIGHT, f"+{d:.1f}pp"
        elif d < -0.5:
            d_color, d_txt = RED, f"{d:.1f}pp"
        else:
            d_color, d_txt = FG_2, f"{d:+.1f}pp"
        deck.text(s, gx, min(y1, y2) - 0.45, group_w, 0.35, d_txt,
                  font="Inter", size=12, color=d_color, bold=True,
                  align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        deck.text(s, gx, label_y, group_w, 0.80, _wrap_topic_label(t["topic"]),
                  font="Inter", size=10, color=WHITE,
                  align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.TOP, line_spacing=1.20)

    deck.chrome(s, 5)


def slide_shipped(deck, m, brand):
    s = deck.add_slide()
    deck.full_bg(s)
    deck.title(s, [("What shipped — ", False),
                   ("and what it earned", True)],
               y=0.55, size=34, h=0.85)
    inv = m["inventory"]
    total = inv["published"] + inv["drafts"]
    if inv["drafts"] > 0:
        sub = (f"{total} pieces produced over {m['days']} days  ·  "
               f"{inv['published']} published live  ·  "
               f"{inv['drafts']} in draft pipeline.\n"
               f"Live articles are already driving "
               f"{inv['total_citations']:,} AI citations across the dataset.")
    else:
        sub = (f"{inv['published']} articles cited so far  ·  "
               f"{inv['total_citations']:,} citations earned in the tracking window.")
    deck.subtitle(s, sub, y=1.55, size=14, h=0.7)

    left_x = 0.65
    stat_w = 4.30
    stat_h = 1.15
    stat_gap = 0.20
    stat_y0 = 2.55

    def stat_pill(y, big, big_color, label):
        deck.rect(s, left_x, y, stat_w, stat_h, CARD_BG, line=big_color, line_w=1.0,
                  rounded=True, radius=0.10)
        deck.text(s, left_x + 0.20, y, 2.20, stat_h, big,
                  font="Inter", size=36, color=big_color, bold=True,
                  align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.MIDDLE)
        deck.text(s, left_x + 2.45, y, stat_w - 2.55, stat_h, label,
                  font="Inter", size=13, color=WHITE,
                  align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.MIDDLE)

    stat_pill(stat_y0, str(inv["published"]), ACCENT, "Published")
    stat_pill(stat_y0 + (stat_h + stat_gap),
              str(inv["drafts"]), ORANGE, "In Draft Pipeline")
    stat_pill(stat_y0 + 2 * (stat_h + stat_gap),
              f"{inv['total_citations']:,}", GREEN_BRIGHT, "Citations earned")

    table_x = 5.55
    table_y = 2.55
    table_w = 7.10
    table_h = 4.00
    deck.rect(s, table_x, table_y, table_w, table_h, CARD_BG,
              line=CARD_BORDER, line_w=0.75, rounded=True, radius=0.04)
    deck.text(s, table_x + 0.40, table_y + 0.30, 4.0, 0.35, "Top cited pieces",
              font="Inter", size=14, color=ACCENT, bold=True)
    deck.text(s, table_x + table_w - 1.30, table_y + 0.30, 1.0, 0.35, "Citations",
              font="Inter", size=11, color=FG_2, align=PP_ALIGN.RIGHT)
    deck.rect(s, table_x + 0.40, table_y + 0.78, table_w - 0.80, 0.012,
              CARD_BORDER, rounded=False)

    top = m["article_citations"].most_common(5)
    row_y = table_y + 0.95
    row_h = 0.60
    for i, (url, count) in enumerate(top):
        title_text = title_from_url(url, m["title_map"])
        if len(title_text) > 65:
            title_text = title_text[:62] + "..."
        first_seen = m["article_first_seen"].get(url, "—")
        deck.text(s, table_x + 0.40, row_y, table_w - 1.80, 0.30, title_text,
                  font="Inter", size=12, color=WHITE, valign=MSO_ANCHOR.MIDDLE)
        deck.text(s, table_x + 0.40, row_y + 0.28, table_w - 1.80, 0.25,
                  f"first cited {first_seen}", font="Inter", size=9, color=FG_3,
                  valign=MSO_ANCHOR.MIDDLE)
        deck.text(s, table_x + table_w - 1.20, row_y, 0.80, 0.50, f"{count}",
                  font="Inter", size=22, color=ACCENT, bold=True,
                  align=PP_ALIGN.RIGHT, valign=MSO_ANCHOR.MIDDLE)
        if i < len(top) - 1:
            deck.rect(s, table_x + 0.40, row_y + row_h - 0.02, table_w - 0.80, 0.005,
                      CARD_BORDER, rounded=False)
        row_y += row_h

    deck.chrome(s, 6)


def slide_under_cited(deck, m):
    s = deck.add_slide()
    deck.full_bg(s)
    deck.title(s, [("Under-cited verticals — ", False),
                   ("the unrealized lever", True)],
               y=0.55, size=34, h=0.85)
    deck.subtitle(s,
                  "Three verticals lag the rest of the portfolio — they're where "
                  "the next wave of citations lives.",
                  y=1.55, size=15)

    items_sorted = sorted(m["topic_delta"], key=lambda t: -t["current_rate"])
    high_count = sum(1 for t in items_sorted if t["current_rate"] >= 20)
    mid_count = sum(1 for t in items_sorted if 10 <= t["current_rate"] < 20)
    low_count = sum(1 for t in items_sorted if t["current_rate"] < 10)

    bar_y = 2.55
    bar_h = 0.85
    bar_x = 0.7
    bar_w = SLIDE_W - 1.4
    total = max(1, high_count + mid_count + low_count)
    high_w = bar_w * (high_count / total)
    mid_w = bar_w * (mid_count / total)
    low_w = bar_w * (low_count / total)

    deck.text(s, bar_x, bar_y - 0.45, high_w, 0.35,
              "Strong  ·  ≥20%", font="Inter", size=12, color=ACCENT, bold=True,
              align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
    deck.text(s, bar_x + high_w, bar_y - 0.45, mid_w, 0.35,
              "Mid  ·  10–20%", font="Inter", size=12, color=ACCENT_DEEP, bold=True,
              align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
    deck.text(s, bar_x + high_w + mid_w, bar_y - 0.45, low_w, 0.35,
              "Under-cited  ·  <10%", font="Inter", size=12, color=ORANGE, bold=True,
              align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
    deck.rect(s, bar_x, bar_y, high_w, bar_h, ACCENT, rounded=True, radius=0.05)
    deck.rect(s, bar_x + high_w, bar_y, mid_w, bar_h, ACCENT_DEEP,
              rounded=True, radius=0.05)
    deck.rect(s, bar_x + high_w + mid_w, bar_y, low_w, bar_h, ORANGE,
              rounded=True, radius=0.05)
    deck.text(s, bar_x, bar_y, high_w, bar_h, str(high_count),
              font="Inter", size=28, color=INK, bold=True,
              align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
    deck.text(s, bar_x + high_w, bar_y, mid_w, bar_h, str(mid_count),
              font="Inter", size=28, color=WHITE, bold=True,
              align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
    deck.text(s, bar_x + high_w + mid_w, bar_y, low_w, bar_h, str(low_count),
              font="Inter", size=28, color=INK, bold=True,
              align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    laggards = sorted(m["topic_delta"], key=lambda t: t["current_rate"])[:3]
    card_y = 4.10
    card_h = 1.95
    card_w = 3.95
    gap = 0.22
    x0 = (SLIDE_W - (3 * card_w + 2 * gap)) / 2
    for i, t in enumerate(laggards):
        cx = x0 + i * (card_w + gap)
        deck.rect(s, cx, card_y, card_w, card_h, CARD_BG, line=ORANGE, line_w=1.0,
                  rounded=True, radius=0.06)
        deck.text(s, cx + 0.35, card_y + 0.20, card_w - 0.7, 0.30, "TARGET VERTICAL",
                  font="Inter", size=9, color=ORANGE, bold=True, char_spacing=2.5)
        deck.text(s, cx + 0.35, card_y + 0.55, card_w - 0.7, 0.45, t["topic"],
                  font="Inter", size=16, color=WHITE, bold=True, line_spacing=1.05)
        deck.text(s, cx + 0.35, card_y + 1.05, card_w - 0.7, 0.55,
                  f"{t['current_rate']:.1f}%",
                  font="Inter", size=32, color=ORANGE, bold=True, line_spacing=1.0)
        deck.text(s, cx + 0.35, card_y + 1.65, card_w - 0.7, 0.25, "current visibility",
                  font="Inter", size=10, color=FG_2)

    pill_y = 6.20
    pill_x = 1.20
    pill_w = SLIDE_W - 2.40
    deck.rect(s, pill_x, pill_y, pill_w, 0.50, CARD_BG_2, line=ACCENT, line_w=0.75,
              rounded=True, radius=0.18)
    deck.text(s, pill_x + 0.40, pill_y, pill_w - 0.80, 0.50,
              [("Takeaway:  ", {"size": 11, "color": ACCENT, "font": "Inter", "bold": True}),
               ("Targeting these three verticals with the next content cohort directly attacks "
                "the laggards — the citation engine is already proven elsewhere.",
                {"size": 11, "color": WHITE, "font": "Inter"})],
              valign=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER, line_spacing=1.4)

    deck.chrome(s, 7)


def slide_platforms(deck, m):
    s = deck.add_slide()
    deck.full_bg(s)
    plats = m["platform_stats"]
    rated = []
    for code, st in plats.items():
        if not code:
            continue
        rate = st["mentioned"] / st["total"] * 100 if st["total"] else 0
        rated.append((PLATFORM_NAMES.get(code, code), rate, st["mentioned"]))
    rated.sort(key=lambda r: -r[1])
    if not rated:
        deck.title(s, [("AI platform visibility", False)], y=0.55, size=38, h=0.85)
        deck.chrome(s, 8)
        return

    leader = rated[0][0]
    laggard = rated[-1][0]
    deck.title(s, [(f"{leader} leads — ", False),
                   (f"{laggard} is the gap", True)],
               y=0.55, size=38, h=0.85)
    deck.subtitle(s,
                  "Visibility varies sharply by AI platform. The lowest two are also "
                  "where targeted citation work compounds fastest.",
                  y=1.55, size=15)

    rows_y = 2.85
    row_h = 0.78
    row_gap = 0.22
    label_w = 1.60
    bar_x = 2.40
    bar_max_w = 7.60
    val_x = bar_x + bar_max_w + 0.20
    max_rate = max(r[1] for r in rated) * 1.05 if rated else 1
    for i, (name, rate, count) in enumerate(rated):
        y = rows_y + i * (row_h + row_gap)
        deck.text(s, 0.65, y, label_w, row_h, name,
                  font="Inter", size=15, color=WHITE, bold=True,
                  valign=MSO_ANCHOR.MIDDLE)
        deck.rect(s, bar_x, y + 0.18, bar_max_w, row_h - 0.36, CARD_BG_2,
                  rounded=True, radius=0.30)
        bw = max(0.30, bar_max_w * (rate / max_rate))
        color = ACCENT if i == 0 else (ACCENT_DEEP if i == 1 else ACCENT_DARK)
        deck.rect(s, bar_x, y + 0.18, bw, row_h - 0.36, color,
                  rounded=True, radius=0.30)
        deck.text(s, bar_x + bw + 0.10, y, 1.4, row_h, f"{rate:.1f}%",
                  font="Inter", size=18, color=WHITE, bold=True,
                  valign=MSO_ANCHOR.MIDDLE)
        deck.text(s, val_x + 1.0, y, 2.0, row_h, f"{count:,} mentions",
                  font="Inter", size=11, color=FG_2,
                  valign=MSO_ANCHOR.MIDDLE)

    deck.chrome(s, 8)


def slide_focus_next(deck, m, brand):
    s = deck.add_slide()
    deck.full_bg(s)
    deck.title(s, [("Where we're focused ", False), ("next", True)],
               y=0.55, size=38, h=0.85)
    deck.subtitle(s,
                  "Two priorities for the coming quarter — informed directly by the gaps "
                  "and pipeline above.",
                  y=1.55, size=15)

    laggards = sorted(m["topic_delta"], key=lambda t: t["current_rate"])[:3]
    laggard_topics = [t["topic"] for t in laggards] if len(laggards) >= 3 else \
                     [t["topic"] for t in laggards] + ["—"] * (3 - len(laggards))
    if laggards:
        laggard_range = (f"{min(t['current_rate'] for t in laggards):.1f}–"
                         f"{max(t['current_rate'] for t in laggards):.1f}%")
    else:
        laggard_range = "n/a"

    plats = m["platform_stats"]
    rated = []
    for code, st in plats.items():
        if not code:
            continue
        rate = st["mentioned"] / st["total"] * 100 if st["total"] else 0
        rated.append((PLATFORM_NAMES.get(code, code), rate))
    rated.sort(key=lambda r: -r[1])
    top_plat = rated[0] if rated else ("(top)", 0)
    weak_plats = rated[-2:] if len(rated) >= 2 else rated

    def focus_card(x, y, w, h, eyebrow, title_text, bullets, callout):
        deck.rect(s, x, y, w, h, CARD_BG, line=CARD_BORDER, line_w=1.0,
                  rounded=True, radius=0.04)
        deck.rect(s, x + 0.4, y + 0.35, 1.3, 0.32, CARD_BG_2,
                  line=ACCENT, line_w=0.75, rounded=True, radius=0.5)
        deck.text(s, x + 0.4, y + 0.35, 1.3, 0.32, eyebrow,
                  font="Inter", size=10, color=ACCENT, bold=True,
                  align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        deck.text(s, x + 0.4, y + 0.80, w - 0.8, 0.50, title_text,
                  font="Inter", size=20, color=WHITE, bold=True, line_spacing=1.1)
        bullet_y = y + 1.50
        for b in bullets:
            deck.oval(s, x + 0.45, bullet_y + 0.06, 0.24, 0.24, GREEN_BG,
                      line=GREEN_BRIGHT)
            deck.text(s, x + 0.45, bullet_y + 0.06, 0.24, 0.24, "✓",
                      font="Inter", size=11, color=GREEN_BRIGHT, bold=True,
                      align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
            deck.text(s, x + 0.83, bullet_y, w - 1.05, 0.40, b,
                      font="Inter", size=11, color=WHITE,
                      valign=MSO_ANCHOR.MIDDLE, line_spacing=1.3)
            bullet_y += 0.48
        co_h = 0.80
        co_y = y + h - co_h - 0.25
        deck.rect(s, x + 0.4, co_y, w - 0.8, co_h, CARD_BG_2,
                  line=ACCENT, line_w=0.75, rounded=True, radius=0.08)
        deck.text(s, x + 0.55, co_y, w - 1.1, co_h, callout,
                  font="Inter", size=11, color=ACCENT,
                  valign=MSO_ANCHOR.MIDDLE, line_spacing=1.35)

    card_w = 6.10
    card_h = 4.55
    card_y = 2.05
    card_gap = 0.30
    x0 = (SLIDE_W - (2 * card_w + card_gap)) / 2

    focus_card(
        x0, card_y, card_w, card_h,
        "FOCUS 01", "Publish into laggard verticals",
        [
            f"Next wave into {laggard_topics[0]}, {laggard_topics[1]}, {laggard_topics[2]}",
            "Mirror the article pattern that already won in top verticals",
            "Match each new slug into the citation tracker on day one",
            "Refresh top-cited posts to keep their authority compounding",
        ],
        f"These three verticals sit at {laggard_range} today — the playbook that drove "
        f"the leaders applies directly here.",
    )
    weak_label = weak_plats[-1][0] if weak_plats else "the lagging platform"
    weak_rate = weak_plats[-1][1] if weak_plats else 0
    focus_card(
        x0 + card_w + card_gap, card_y, card_w, card_h,
        "FOCUS 02", f"Close the {weak_label} gap",
        [
            "Earn third-party reviews on G2, Capterra, industry directories",
            "Add structured FAQ + HowTo schema to all comparison pages",
            "Pitch original product or category data to industry media",
            f"Cross-link {brand} product surfaces back to cited blog posts",
        ],
        f"{brand} sits at {weak_rate:.1f}% on {weak_label} vs. {top_plat[1]:.1f}% on "
        f"{top_plat[0]} — small lifts compound across every vertical.",
    )

    deck.chrome(s, 9)


# ============ ASSET DISCOVERY ============
OVERRIDE_ASSETS = ("bg.png", "bg_cover.png", "logo_light.png")


def _candidate_dirs(skill_root):
    """Yield directories that might contain deck assets."""
    yield skill_root / "assets"
    yield (
        skill_root.parents[2]
        / "styleguide"
        / "skills"
        / "visual-styleguide"
        / "references"
        / "yolando-design-system"
        / "assets"
    )
    # Walk a few levels up from the skill itself in case a sibling owns shared assets.
    p = skill_root
    for _ in range(5):
        p = p.parent
        if not p or not p.exists():
            break
        try:
            for hit in p.glob("*/assets"):
                yield hit
        except (PermissionError, OSError):
            continue


def find_assets_dir(skill_root, override=None):
    """Locate the directory containing deck assets.
    Order: --assets-dir override → <skill>/assets → siblings of the skill folder."""
    if override:
        c = Path(override)
        if c.is_dir() and ((c / "logo_light.png").exists() or (c / "yolando-full-light.png").exists()):
            return c
        raise FileNotFoundError(
            f"--assets-dir {override} must contain logo_light.png or yolando-full-light.png")
    seen = set()
    for c in _candidate_dirs(skill_root):
        cs = str(c)
        if cs in seen:
            continue
        seen.add(cs)
        if c.is_dir() and ((c / "logo_light.png").exists() or (c / "yolando-full-light.png").exists()):
            return c
    raise FileNotFoundError(
        "Could not locate deck assets "
        f"({', '.join(OVERRIDE_ASSETS)} or Yolando styleguide assets). Copy them into "
        f"{skill_root / 'assets'} or pass --assets-dir explicitly."
    )


# ============ BUILD ============
def build_deck(csv_path, brand_name, output_pptx, *,
               brand_keyword=None, inventory=None, title_map=None,
               assets_dir=None):
    skill_root = Path(__file__).resolve().parent.parent
    asset_dir = find_assets_dir(skill_root, assets_dir)

    metrics = load_and_analyze(csv_path, brand_name,
                               brand_keyword=brand_keyword,
                               inventory=inventory,
                               title_map=title_map)
    tmp = tempfile.mkdtemp()
    chart_path = make_chart_visibility_trend(metrics, tmp)

    prs = Presentation()
    prs.slide_width = Inches(SLIDE_W)
    prs.slide_height = Inches(SLIDE_H)
    deck = Deck(prs, total_slides=9, asset_dir=asset_dir)

    slide_cover(deck, metrics, brand_name)
    slide_stands_today(deck, metrics, brand_name)
    slide_visibility_trend(deck, metrics, chart_path)
    slide_topic_concentration(deck, metrics)
    slide_topic_delta(deck, metrics)
    slide_shipped(deck, metrics, brand_name)
    slide_under_cited(deck, metrics)
    slide_platforms(deck, metrics)
    slide_focus_next(deck, metrics, brand_name)

    output_pptx = str(output_pptx)
    Path(output_pptx).parent.mkdir(parents=True, exist_ok=True)
    prs.save(output_pptx)

    pdf_path = output_pptx.rsplit(".", 1)[0] + ".pdf"
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if soffice:
        subprocess.run(
            [soffice, "--headless", "--convert-to", "pdf",
             "--outdir", str(Path(output_pptx).parent), output_pptx],
            check=False, stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL, timeout=120,
        )
    return output_pptx, pdf_path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("csv_path", help="Path to prompt_executions CSV")
    p.add_argument("brand_name", help="Tracked brand name")
    p.add_argument("output_pptx", help="Output .pptx path")
    p.add_argument("--brand-domain-keyword", default=None,
                   help="Override the keyword used to identify brand-owned URLs in citations")
    p.add_argument("--published-count", type=int, default=None,
                   help="Number of articles live on the brand's site (overrides data-derived count)")
    p.add_argument("--drafts-count", type=int, default=None,
                   help="Number of unpublished drafts in the pipeline")
    p.add_argument("--total-article-citations", type=int, default=None,
                   help="Total article citations across the dataset (overrides data-derived count)")
    p.add_argument("--article-titles-json", default=None,
                   help="JSON file mapping article URLs to display titles")
    p.add_argument("--assets-dir", default=None,
                   help="Optional asset directory containing logo_light.png and optional bg.png/bg_cover.png")
    args = p.parse_args()

    inventory = {}
    if args.published_count is not None:
        inventory["published"] = args.published_count
    if args.drafts_count is not None:
        inventory["drafts"] = args.drafts_count
    if args.total_article_citations is not None:
        inventory["total_citations"] = args.total_article_citations

    title_map = {}
    if args.article_titles_json:
        with open(args.article_titles_json) as f:
            title_map = json.load(f)

    pptx, pdf = build_deck(
        csv_path=args.csv_path,
        brand_name=args.brand_name,
        output_pptx=args.output_pptx,
        brand_keyword=args.brand_domain_keyword,
        inventory=inventory or None,
        title_map=title_map,
        assets_dir=args.assets_dir,
    )
    print(f"Saved PPTX: {pptx}")
    if Path(pdf).exists():
        print(f"Saved PDF:  {pdf}")


if __name__ == "__main__":
    main()
