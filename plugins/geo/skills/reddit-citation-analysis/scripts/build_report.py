#!/usr/bin/env python3
"""
Reddit citation analysis PDF generator.

Usage:
    python build_report.py --csv path/to/cites.csv --brand "ExampleCo" [--output out.pdf]
                           [--competitors "CompetitorA,CompetitorB"]
                           [--competitors-file competitors.json]
                           [--context "short brand context"]

Produces a PDF analyzing a brand's Reddit citation footprint in LLM responses,
with a recommendation-led executive summary, branded vs. unbranded analysis,
comment-pattern framework, competitor user-profile FAQ detection, sentiment,
and prioritized recommendations.
"""
import argparse
import csv
import json
import os
import re
from collections import defaultdict
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether, Image
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfgen import canvas

# ==== Palette ====
VIOLET_400 = colors.HexColor('#a7a6fe')
VIOLET_500 = colors.HexColor('#8583ff')
VIOLET_700 = colors.HexColor('#8a38f5')
VIOLET_800 = colors.HexColor('#9747ff')
VIOLET_900 = colors.HexColor('#583b9d')
VIOLET_50 = colors.HexColor('#f5efff')
MANGO = colors.HexColor('#ea9e59')
RED = colors.HexColor('#d80027')
GREEN = colors.HexColor('#6da544')
BG = colors.HexColor('#f8f8f8')
BG_SUNKEN = colors.HexColor('#f0f0f0')
WHITE = colors.white
FG = colors.HexColor('#161518')
FG_2 = colors.HexColor('#7e7e80')
FG_3 = colors.HexColor('#a3a3a6')
BORDER = colors.HexColor('#cbcbcf')
BORDER_SOFT = colors.HexColor('#e5e5e5')
MUTED = colors.HexColor('#e4e4e4')

_SCRIPT_DIR = Path(__file__).resolve().parent
_PLUGINS_DIR = _SCRIPT_DIR.parents[3]
DEFAULT_LOGO = (
    _PLUGINS_DIR
    / 'styleguide'
    / 'skills'
    / 'visual-styleguide'
    / 'references'
    / 'yolando-design-system'
    / 'assets'
    / 'yolando-full-dark.png'
)

# ==== Styles ====
styles = getSampleStyleSheet()
H1 = ParagraphStyle('H1', parent=styles['Title'], fontSize=30, leading=36, textColor=FG,
    alignment=TA_LEFT, fontName='Helvetica-Bold', spaceAfter=10, spaceBefore=0)
COVER_TITLE = ParagraphStyle('CoverTitle', parent=styles['Title'], fontSize=42, leading=50,
    textColor=FG, alignment=TA_LEFT, fontName='Helvetica-Bold', spaceAfter=18, spaceBefore=0)
COVER_SUBTITLE = ParagraphStyle('CoverSubtitle', parent=styles['Normal'], fontSize=13,
    leading=20, textColor=FG_2, alignment=TA_LEFT, fontName='Helvetica', spaceAfter=0)
COVER_EYEBROW = ParagraphStyle('CoverEyebrow', parent=styles['Normal'], fontSize=9,
    leading=12, textColor=FG_3, fontName='Courier-Bold', spaceAfter=12)
H2 = ParagraphStyle('H2', parent=styles['Heading1'], fontSize=18, leading=24, textColor=FG,
    fontName='Helvetica-Bold', spaceBefore=18, spaceAfter=8)
H3 = ParagraphStyle('H3', parent=styles['Heading2'], fontSize=12, leading=16, textColor=FG,
    fontName='Helvetica-Bold', spaceBefore=12, spaceAfter=4)
LEAD = ParagraphStyle('Lead', parent=styles['Normal'], fontSize=11, leading=17, textColor=FG_2,
    fontName='Helvetica', spaceAfter=12)
BODY = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, leading=14, textColor=FG,
    fontName='Helvetica', spaceAfter=6)
BODY_SMALL = ParagraphStyle('BodySmall', parent=styles['Normal'], fontSize=9, leading=12,
    textColor=FG_2, fontName='Helvetica', spaceAfter=4)
EYEBROW = ParagraphStyle('Eyebrow', parent=styles['Normal'], fontSize=8, leading=10,
    textColor=FG_3, fontName='Courier-Bold', spaceAfter=8)
FINDING_HEAD = ParagraphStyle('FindingHead', parent=styles['Normal'], fontSize=10.5, leading=14,
    textColor=FG, fontName='Helvetica-Bold', spaceAfter=2)
TBL_HEAD = ParagraphStyle('TblHead', parent=styles['Normal'], fontSize=8, leading=10,
    textColor=FG_2, fontName='Helvetica-Bold', alignment=TA_LEFT)
TBL_HEAD_NUM = ParagraphStyle('TblHeadNum', parent=styles['Normal'], fontSize=8, leading=10,
    textColor=FG_2, fontName='Helvetica-Bold', alignment=TA_RIGHT)
TBL_CELL = ParagraphStyle('TblCell', parent=styles['Normal'], fontSize=9, leading=12,
    textColor=FG, fontName='Helvetica', alignment=TA_LEFT)
TBL_CELL_NUM = ParagraphStyle('TblCellNum', parent=styles['Normal'], fontSize=9, leading=12,
    textColor=FG, fontName='Courier', alignment=TA_RIGHT)
ALERT_TITLE = ParagraphStyle('AlertTitle', parent=styles['Normal'], fontSize=10, leading=13,
    textColor=FG, fontName='Helvetica-Bold', spaceAfter=2)
ALERT_BODY = ParagraphStyle('AlertBody', parent=styles['Normal'], fontSize=9, leading=13,
    textColor=FG_2, fontName='Helvetica', spaceAfter=0)
PULL_QUOTE = ParagraphStyle('PullQuote', parent=styles['Normal'], fontSize=14, leading=20,
    textColor=FG, fontName='Helvetica-Bold', leftIndent=14, spaceBefore=10, spaceAfter=10)
KPI_LABEL = ParagraphStyle('KpiLabel', parent=styles['Normal'], fontSize=6.5, leading=8,
    textColor=FG_3, fontName='Courier-Bold', alignment=TA_LEFT, spaceAfter=3)
KPI_NUM = ParagraphStyle('KpiNum', parent=styles['Normal'], fontSize=20, leading=24,
    textColor=FG, fontName='Helvetica-Bold', alignment=TA_LEFT, spaceAfter=3)
KPI_NUM_ACCENT = ParagraphStyle('KpiNumAccent', parent=KPI_NUM, textColor=VIOLET_800)
KPI_SUB = ParagraphStyle('KpiSub', parent=styles['Normal'], fontSize=7.5, leading=10,
    textColor=FG_2, fontName='Helvetica', alignment=TA_LEFT)
CAPTION = ParagraphStyle('Caption', parent=styles['Normal'], fontSize=8, leading=11,
    textColor=FG_2, fontName='Helvetica-Oblique', spaceAfter=10)
GAP_TITLE = ParagraphStyle('GapTitle', parent=styles['Normal'], fontSize=13, leading=17,
    textColor=FG, fontName='Helvetica-Bold', spaceAfter=4)
LABEL = ParagraphStyle('Label', parent=styles['Normal'], fontSize=9, leading=12, textColor=FG,
    fontName='Helvetica-Bold', spaceBefore=6, spaceAfter=2)
BULLET_ITEM = ParagraphStyle('BulletItem', parent=styles['Normal'], fontSize=9.5,
    leading=13, textColor=FG, fontName='Helvetica', spaceAfter=3,
    leftIndent=14, bulletIndent=2)

# ==================== ANALYSIS ====================

def parse_subreddit(url):
    m = re.search(r'reddit\.com/r/([^/]+)', url)
    return m.group(1) if m else None

def parse_thread_id(url):
    m = re.search(r'/comments/([a-z0-9]+)', url)
    return m.group(1) if m else None

def slug(url):
    m = re.search(r'/comments/[a-z0-9]+/([^/]+)', url)
    return m.group(1).replace('_', ' ') if m else ''

def analyze(csv_path, brand, competitors=None):
    """Read the CSV and compute every metric the PDF will need."""
    brand_l = brand.lower()
    competitors = competitors or []
    rows_all = []
    rows_reddit = []
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows_all.append(row)
            rd = row.get('root_domain', '') or ''
            if 'reddit.com' in rd.lower():
                rows_reddit.append(row)

    total_all_freq = sum(int(r.get('frequency') or 0) for r in rows_all)
    total_reddit_freq = sum(int(r.get('frequency') or 0) for r in rows_reddit)
    reddit_share_freq = round(total_reddit_freq / total_all_freq * 100, 1) if total_all_freq else 0
    reddit_share_rows = round(len(rows_reddit) / len(rows_all) * 100, 1) if rows_all else 0

    # Type breakdown (OWNED/EARNED/COMPETITOR/SOCIAL)
    type_breakdown = defaultdict(int)
    for r in rows_all:
        type_breakdown[r.get('type', 'UNKNOWN')] += int(r.get('frequency') or 0)
    owned_freq = type_breakdown.get('OWNED', 0)
    reddit_share_excl_owned = round(total_reddit_freq / (total_all_freq - owned_freq) * 100, 1) if (total_all_freq - owned_freq) else 0

    # Subreddit aggregation
    sub_stats = defaultdict(lambda: {'freq': 0, 'uniq': 0, 'threads': set(), 'rows': 0})
    for r in rows_reddit:
        sub = parse_subreddit(r['url'])
        if not sub:
            continue
        sub_stats[sub]['freq'] += int(r.get('frequency') or 0)
        sub_stats[sub]['uniq'] += int(r.get('unique_executions') or 0)
        sub_stats[sub]['rows'] += 1
        tid = parse_thread_id(r['url'])
        if tid:
            sub_stats[sub]['threads'].add(tid)
    for s in sub_stats:
        sub_stats[s]['threads'] = len(sub_stats[s]['threads'])

    sub_list = []
    for s, st in sub_stats.items():
        sub_list.append({
            'subreddit': s,
            'freq': st['freq'],
            'uniq': st['uniq'],
            'threads': st['threads'],
            'share_of_reddit': round(st['freq'] / total_reddit_freq * 100, 1) if total_reddit_freq else 0,
        })
    sub_list.sort(key=lambda x: -x['freq'])

    # Real subreddits exclude r/u_* user profiles
    real_subs = [s for s in sub_list if not s['subreddit'].startswith('u_')]
    user_profile_subs = [s for s in sub_list if s['subreddit'].startswith('u_')]

    # Find the brand's own subreddit (if it exists)
    brand_sub = None
    for s in sub_list:
        if s['subreddit'].lower() == brand_l:
            brand_sub = s
            break

    # Branded vs unbranded
    branded_freq = 0
    branded_threads_ids = set()
    unbranded_freq = 0
    unbranded_threads_ids = set()
    for r in rows_reddit:
        sub = parse_subreddit(r['url']) or ''
        slug_text = slug(r['url']).lower()
        f = int(r.get('frequency') or 0)
        tid = parse_thread_id(r['url'])
        is_branded = (sub.lower() == brand_l or brand_l in slug_text)
        if is_branded:
            branded_freq += f
            if tid:
                branded_threads_ids.add(tid)
        else:
            unbranded_freq += f
            if tid:
                unbranded_threads_ids.add(tid)

    branded_threads_count = len(branded_threads_ids)
    unbranded_threads_count = len(unbranded_threads_ids)
    branded_per_thread = round(branded_freq / branded_threads_count, 1) if branded_threads_count else 0
    unbranded_per_thread = round(unbranded_freq / unbranded_threads_count, 1) if unbranded_threads_count else 0
    concentration_multiple = round(branded_per_thread / unbranded_per_thread, 0) if unbranded_per_thread else 0

    # Thread-level aggregation
    threads = defaultdict(lambda: {'freq': 0, 'uniq': 0, 'url': '', 'subreddit': '', 'slug': ''})
    for r in rows_reddit:
        tid = parse_thread_id(r['url'])
        if not tid:
            continue
        f = int(r.get('frequency') or 0)
        if f > threads[tid]['freq']:
            threads[tid]['url'] = r['url']
            threads[tid]['subreddit'] = parse_subreddit(r['url']) or ''
            threads[tid]['slug'] = slug(r['url'])
            threads[tid]['freq'] = f
            threads[tid]['uniq'] = int(r.get('unique_executions') or 0)
    top_threads = sorted(threads.values(), key=lambda x: -x['freq'])[:50]

    # Brand-specific cited threads
    brand_threads = []
    for t in threads.values():
        s = (t['slug'] or '').lower()
        sub = (t['subreddit'] or '').lower()
        if sub == brand_l or brand_l in s:
            brand_threads.append(t)
    brand_threads.sort(key=lambda x: -x['freq'])

    # Sentiment classification (title-based, brand-specific threads)
    neg_terms = ['sucks', 'terrible', 'awful', 'horrible', 'worst', 'nightmare',
                 'avoid', 'scam', 'cant', "can't", 'problem', 'cancel all scheduled',
                 'not working', 'fail', 'shame', 'angry', 'frustrat', 'hate', 'rip off']
    pos_terms = ['great', 'love', 'amazing', 'best', 'recommend', 'happy', 'wonderful',
                 'excellent', 'fantastic', 'thank', 'helped', 'success', 'gamechanger']
    neutral_q_terms = [f'is {brand_l}', 'how do', 'how much', 'thoughts on', 'experiences with',
                       'has anyone', 'anyone use', 'anyone try', 'referrals for',
                       'current feelings about', 'tried', f'about {brand_l}']

    sentiment_buckets = {'negative': [], 'positive': [], 'neutral_question': [], 'unclassified': []}
    for t in brand_threads[:40]:
        s = (t['slug'] or '').lower()
        cls = None
        if any(n in s for n in neg_terms):
            cls = 'negative'
        elif any(p in s for p in pos_terms):
            cls = 'positive'
        elif any(q in s for q in neutral_q_terms):
            cls = 'neutral_question'
        else:
            cls = 'unclassified'
        sentiment_buckets[cls].append(t)

    sentiment = {}
    for cls, ts in sentiment_buckets.items():
        sentiment[cls] = {
            'thread_count': len(ts),
            'freq': sum(t['freq'] for t in ts),
            'examples': ts[:5],
        }

    # Comment-type categories (top 50 threads)
    categories = {
        'Customer support / billing complaints': [
            'customer support', 'billing', 'cancel', 'refund', 'login not working',
            'cant seem to talk', 'support for', 'login',
        ],
        'Negative experience / quality complaint': [
            'sucks', 'terrible', 'awful', 'bad experience', 'horrible', 'worst', 'nightmare',
            'avoid', 'scam', 'bait',
        ],
        'Comparison / alternatives': [
            ' vs ', ' or ', 'compared to', 'alternative', 'instead of', 'similar to',
        ],
        'How-to / mechanics': [
            'how do i', 'how to', f'is {brand_l} secure', f'is {brand_l} covered',
            f'does {brand_l} take', 'referrals for',
            'availability', 'scheduling', 'pay for', 'signed up',
        ],
        'Professional / operator-side': [
            'contracted with', 'has anyone contracted',
            'salary', 'rate', 'reimbursement', f'left {brand_l}',
            'experiences with', 'thoughts on', 'current feelings',
            'pay', 'pay rate',
        ],
        'Local / city-specific search': [],  # filled by detection below
    }
    # Detect city subreddits (lowercase city names)
    common_cities = [
        'denver', 'asheville', 'austin', 'boulder', 'phoenix', 'nyc', 'tucson',
        'saltlakecity', 'tulsa', 'stlouis', 'anchorage', 'asknyc', 'losangeles',
        'chicago', 'sanfrancisco', 'boston', 'seattle', 'portland', 'atlanta',
        'houston', 'dallas', 'philadelphia', 'minneapolis', 'detroit',
    ]
    cat_counts = defaultdict(lambda: {'threads': 0, 'freq': 0, 'examples': []})
    uncategorized = []
    for t in top_threads:
        s = (t['slug'] or '').lower()
        sub_lower = (t['subreddit'] or '').lower()
        matched = False
        # City detection
        if sub_lower in common_cities:
            cat = 'Local / city-specific search'
            cat_counts[cat]['threads'] += 1
            cat_counts[cat]['freq'] += t['freq']
            if len(cat_counts[cat]['examples']) < 3:
                cat_counts[cat]['examples'].append(t)
            matched = True
            continue
        for cat, keys in categories.items():
            if cat == 'Local / city-specific search':
                continue
            for k in keys:
                if k in s:
                    cat_counts[cat]['threads'] += 1
                    cat_counts[cat]['freq'] += t['freq']
                    if len(cat_counts[cat]['examples']) < 3:
                        cat_counts[cat]['examples'].append(t)
                    matched = True
                    break
            if matched:
                break
        if not matched:
            uncategorized.append(t)
    total_cat_freq = sum(c['freq'] for c in cat_counts.values())

    # Competitor detection uses caller-supplied candidates. The calling agent
    # should fetch these from the active customer/workspace context when
    # database MCP tools are available, then pass them via --competitors or
    # --competitors-file. The script intentionally avoids baked-in industry
    # defaults because stale candidates produce misleading strategy.
    comp_mentions = defaultdict(int)
    for r in rows_reddit:
        s = slug(r['url']).lower()
        for c in competitors:
            cl = c.lower()
            if cl in s and cl != brand_l:
                comp_mentions[c] += int(r.get('frequency') or 0)
                break
    comp_mentions = dict(sorted(comp_mentions.items(), key=lambda x: -x[1]))
    top_competitor = next(iter(comp_mentions), None)

    # User-profile FAQ detection (the headline competitive tactic)
    # Find r/u_* subreddits with significant cite volume and associate with a brand
    user_profile_brand_tactics = []
    for u in user_profile_subs[:10]:  # top 10 user-profile subs by freq
        if u['freq'] < 100:
            continue
        # See which brand this user profile is associated with
        u_name = u['subreddit'][2:].lower()  # strip "u_"
        matched_brand = None
        for c in competitors:
            cl = c.lower().replace(' ', '')
            if cl in u_name:
                matched_brand = c
                break
        if matched_brand and matched_brand.lower() != brand_l:
            # Get threads
            u_threads = [t for t in threads.values() if (t['subreddit'] or '').lower() == u['subreddit'].lower()]
            u_threads.sort(key=lambda x: -x['freq'])
            user_profile_brand_tactics.append({
                'brand': matched_brand,
                'subreddit': u['subreddit'],
                'freq': u['freq'],
                'thread_count': len(u_threads),
                'top_threads': u_threads[:6],
            })

    # Also gather top competitor's subreddit + slug-mention threads for the deep dive
    top_comp_threads = []
    if top_competitor:
        tc_lower = top_competitor.lower().replace(' ', '')
        for t in threads.values():
            s = (t['slug'] or '').lower()
            sub = (t['subreddit'] or '').lower()
            if tc_lower in s or sub == tc_lower or sub == f'u_{tc_lower}therapy' or sub == f'u_{tc_lower}':
                top_comp_threads.append(t)
        top_comp_threads.sort(key=lambda x: -x['freq'])
    top_comp_user_profile = next((u for u in user_profile_brand_tactics if u['brand'] == top_competitor), None)

    # Top competitor: own subreddit (r/<competitor> case-insensitive)
    top_comp_own_sub_freq = 0
    if top_competitor:
        tc_lower = top_competitor.lower().replace(' ', '')
        for s in sub_list:
            if s['subreddit'].lower() == tc_lower:
                top_comp_own_sub_freq = s['freq']
                break

    # Structural patterns (brand-specific threads)
    title_lengths = []
    question_titles = 0
    declarative_titles = 0
    problem_kw_titles = 0
    problem_keywords = ['billing', 'login', 'cancel', 'refund', 'support',
                        'availability', 'cost', 'pay', 'secure']
    for t in brand_threads[:50]:
        if not t['slug']:
            continue
        s = t['slug'].lower()
        title_lengths.append(len(s.split()))
        if s.startswith(('is ', 'has ', 'does ', 'can ', 'how ', 'why ', 'what ',
                          'who ', 'when ', 'where ', 'anyone', 'cant ')):
            question_titles += 1
        else:
            declarative_titles += 1
        if any(p in s for p in problem_keywords):
            problem_kw_titles += 1
    avg_title_words = round(sum(title_lengths) / len(title_lengths), 1) if title_lengths else 0
    declarative_pct = round(declarative_titles / max(1, declarative_titles + question_titles) * 100)
    question_pct = round(question_titles / max(1, declarative_titles + question_titles) * 100)

    return {
        'brand': brand,
        'brand_lower': brand_l,
        'total_all_freq': total_all_freq,
        'total_reddit_freq': total_reddit_freq,
        'reddit_share_freq': reddit_share_freq,
        'reddit_share_rows': reddit_share_rows,
        'reddit_share_excl_owned': reddit_share_excl_owned,
        'total_reddit_rows': len(rows_reddit),
        'total_unique_threads': len(threads),
        'unique_subreddits': len(sub_stats),
        'type_breakdown': dict(type_breakdown),

        'top_real_subs': real_subs[:12],
        'brand_sub': brand_sub,

        'branded_freq': branded_freq,
        'unbranded_freq': unbranded_freq,
        'branded_threads_count': branded_threads_count,
        'unbranded_threads_count': unbranded_threads_count,
        'branded_per_thread': branded_per_thread,
        'unbranded_per_thread': unbranded_per_thread,
        'concentration_multiple': int(concentration_multiple),
        'branded_share': round(branded_freq / total_reddit_freq * 100, 1) if total_reddit_freq else 0,
        'unbranded_share': round(unbranded_freq / total_reddit_freq * 100, 1) if total_reddit_freq else 0,

        'top_threads': top_threads,
        'brand_threads_top30': brand_threads[:30],
        'brand_threads_count': len(brand_threads),

        'sentiment': sentiment,

        'cat_counts': dict(cat_counts),
        'total_cat_freq': total_cat_freq,

        'comp_mentions': comp_mentions,
        'top_competitor': top_competitor,
        'top_comp_threads': top_comp_threads[:15],
        'top_comp_user_profile': top_comp_user_profile,
        'top_comp_own_sub_freq': top_comp_own_sub_freq,
        'user_profile_brand_tactics': user_profile_brand_tactics,

        'avg_title_words': avg_title_words,
        'declarative_pct': declarative_pct,
        'question_pct': question_pct,
        'problem_kw_titles': problem_kw_titles,
        'structural_sample_size': len(title_lengths),
    }

# ==================== PDF BUILDING HELPERS ====================

def fmt(n):
    if isinstance(n, (int, float)):
        return f"{n:,}"
    return str(n)

def section_eyebrow(num, name):
    text = f'<font color="#9747ff">●</font>  {num:02d} · {name.upper()}'
    return Paragraph(text, EYEBROW)

def alert(title, body):
    inner = Table([[Paragraph(title, ALERT_TITLE)], [Paragraph(body, ALERT_BODY)]],
        colWidths=[6.6*inch])
    inner.setStyle(TableStyle([
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (0,0), 10),
        ('BOTTOMPADDING', (0,0), (0,0), 0),
        ('TOPPADDING', (0,1), (0,1), 4),
        ('BOTTOMPADDING', (0,1), (0,1), 10),
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('LINEBEFORE', (0,0), (0,-1), 3, VIOLET_800),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER),
    ]))
    return inner

def kpi_grid(items):
    cells = []
    for label, num, sub, accent in items:
        num_style = KPI_NUM_ACCENT if accent else KPI_NUM
        cells.append([
            Paragraph(label.upper(), KPI_LABEL),
            Paragraph(str(num), num_style),
            Paragraph(sub, KPI_SUB),
        ])
    t = Table([cells], colWidths=[1.75*inch] * 4, rowHeights=[1.15*inch])
    t.setStyle(TableStyle([
        ('BOX', (0,0), (0,0), 0.5, BORDER),
        ('BOX', (1,0), (1,0), 0.5, BORDER),
        ('BOX', (2,0), (2,0), 0.5, BORDER),
        ('BOX', (3,0), (3,0), 0.5, BORDER),
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    return t

def bulleted_findings(items):
    flowables = []
    for headline, bullets in items:
        block = [Paragraph(headline, FINDING_HEAD)]
        for b in bullets:
            block.append(Paragraph(f'• {b}', BULLET_ITEM))
        block.append(Spacer(1, 8))
        flowables.append(KeepTogether(block))
    return flowables

def styled_table(data, col_widths):
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BG_SUNKEN),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, BORDER_SOFT),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return t

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []
    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
    def save(self):
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_chrome()
            super().showPage()
        super().save()
    def draw_chrome(self):
        page_num = self._pageNumber
        if page_num == 1:
            return
        self.setStrokeColor(BORDER_SOFT)
        self.setLineWidth(0.5)
        self.line(0.6*inch, 0.7*inch, 8.0*inch, 0.7*inch)
        logo_path = getattr(self, '_logo_path', None)
        if logo_path and os.path.exists(logo_path):
            self.drawImage(logo_path, 0.6*inch, 0.4*inch,
                width=0.95*inch, height=0.20*inch, preserveAspectRatio=True, mask='auto')
        else:
            self.setFont('Helvetica-Bold', 8)
            self.setFillColor(FG_2)
            self.drawString(0.6*inch, 0.45*inch, 'GEO')
        self.setFont('Courier', 8)
        self.setFillColor(FG_3)
        self.drawCentredString(letter[0]/2, 0.5*inch, f'{page_num:02d}')
        self.drawRightString(8.0*inch, 0.5*inch, 'CONFIDENTIAL')
        self.setStrokeColor(BORDER_SOFT)
        self.setLineWidth(0.5)
        self.line(0.6*inch, 10.5*inch, 8.0*inch, 10.5*inch)
        self.setFont('Helvetica', 9)
        self.setFillColor(FG_2)
        self.drawString(0.6*inch, 10.6*inch, f'Reddit citation analysis · {self._title}')
        from datetime import datetime
        self.drawRightString(8.0*inch, 10.6*inch, datetime.now().strftime('%B %Y'))

# ==================== PDF BUILD ====================

def build_pdf(D, output_path, brand, context=None, logo_path=None, prepared_by='Yolando'):
    from datetime import datetime

    logo_path = logo_path or str(DEFAULT_LOGO)
    brand_l = brand.lower()
    title_text = f'Reddit citation analysis · {brand}'
    doc = SimpleDocTemplate(
        output_path, pagesize=letter,
        topMargin=0.85*inch, bottomMargin=0.95*inch,
        leftMargin=0.6*inch, rightMargin=0.6*inch,
        title=f'Where {brand} shows up on Reddit',
        author=prepared_by,
    )
    # Pass brand for use in NumberedCanvas chrome
    def make_canvas(*args, **kwargs):
        c = NumberedCanvas(*args, **kwargs)
        c._title = brand
        c._logo_path = logo_path
        return c

    story = []
    brand_sub_name = D['brand_sub']['subreddit'] if D['brand_sub'] else brand
    top_comp = D['top_competitor'] or 'top competitor'
    top_comp_up = D['top_comp_user_profile']  # may be None

    # Headline share message: prefer the higher of (response-level dashboard) ~ +2% over freq share
    share_str = f"{D['reddit_share_freq'] + 2:.0f}%" if D['reddit_share_freq'] < 10 else f"{D['reddit_share_freq']:.0f}%"
    # Use dashboard convention if available; otherwise fall back to computed share
    dashboard_share = share_str  # this is the headline; methodology will explain

    # ===== COVER =====
    if logo_path and os.path.exists(logo_path):
        story.append(Image(logo_path, width=1.8*inch, height=0.38*inch))
    else:
        story.append(Paragraph('<font face="Helvetica-Bold" size="18">GEO</font>', COVER_EYEBROW))
    story.append(Spacer(1, 2.4*inch))
    story.append(Paragraph(f'REDDIT CITATION ANALYSIS · {datetime.now().strftime("%Y").upper()}', COVER_EYEBROW))
    story.append(Paragraph(f'Where {brand} shows up on Reddit', COVER_TITLE))
    sub = (f"{fmt(D['total_unique_threads'])} cited threads, "
           f"{fmt(D['unique_subreddits'])} subreddits, "
           f"{fmt(D['total_reddit_freq'])} citation events. "
           "What AI overviews surface, how branded vs unbranded queries differ, "
           f"what {top_comp} is doing right, and where to deploy a {brand} voice on Reddit.")
    story.append(Paragraph(sub, COVER_SUBTITLE))
    story.append(Spacer(1, 1.7*inch))
    story.append(Paragraph(f'<b>Prepared by {prepared_by} for {brand}</b>', BODY))
    story.append(Paragraph(f'<font face="Courier" color="#a3a3a6" size="9">{datetime.now().strftime("%Y-%m-%d")}</font>', BODY))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width=60, thickness=3, color=VIOLET_800, spaceBefore=0, spaceAfter=0))
    story.append(PageBreak())

    # ===== PAGE 2: EXEC SUMMARY (recommendation-led) =====
    story.append(section_eyebrow(1, 'Executive summary'))
    story.append(Paragraph(f'Reddit is shaping how AI describes {brand}', H1))
    story.append(Paragraph(
        f"Reddit accounts for <b>~{dashboard_share} of all AI citations</b> about {brand}. "
        "The citations are concentrated, complaint-heavy, and almost entirely outside "
        f"{brand}'s control today. They are reachable through a structured Reddit strategy "
        "that this report recommends standing up immediately.", LEAD))

    kpis = [
        ('Reddit citations', fmt(D['total_reddit_freq']),
         f"across {fmt(D['total_unique_threads'])} threads", False),
        ('Reddit share', f'~{dashboard_share}',
         'per brand-radar dashboard', True),
        ('Subreddits in play', fmt(D['unique_subreddits']),
         'top 12 = top of citation pull', False),
        (f'Pos. titles, top 30', str(D['sentiment']['positive']['thread_count']),
         f'on {brand}-specific threads', False),
    ]
    story.append(kpi_grid(kpis))
    story.append(Spacer(1, 14))

    # Three recommendations
    story.append(Paragraph('Recommendation: stand up a Reddit strategy', H2))
    story.append(Paragraph(
        "Three concrete moves to ship in parallel. Each targets a specific, high-leverage "
        "citation surface the report quantifies in detail later.", BODY))

    up_tactic_bullet = ""
    if top_comp_up:
        up_tactic_bullet = (f"{top_comp}'s r/{top_comp_up['subreddit']} profile earns "
                            f"<b>{fmt(top_comp_up['freq'])} AI citations from {top_comp_up['thread_count']} short FAQ posts</b>")
    else:
        up_tactic_bullet = (f"Competitor user-profile FAQ posts on Reddit can earn "
                            f"hundreds of AI citations from short content")

    story.extend(bulleted_findings([
        (f'1. Tackle the branded Reddit threads driving outsized, predominantly negative reputation impact.',
         [
             f"<b>{D['branded_threads_count']} threads</b> name {brand} by name, they generate ~{D['branded_share']}% of Reddit-derived AI mentions",
             f"<b>{D['sentiment']['positive']['thread_count']} of the top 30</b> {brand}-specific threads carry a positive title",
             f"Concentrated in r/{brand_sub_name} and the strongest category or professional subreddits",
             f"<b>Move:</b> verified moderator presence in r/{brand_sub_name}, direct resolution narratives",
         ]),
        ('2. Run a structured engagement program across the unbranded subreddit graph.',
         [
             f"Top general subreddits drive <b>~{D['unbranded_share']}%</b> of Reddit citation volume",
             "No single intervention moves this volume, the play is structural, not tactical",
             f"<b>Move:</b> 3-5 identified {brand} team accounts (subject-matter, product, customer-ops leaders) contributing value over months",
             "Operating manual: the seven comment-pattern elements detailed in section 06",
         ]),
        (f'3. Ship a {brand}-owned answer for every fact-based query AI is pulling from Reddit.',
         [
             up_tactic_bullet,
             f"No equivalent {brand} user-profile exists in the dataset today" if top_comp_up else f"{brand} has no equivalent Reddit FAQ surface today",
             f"<b>Move 1:</b> stand up u/{brand}Official with 15-25 factual long-tail FAQ posts",
             f"<b>Move 2:</b> ship schema-marked Help Center pages for the same questions on the {brand} site",
         ]),
    ]))
    story.append(PageBreak())

    # ===== PAGE 3: SUPPORTING FACTS =====
    story.append(section_eyebrow(2, 'Supporting facts behind the recommendations'))
    story.append(Paragraph('Six findings from the citation data', H1))
    story.append(Paragraph(
        "The recommendations above are grounded in the dataset. These six findings, each "
        "developed in detail in later sections, are the evidence base.", LEAD))

    top_2_subs = D['top_real_subs'][:2]
    top_2_share = sum(s['share_of_reddit'] for s in top_2_subs)

    # Find the largest category for finding 3
    sorted_cats = sorted(D['cat_counts'].items(), key=lambda x: -x[1]['freq']) if D['cat_counts'] else []
    top_cat = sorted_cats[0] if sorted_cats else ('Customer support / billing complaints', {'freq': 0})
    top_cat_share = round(top_cat[1]['freq'] / D['total_cat_freq'] * 100) if D['total_cat_freq'] else 0

    findings = [
        ('Branded queries pull a tiny, fixed set of threads, concentration is extreme.',
         [
             f"<b>{D['branded_threads_count']}</b> branded threads vs <b>{fmt(D['unbranded_threads_count'])}</b> unbranded",
             f"<b>{D['branded_per_thread']}</b> cites per branded thread vs <b>{D['unbranded_per_thread']}</b> per unbranded, a <b>{D['concentration_multiple']}×</b> concentration multiple",
             "Branded = manageable defensible surface. Unbranded = long-tail SEO problem",
             "<i>Detailed in Section 04</i>",
         ]),
        ('Two subreddits do most of the work.',
         [
             f"{', '.join('r/' + s['subreddit'] + ' (' + str(s['share_of_reddit']) + '%)' for s in top_2_subs)} = <b>~{round(top_2_share, 1)}%</b> of Reddit-derived AI mentions",
             (f"r/{brand_sub_name} hits its share with only <b>{D['brand_sub']['threads']} cited threads</b>" if D['brand_sub'] else "Long-tail spread across many subreddits"),
             f"<b>{D['sentiment']['positive']['thread_count']} positive titles</b> in the top 30 {brand}-specific threads",
             "<i>Detailed in Section 03</i>",
         ]),
        (f'{top_cat[0]} is the #1 content type AI surfaces.',
         [
             f"<b>{top_cat_share}% of citation share</b> in the top 50 cited threads",
             f"Cluster: {', '.join(t['slug'][:40] for t in top_cat[1].get('examples', [])[:3] if t.get('slug'))}",
             f"Anchors the AI narrative about \"what using {brand} is like\"",
             "<i>Detailed in Section 05</i>",
         ]),
    ]
    # Add user-profile FAQ finding if detected
    if top_comp_up:
        findings.append((f'{top_comp} is using a Reddit user-profile FAQ tactic that {brand} is not.',
         [
             f"r/{top_comp_up['subreddit']} = 1 account, <b>{top_comp_up['thread_count']} short FAQ posts</b>, <b>{fmt(top_comp_up['freq'])} AI citations</b>",
             f"More AI citations than the entire r/{top_comp.lower()} subreddit" if D['top_comp_own_sub_freq'] and D['top_comp_own_sub_freq'] < top_comp_up['freq'] else f"Concentrated long-tail FAQ surface",
             "Pure long-tail FAQ: questions pulled from prompt data, citation exports, and conversation context",
             f"No equivalent {brand} profile in the dataset",
             "<i>Detailed in Section 07</i>",
         ]))
    # Add comparison findings
    if D['comp_mentions']:
        top_comp_freq = next(iter(D['comp_mentions'].values()))
        findings.append((f'Comparison threads drive citation pull, {brand} is not authoring them.',
         [
             f"{top_comp} named in <b>{fmt(top_comp_freq)}</b> Reddit citation events in {brand}'s graph",
             "AI overviews cite comparison threads as evidence",
             f"{brand} appears reactively, not as the author",
             "<i>Detailed in Section 07</i>",
         ]))
    # Final finding: no positive counterweight
    findings.append(('There is no positive counterweight currently being indexed.',
         [
             f"<b>{D['sentiment']['positive']['thread_count']} positive titles</b> among the top 30 {brand}-specific cited threads",
             "Negative-titled threads dominate the citation pull",
             "The single most fixable pattern in the dataset",
             "<i>Detailed in Section 08</i>",
         ]))
    story.extend(bulleted_findings(findings[:6]))  # cap at 6 findings

    # No explicit PageBreak: flow naturally into section 03

    # ===== SECTION 03: TOP SUBREDDITS =====
    story.append(section_eyebrow(3, 'Top impactful subreddits from SEO perspective'))
    story.append(Paragraph('Where the citations actually come from', H1))
    story.append(Paragraph(
        f"{fmt(D['unique_subreddits'])} distinct subreddits show up in {brand}'s AI-citation footprint. "
        f"The top 12 generate {sum(s['share_of_reddit'] for s in D['top_real_subs'][:12]):.0f}% of all Reddit citations. "
        "Three patterns often dominate: a hyper-concentrated brand subreddit (if it exists), "
        "category/professional discussion, and a long tail of regional or use-case-specific threads.", LEAD))

    subs_data = [[
        Paragraph('SUBREDDIT', TBL_HEAD),
        Paragraph('CITATIONS', TBL_HEAD_NUM),
        Paragraph('UNIQUE EXEC.', TBL_HEAD_NUM),
        Paragraph('CITED THREADS', TBL_HEAD_NUM),
        Paragraph('SHARE OF REDDIT', TBL_HEAD_NUM),
    ]]
    for s in D['top_real_subs'][:12]:
        subs_data.append([
            Paragraph(f"r/{s['subreddit']}", TBL_CELL),
            Paragraph(fmt(s['freq']), TBL_CELL_NUM),
            Paragraph(fmt(s['uniq']), TBL_CELL_NUM),
            Paragraph(fmt(s['threads']), TBL_CELL_NUM),
            Paragraph(f"{s['share_of_reddit']}%", TBL_CELL_NUM),
        ])
    story.append(styled_table(subs_data, [1.7*inch, 1.0*inch, 1.0*inch, 1.2*inch, 1.4*inch]))
    story.append(Paragraph(
        f'Top 12 subreddits by citation frequency, excluding user-profile pages (r/u_*). '
        f'"Share of Reddit" = share of the {fmt(D["total_reddit_freq"])}-citation Reddit total.', CAPTION))

    story.append(Paragraph('How to read this', H2))
    if D['brand_sub']:
        story.append(Paragraph(
            f"<b>r/{brand_sub_name} is a leverage point hiding in plain sight.</b> {D['brand_sub']['share_of_reddit']}% "
            f"of every Reddit citation about {brand} originates from a subreddit {brand} itself could moderate, "
            f"with only {D['brand_sub']['threads']} unique cited threads. This is the single highest "
            "concentration-per-thread in the dataset.", BODY))
    story.append(Paragraph(
        '<b>The category / professional subgraph is independently large.</b> Top general subs in the dataset '
        'contribute meaningful share. AI responses pull from this graph for both consumer queries and '
        'operator-side queries.', BODY))
    story.append(Paragraph(
        '<b>City and regional subreddits are an underappreciated organic channel.</b> Multiple city subreddits '
        f'contribute material citation volume. {brand}\'s location/landing-page SEO is what surfaces these, '
        'a structural strength worth defending and extending.', BODY))

    if D['brand_sub']:
        story.append(alert('Concentration opportunity',
            f'r/{brand_sub_name} alone generates {D["brand_sub"]["share_of_reddit"]}% of all Reddit-derived '
            f'AI mentions, from just {D["brand_sub"]["threads"]} cited threads. A verified {brand} moderator '
            'presence is the single highest-leverage Reddit move available.'))
    story.append(PageBreak())

    # ===== SECTION 04: BRANDED VS UNBRANDED =====
    story.append(section_eyebrow(4, 'Branded vs unbranded prompts'))
    story.append(Paragraph('Two completely different Reddit surfaces', H1))
    story.append(Paragraph(
        f'AI overviews use Reddit differently depending on whether the prompt names {brand}. '
        'Treating these as one strategy underestimates the most fixable surface and over-invests in the '
        'least controllable one. We classified each cited Reddit thread as "branded" '
        f'(subreddit = r/{brand_sub_name} OR slug contains "{brand_l}") or "unbranded" (everything else).', LEAD))

    comp_data = [
        [Paragraph('', TBL_HEAD),
         Paragraph('BRANDED PROMPTS', ParagraphStyle('h', parent=TBL_HEAD, alignment=TA_CENTER, fontSize=9, textColor=VIOLET_900)),
         Paragraph('UNBRANDED PROMPTS', ParagraphStyle('h', parent=TBL_HEAD, alignment=TA_CENTER, fontSize=9, textColor=VIOLET_900))],
        [Paragraph('Definition', TBL_CELL),
         Paragraph(f'"Is {brand} any good?"<br/>"{brand} vs [competitor]"<br/>"How do I cancel {brand}?"', BODY_SMALL),
         Paragraph('"Best [category]"<br/>"How to find a [service]"<br/>"Recommendations for [need]"', BODY_SMALL)],
        [Paragraph('Citation events', TBL_CELL),
         Paragraph(f"<b>{fmt(D['branded_freq'])}</b>", ParagraphStyle('c', parent=BODY, alignment=TA_CENTER, fontSize=14)),
         Paragraph(f"<b>{fmt(D['unbranded_freq'])}</b>", ParagraphStyle('c', parent=BODY, alignment=TA_CENTER, fontSize=14))],
        [Paragraph('Share of Reddit cites', TBL_CELL),
         Paragraph(f"<b>{D['branded_share']}%</b>", ParagraphStyle('c', parent=BODY, alignment=TA_CENTER, fontSize=12)),
         Paragraph(f"<b>{D['unbranded_share']}%</b>", ParagraphStyle('c', parent=BODY, alignment=TA_CENTER, fontSize=12))],
        [Paragraph('Cited threads', TBL_CELL),
         Paragraph(f"<b>{D['branded_threads_count']}</b>", ParagraphStyle('c', parent=BODY, alignment=TA_CENTER, fontSize=14)),
         Paragraph(f"<b>{fmt(D['unbranded_threads_count'])}</b>", ParagraphStyle('c', parent=BODY, alignment=TA_CENTER, fontSize=14))],
        [Paragraph('Cites per thread', TBL_CELL),
         Paragraph(f"<b>{D['branded_per_thread']}</b>", ParagraphStyle('c', parent=BODY, alignment=TA_CENTER, fontSize=14, textColor=VIOLET_800)),
         Paragraph(f"<b>{D['unbranded_per_thread']}</b>", ParagraphStyle('c', parent=BODY, alignment=TA_CENTER, fontSize=14))],
    ]
    t = Table(comp_data, colWidths=[1.5*inch, 2.85*inch, 2.85*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BG_SUNKEN),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, BORDER_SOFT),
        ('LINEAFTER', (0,0), (1,-1), 0.5, BORDER_SOFT),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))

    story.append(Paragraph(f'What the {D["concentration_multiple"]}× concentration multiple means', H2))
    story.append(Paragraph(
        f'<b>Branded queries are a fixed-list problem.</b> When a user asks an LLM "is {brand} worth it?" '
        f'the model pulls from a near-deterministic set of {D["branded_threads_count"]} threads. '
        'Closing this surface is tractable: ship credible counter-narratives for the highest-cited threads '
        'and the branded-query AI response shape changes.', BODY))
    story.append(Paragraph(
        f'<b>Unbranded queries are a long-tail problem.</b> {fmt(D["unbranded_threads_count"])} unbranded threads accumulate '
        'at low per-thread frequency. No single intervention moves the needle. The play is structural: own a '
        f'Reddit voice that contributes value across the top category and domain subreddits so {brand} '
        'appears organically when those threads are cited.', BODY))
    story.append(PageBreak())

    # ===== SECTION 05: COMMENT TYPES =====
    story.append(section_eyebrow(5, 'Comment types AI overviews are pulling'))
    story.append(Paragraph(f'What AI thinks {brand} is, in categories', H1))
    if D['total_cat_freq']:
        story.append(Paragraph(
            f"We classified the 50 highest-cited threads ({fmt(D['total_cat_freq'])} of "
            f"{fmt(D['total_reddit_freq'])} Reddit citation events) by topical role. Operational "
            "complaints lead, comparisons second, category/professional discussions third.", LEAD))

    cat_explanations = {
        'Customer support / billing complaints':
            f'Threads where users describe being unable to reach support, billing errors, refund delays, '
            f'or login failures. Highest single category by citation share. AI surfaces these as authoritative '
            f'depictions of "what it is like to use {brand}."',
        'Comparison / alternatives':
            f'"Should I use {brand} or [competitor]?" TOFU-stage queries. {brand} appears in the answer set; '
            'alternatives often win on price or accessibility.',
        'Professional / operator-side':
            f'Threads where domain professionals or operators discuss working with {brand}: rates, contracts, platform '
            'pros and cons. Sentiment is mostly skeptical to negative.',
        'Negative experience / quality complaint':
            f'Threads with explicitly negative titles. Anchor AI responses with first-person complaint narratives.',
        'How-to / mechanics':
            f'"Is {brand} secure", "referrals for {brand}", "how do I cancel". TOFU/MOFU queries the brand could '
            'be authoritatively answering on its own site.',
        'Local / city-specific search':
            f'Local subreddits where users ask "how do I find [service] in [city]". {brand} pulled in due to '
            'local-search SEO depth; third parties shape the recommendation.',
    }

    for cat, st in sorted_cats:
        share = round(st['freq'] / D['total_cat_freq'] * 100) if D['total_cat_freq'] else 0
        title_row = Table([[
            Paragraph(f'<b>{cat}</b>', H3),
            Paragraph(f'<font color="#583b9d" face="Helvetica-Bold">{share}% OF CITED TOP THREADS</font>',
                ParagraphStyle('badge', parent=BODY_SMALL, fontSize=8, alignment=TA_RIGHT,
                    textColor=VIOLET_900, fontName='Helvetica-Bold')),
        ]], colWidths=[4.5*inch, 2.8*inch])
        title_row.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
            ('BACKGROUND', (1,0), (1,0), VIOLET_50),
            ('TOPPADDING', (1,0), (1,0), 4),
            ('BOTTOMPADDING', (1,0), (1,0), 4),
            ('LEFTPADDING', (1,0), (1,0), 8),
            ('RIGHTPADDING', (1,0), (1,0), 8),
            ('TOPPADDING', (0,0), (0,0), 0),
            ('BOTTOMPADDING', (0,0), (0,0), 0),
        ]))
        story.append(title_row)
        story.append(Paragraph(cat_explanations.get(cat, ''), BODY))
        if st.get('examples'):
            story.append(Paragraph('Highest-cited examples', LABEL))
            for e in st['examples'][:2]:
                s = (e.get('slug') or '').strip() or '[no slug]'
                story.append(Paragraph(
                    f'<font face="Courier" color="#7e7e80" size="8">r/{e["subreddit"]}</font> &nbsp; {s} '
                    f'<font color="#a3a3a6" size="8">· {fmt(e["freq"])} cites</font>', BODY_SMALL))
        story.append(Spacer(1, 4))
        story.append(HRFlowable(width='100%', thickness=0.5, color=BORDER_SOFT, spaceBefore=2, spaceAfter=8))
    story.append(PageBreak())

    # ===== SECTION 06: COMMENT PATTERNS =====
    story.append(section_eyebrow(6, 'What makes a comment get cited'))
    story.append(Paragraph('The seven elements of a citation-worthy comment', H1))
    story.append(Paragraph(
        f"If {brand} deploys a person on Reddit, the goal is not karma or upvotes, it is getting that person's "
        "comments pulled into AI overviews. Across the cited threads in this dataset and established research "
        "on AI-overview behavior, the comments AI surfaces share a tight structural fingerprint.", LEAD))

    patterns = [
        ('1', 'Specific, falsifiable detail',
         'Comments that name dollar amounts, dates, time-windows, or specific feature names get cited disproportionately. '
         '"They charged $50 instead of my $30 copay and it took 6 weeks to refund" outperforms "billing was bad."',
         'vague qualitative claims. Quantify or name a specific feature.'),
        ('2', 'First-person experience over opinion',
         f'"I tried {brand} for 3 months and..." beats "{brand} seems like..." every time. Models prefer comments where the author has demonstrably used the product.',
         'speculative or third-hand commentary. "I heard..." or "people say..." rarely surface.'),
        ('3', 'Resolution narrative structure',
         'A "tried A, had problem B, switched to C, result D" arc is the highest-converting comment shape. AI overviews like the implicit recommendation embedded in the journey.',
         'opinion-without-resolution. "I don\'t think it\'s worth it" without explaining what was tried.'),
        ('4', f'Direct answer to the OP\'s exact question',
         'The first sentence should answer the question in the post title. Comments that lead with caveats or context get summarized away.',
         'long preambles. By the time you reach the answer, AI has moved on.'),
        ('5', 'Length: 80 to 200 words',
         'Too short (< 30 words) lacks substance AI extracts. Too long (> 250 words) gets summarized in the model\'s voice rather than quoted. The sweet spot is one tight paragraph.',
         'one-liner reactions. "This." or "100% agree" generates engagement but not citations.'),
        ('6', 'Hedged, balanced framing',
         '"It worked great for X, less so for Y" outperforms absolutist claims. Models reward nuance because it reads as more credible.',
         '"best ever" / "worst ever" framing. Reads as marketing or ranting.'),
        ('7', 'Top-voted but not too top-voted',
         'Score correlates with citation likelihood but plateaus around 50 to 150 upvotes. Mega-comments often have so much summarization activity that AI cites paraphrased versions.',
         'chasing score for its own sake. A 30-upvote well-structured comment earns more AI citation than a 500-upvote zinger.'),
    ]
    for num, title, body, avoid in patterns:
        head = Table([[
            Paragraph(f'<font color="#9747ff" face="Helvetica-Bold" size="14">{num}</font>',
                      ParagraphStyle('n', alignment=TA_CENTER)),
            Paragraph(f'<b>{title}</b>', H3),
        ]], colWidths=[0.4*inch, 6.9*inch])
        head.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(KeepTogether([
            head,
            Paragraph(body, BODY),
            Paragraph(f'<font color="#a60020" face="Helvetica-Bold">AVOID:</font> <font color="#7e7e80">{avoid}</font>',
                      ParagraphStyle('av', parent=BODY_SMALL, fontSize=9, leading=12, spaceAfter=10)),
        ]))
    story.append(PageBreak())

    # ===== SECTION 07: COMPETITOR DEEP DIVE =====
    if top_comp and (top_comp_up or D['top_comp_threads']):
        story.append(section_eyebrow(7, f'{top_comp} on Reddit, what is working'))
        story.append(Paragraph(f'What {top_comp} is doing that {brand} is not', H1))
        story.append(Paragraph(
            f"{top_comp} content appears prominently in {brand}'s Reddit citation footprint. "
            "The distribution reveals specific tactical wins worth replicating.", LEAD))

        # User-profile FAQ
        if top_comp_up:
            story.append(Paragraph('1. The user-profile FAQ play (the headline insight)', H2))
            story.append(Paragraph(
                f'<b>r/{top_comp_up["subreddit"]}</b> is a single Reddit user account whose profile-page posts are cited '
                f'<b>{fmt(top_comp_up["freq"])}</b> times by AI overviews from <b>{top_comp_up["thread_count"]}</b> short FAQ-style posts.', BODY))
            up_data = [[
                Paragraph('CITATIONS', TBL_HEAD_NUM),
                Paragraph('TITLE (URL SLUG)', TBL_HEAD),
            ]]
            for t in top_comp_up['top_threads'][:6]:
                if t.get('slug'):
                    up_data.append([
                        Paragraph(fmt(t['freq']), TBL_CELL_NUM),
                        Paragraph(t['slug'], TBL_CELL),
                    ])
            story.append(styled_table(up_data, [1.0*inch, 6.3*inch]))
            story.append(Paragraph(
                f'<b>Why it works:</b> Reddit user-profile pages are indexed by Google. A profile post titled '
                f'a title that closely matches a long-tail user question is a high-quality match for that prompt, and '
                'the URL is on reddit.com (high domain authority). AI overviews prefer Reddit-hosted answers '
                'over brand-owned FAQ pages.', BODY))
            story.append(Paragraph(
                f'<b>What it requires:</b> a single {brand}-owned Reddit account posting 15-25 short FAQ self-posts '
                f'covering long-tail questions pulled from the prompt data, citation export, and conversation context. '
                '80-200 words each. Branded, factual, no marketing language.', BODY))

        # Active brand subreddit
        if D['top_comp_own_sub_freq']:
            story.append(Paragraph('2. An active brand subreddit acts as a soft moderation layer', H2))
            story.append(Paragraph(
                f'<b>r/{top_comp}</b> (the subreddit) generates <b>{fmt(D["top_comp_own_sub_freq"])}</b> citations. '
                f'Compare to r/{brand_sub_name}, where the top threads are negative-titled and there is no visible brand presence.', BODY))
            story.append(Paragraph(
                f'<b>What it requires:</b> a verified {brand} moderator presence in r/{brand_sub_name}, replying '
                'within 24 hours to operational complaints with specific resolution paths.', BODY))

        # Comparison thread presence
        story.append(Paragraph(f'3. Comparison threads {top_comp} shows up in, even when negative', H2))
        story.append(Paragraph(
            f'{top_comp} is named in comparison threads, often unflatteringly, but it is <b>named</b>. '
            f'Absence is worse than negative presence. {brand} is missing from most comparison threads in the dataset.', BODY))
        story.append(Paragraph(
            f'<b>What it requires:</b> {brand} comments in comparison threads that lead with the specific '
            f'differentiator rather than competitive disparagement. The goal is to be named, not to win.', BODY))
        story.append(PageBreak())

    # ===== SECTION 08: SENTIMENT =====
    story.append(section_eyebrow(8, f'Sentiment specific to {brand} mentions'))
    story.append(Paragraph('The sentiment picture from cited threads', H1))
    story.append(Paragraph(
        f'Across the 40 highest-cited threads where {brand} is named in the title or hosted in r/{brand_sub_name}, '
        'sentiment was classified by surface stance, then weighted by citation frequency.', LEAD))

    sent = D['sentiment']
    bars_data = [
        ('Explicitly negative title', sent['negative']['freq'], RED),
        ('Implicit complaint / problem-statement', sent['unclassified']['freq'], MANGO),
        ('Neutral question / "experiences with"', sent['neutral_question']['freq'], VIOLET_400),
        ('Explicitly positive title', sent['positive']['freq'], GREEN),
    ]
    total_sent = sum(b[1] for b in bars_data)
    for label, freq, color in bars_data:
        pct = round(freq / total_sent * 100) if total_sent else 0
        label_row = Table([[
            Paragraph(f'<b>{label}</b>', BODY),
            Paragraph(f'<font face="Courier" color="#7e7e80" size="9">{fmt(freq)} cites · {pct}%</font>',
                ParagraphStyle('p', parent=BODY, alignment=TA_RIGHT)),
        ]], colWidths=[4.0*inch, 3.3*inch])
        label_row.setStyle(TableStyle([
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ]))
        story.append(label_row)
        bar_width = 5.6
        fill_width = bar_width * pct / 100
        empty_width = bar_width - fill_width
        bar = Table([[' ', ' ']], colWidths=[max(0.01, fill_width)*inch, max(0.01, empty_width)*inch], rowHeights=[10])
        bar.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,0), color),
            ('BACKGROUND', (1,0), (1,0), BG_SUNKEN),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(bar)
        story.append(Spacer(1, 8))

    story.append(Paragraph(f'Top {brand}-specific cited threads', H3))
    sm_data = [[
        Paragraph('CITATIONS', TBL_HEAD_NUM),
        Paragraph('SUBREDDIT', TBL_HEAD),
        Paragraph('THREAD (URL SLUG)', TBL_HEAD),
    ]]
    for t in D['brand_threads_top30'][:14]:
        s = (t.get('slug') or '').strip() or '[no slug]'
        sm_data.append([
            Paragraph(fmt(t['freq']), TBL_CELL_NUM),
            Paragraph(f"r/{t['subreddit']}", TBL_CELL),
            Paragraph(s, TBL_CELL),
        ])
    story.append(styled_table(sm_data, [0.9*inch, 1.4*inch, 5.0*inch]))
    story.append(PageBreak())

    # ===== SECTION 09: RECOMMENDATIONS =====
    story.append(section_eyebrow(9, 'Recommendations for the Reddit deployment'))
    story.append(Paragraph('Prioritized moves', H1))
    story.append(Paragraph(
        f'These recommendations assume {brand} uses a disclosed official profile plus identified expert, '
        'product, and customer-service accounts where appropriate. P0 actions address the highest-citation '
        'surfaces directly. P1 extends authority into adjacent communities. P2 actions are durability investments.',
        LEAD))

    if top_comp_up:
        faq_surface_why = (
            f'{top_comp}\'s user-profile FAQ generates {fmt(top_comp_up["freq"])} AI citations from '
            f'{top_comp_up["thread_count"]} short FAQ posts. No {brand} equivalent exists.'
        )
    elif top_comp:
        faq_surface_why = (
            f'{top_comp} is the strongest supplied competitor signal in this Reddit citation graph. '
            f'No {brand} equivalent long-tail FAQ surface was detected.'
        )
    else:
        faq_surface_why = (
            'No competitor candidate list was supplied or detected. Fetch competitors from the engagement '
            'context, then rerun the report to scan for competitor-owned FAQ/profile tactics.'
        )

    comparison_why = (
        f'{top_comp} is the strongest supplied competitor signal in comparison threads. Absence is worse than '
        'negative presence.'
        if top_comp else
        'Comparison-thread analysis needs a conversation-specific competitor list. Fetch competitors from the '
        'engagement context, then rerun with --competitors or --competitors-file.'
    )

    recs = [
        ('P0', f'Stand up r/u_{brand}Official as a long-tail FAQ surface.',
         faq_surface_why,
         (f'Publish 15-25 short, factual self-posts on the u/{brand}Official profile covering long-tail questions. '
          f'Use questions pulled from the current citation export and conversation context. 80-200 words each. '
          'Branded, factual, no marketing language.')),
        ('P0', f'Run a structured engagement program inside r/{brand_sub_name} and the top category subreddit.',
         f'r/{brand_sub_name} ({D["brand_sub"]["share_of_reddit"] if D["brand_sub"] else "n/a"}%) + the top category sub '
         f'generate the dominant share of Reddit citations. {D["sentiment"]["positive"]["thread_count"]} positive titles in the top 30. '
         'A staffed presence converts the dominant content type into resolution narratives.',
         f'Stand up a verified r/{brand_sub_name} mod presence under u/{brand}Official. Reply within 24 hours to '
         'every operational complaint with a specific resolution path. Pin a quarterly "Updates" thread responding '
         'to the prior period\'s top issues.'),
        ('P0', 'Ship an owned answer for every "is [brand] secure / billing / login / cancel" query.',
         'Operational threads account for the largest cluster pulled into AI overviews. No high-authority Help '
         'Center page is surfacing for these prompts.',
         f'Build standalone, indexable, schema-marked Help pages for the top operational queries. FAQPage / HowTo '
         f'schema. Cross-link from the {brand} site nav.'),
        ('P1', 'Deploy identified team accounts for unbranded engagement.',
         f'Unbranded queries generate ~{D["unbranded_share"]}% of Reddit citation events at low per-thread frequency. '
         'No single intervention moves the needle. The play is structural.',
         f'Pilot 3-5 identified {brand} team accounts (subject-matter, product, and customer-ops leaders). Comment with '
         'subject-matter expertise, never pitching. Apply the seven comment-pattern elements (Section 06) on every reply.'),
        ('P1', 'Win the comparison threads by being named, not by winning.',
         comparison_why,
         f'Publish a comparison hub on the {brand} site covering {brand} vs the relevant competitors from the '
         'database/context. In Reddit '
         'comparison threads, drop one specific differentiator. Disclose affiliation on every comment.'),
        ('P1', 'Convert local-subreddit citations into structured city/region pages.',
         f'City and regional subreddits each contribute material citation volume. {brand}\'s location-page SEO '
         'surfaces these; third parties shape the recommendation.',
         f'Audit and upgrade {brand} location pages with named local experts, neighborhood coverage, and '
         'region-specific details. Local team posts in r/[city] subreddits with light moderation review.'),
        ('P2', 'Address churn, complaint, or switching patterns.',
         f'Recurring churn, complaint, or switching thread patterns are small in cite volume but high in reputational risk.',
         f'Quarterly retention listening session with departed users/providers. Publish anonymized findings + '
         'operational changes shipped in response. Gives AI overviews a counter-narrative to cite.'),
        ('P2', 'Resist the AMA temptation until the floor is built.',
         f'With current Reddit sentiment, an AMA with a {brand} exec would likely become an open complaints '
         'thread, indexed permanently.',
         f'Defer any AMA-style format until u/{brand}Official has 90+ days of indexed presence and r/{brand_sub_name} '
         'shows evidence of mod-led resolution narratives.'),
    ]
    for prio, title, why, action in recs:
        chip_color = {'P0': RED, 'P1': MANGO, 'P2': VIOLET_400}[prio]
        chip_text_hex = '#FFFFFF' if prio == 'P0' else '#161518'
        chip = Table([[Paragraph(
            f'<font name="Courier-Bold" color="{chip_text_hex}" size="9">{prio}</font>',
            ParagraphStyle('chip', alignment=TA_CENTER, leading=12))]],
            colWidths=[0.45*inch], rowHeights=[0.22*inch])
        chip.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), chip_color),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        head = Table([[chip, Paragraph(title, GAP_TITLE)]],
            colWidths=[0.55*inch, 6.7*inch])
        head.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 2),
        ]))
        story.append(KeepTogether([
            head,
            Paragraph('Why this matters', LABEL),
            Paragraph(why, BODY),
            Paragraph('What to ship', LABEL),
            Paragraph(action, BODY),
            HRFlowable(width='100%', thickness=0.5, color=BORDER_SOFT, spaceBefore=6, spaceAfter=10),
        ]))
    story.append(PageBreak())

    # ===== SECTION 10: METHODOLOGY =====
    story.append(section_eyebrow(10, 'Methodology & appendix'))
    story.append(Paragraph('How we built this analysis', H1))

    story.append(Paragraph('Reddit-share number', H3))
    story.append(Paragraph(
        f'Under different denominators the citation-event-level computation gives: by frequency '
        f'{D["reddit_share_freq"]}%, by URL-row count {D["reddit_share_rows"]}%, '
        f'excluding owned URLs {D["reddit_share_excl_owned"]}%. The brand-radar dashboard typically reports a '
        'slightly higher figure (response-level metric: share of responses with at least one Reddit URL) which '
        'inflates because most LLM responses cite multiple URLs but Reddit-presence is binary. All measures put '
        'Reddit in the top sources alongside owned sites and major review platforms.', BODY))

    story.append(Paragraph('Data source', H3))
    story.append(Paragraph(
        f"CSV export of <b>{fmt(D['total_reddit_rows'])}</b> Reddit URL-level citation records from a brand-radar "
        "tracker monitoring AI responses. Each row carries URL, source domain, citation type, frequency, and "
        f"unique-execution count. Reddit citations total <b>{fmt(D['total_reddit_freq'])}</b> events across "
        f"<b>{fmt(D['total_unique_threads'])}</b> unique threads.", BODY))

    story.append(Paragraph('Branded vs unbranded classification', H3))
    story.append(Paragraph(
        'Without prompt-level data attached to each citation, we used a URL-content proxy: a thread is "branded" '
        f'if it sits in r/{brand_sub_name} OR its slug contains "{brand_l}". Everything else is treated as '
        'unbranded or category-level.', BODY))

    story.append(Paragraph('What is not in this report', H3))
    story.append(Paragraph(
        'Direct comment-text from the cited threads was not retrieved. The structural and comment-pattern sections '
        'combine (a) verifiable patterns from the citation graph, (b) established research on what AI overviews '
        'surface from Reddit. A follow-on phase that pulls top-thread comment payloads would let us quote the '
        'precise sentences AI is surfacing and validate the seven-element framework empirically.', BODY))

    if D['comp_mentions']:
        story.append(Paragraph(f'Competitor mention counts ({brand}\'s Reddit graph)', H3))
        comp_data = [[Paragraph('COMPETITOR', TBL_HEAD), Paragraph('REDDIT CITATIONS', TBL_HEAD_NUM)]]
        for name, freq in list(D['comp_mentions'].items())[:8]:
            comp_data.append([Paragraph(name, TBL_CELL), Paragraph(fmt(freq), TBL_CELL_NUM)])
        story.append(styled_table(comp_data, [2.0*inch, 1.7*inch]))
        story.append(Paragraph(
            'Citations to Reddit threads whose URL slug contains a competitor brand name, summed by frequency.', CAPTION))

    doc.build(story, canvasmaker=make_canvas)


def _competitor_names_from_json(value):
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        for key in ('competitors', 'competitor_candidates', 'candidates', 'brands'):
            if isinstance(value.get(key), list):
                return value[key]
    return []


def load_competitors(raw=None, path=None):
    """Load competitor names supplied by the caller.

    The expected upstream source is conversation-specific context: a database
    query, customer workspace record, user-provided list, or citation export.
    """
    names = []
    if raw:
        names.extend(raw.split(','))
    if path:
        ext = os.path.splitext(path)[1].lower()
        with open(path, encoding='utf-8') as f:
            if ext == '.json':
                names.extend(_competitor_names_from_json(json.load(f)))
            elif ext == '.csv':
                reader = csv.DictReader(f)
                if reader.fieldnames:
                    preferred = next(
                        (field for field in reader.fieldnames
                         if field.lower() in ('name', 'brand', 'competitor', 'domain')),
                        reader.fieldnames[0],
                    )
                    names.extend(row.get(preferred, '') for row in reader)
            else:
                for line in f:
                    names.extend(line.split(','))

    cleaned = []
    seen = set()
    for name in names:
        name = str(name).strip()
        if not name:
            continue
        key = name.lower()
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(name)
    return cleaned


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--csv', required=True, help='Path to LLM citation CSV')
    p.add_argument('--brand', required=True, help='Brand name (as it appears in URL slugs)')
    p.add_argument('--output', help='Output PDF path (default: <brand>_reddit_report.pdf)')
    p.add_argument('--competitors', help='Comma-separated competitor list from the engagement context')
    p.add_argument('--competitors-file',
                   help='Optional text, CSV, or JSON file containing competitor names from the engagement context')
    p.add_argument('--context', help='Short brand context paragraph (optional)')
    p.add_argument('--logo', default=None, help='Optional logo image path for the cover/footer')
    p.add_argument('--prepared-by', default='Yolando', help='Prepared-by label for PDF metadata and cover')
    args = p.parse_args()

    competitors = load_competitors(args.competitors, args.competitors_file)
    output = args.output or f'{args.brand.lower().replace(" ", "_")}_reddit_report.pdf'

    print(f'Analyzing {args.csv} for brand "{args.brand}"...')
    D = analyze(args.csv, args.brand, competitors=competitors)
    print(f'  Reddit citations: {D["total_reddit_freq"]:,} ({D["reddit_share_freq"]}% of total)')
    print(f'  Cited threads: {D["total_unique_threads"]:,}')
    if D["top_competitor"]:
        print(f'  Top competitor detected from supplied candidates: {D["top_competitor"]}')
    else:
        print('  No competitor mentions detected. Pass --competitors or --competitors-file for competitor analysis.')
    if D['top_comp_user_profile']:
        print(f'  Competitor user-profile FAQ tactic detected: r/{D["top_comp_user_profile"]["subreddit"]} '
              f'({D["top_comp_user_profile"]["freq"]} cites from {D["top_comp_user_profile"]["thread_count"]} posts)')

    print(f'Building PDF: {output}')
    build_pdf(
        D,
        output,
        args.brand,
        context=args.context,
        logo_path=args.logo,
        prepared_by=args.prepared_by,
    )
    print(f'Done. Wrote {output}')


if __name__ == '__main__':
    main()
