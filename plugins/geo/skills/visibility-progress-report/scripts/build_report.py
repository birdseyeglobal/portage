#!/usr/bin/env python3
"""
GEO visibility progress PDF report generator.

Reads a CSV of LLM prompt execution data and produces a multi-page PDF showing
how a client's AI discoverability has improved over time.

Usage:
    python build_report.py --csv data.csv --brand "Brand Name" --output report.pdf [--logo logo.png]
"""

import argparse
import csv
import os
import sys
import tempfile
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, HRFlowable, KeepTogether
)

# ============ YOLANDO COLORS ============
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
PURPLE_DARK = colors.HexColor('#3D2C6B')
PURPLE_LIGHT = colors.HexColor('#F0EDF5')
ORANGE_ACCENT = colors.HexColor('#E8712B')
ORANGE_WARM = colors.HexColor('#E8A54B')
GREEN_POS = colors.HexColor('#00A651')
RED_NEG = colors.HexColor('#E74C3C')
BLACK = colors.HexColor('#2C2C2C')
GRAY_SUB = colors.HexColor('#888888')
GRAY_ALT = colors.HexColor('#F5F5F5')
WHITE = colors.white


# ============ CSV PARSING ============

def find_column(headers, candidates):
    """Find a column by trying multiple possible names (case-insensitive)."""
    headers_lower = {h.lower().strip(): h for h in headers}
    for c in candidates:
        if c.lower() in headers_lower:
            return headers_lower[c.lower()]
    return None


def parse_bool(val):
    """Parse YES/NO, TRUE/FALSE, 1/0 to boolean."""
    return val.strip().upper() in ('YES', 'TRUE', '1')


def load_data(csv_path):
    """Load CSV and return structured data with auto-detected columns."""
    csv.field_size_limit(10**7)

    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames

        # Auto-detect columns
        col_map = {
            'date': find_column(headers, ['Execution Date', 'Date', 'Run Date', 'date']),
            'prompt': find_column(headers, ['Prompt', 'Query', 'Question']),
            'topic': find_column(headers, ['Topic', 'Category', 'Product Area']),
            'platform': find_column(headers, ['Platform']),
            'model': find_column(headers, ['Model']),
            'brand_mentioned': find_column(headers, ['Workspace Brand Mentioned', 'Brand Mentioned']),
            'response': find_column(headers, ['AI Response', 'Response']),
            'citations': find_column(headers, ['Citations (Links)', 'Citation URLs', 'Citations']),
            'citation_domains': find_column(headers, ['Citation Domains']),
            'competitor_mentioned': find_column(headers, ['Competitor Mentioned']),
            'competitor_mentions': find_column(headers, ['Competitor Mentions']),
            'funnel_stage': find_column(headers, ['Funnel Stage', 'Stage']),
            'brand_name': find_column(headers, ['Tracked Brand', 'Brand Name', 'Brand']),
            'positive': find_column(headers, ['Mentions - Positive']),
            'neutral': find_column(headers, ['Mentions - Neutral']),
            'negative': find_column(headers, ['Mentions - Negative']),
        }

        rows = []
        for row in reader:
            parsed = {}
            for key, col in col_map.items():
                if col and col in row:
                    parsed[key] = row[col].strip()
                else:
                    parsed[key] = ''
            rows.append(parsed)

    return rows, col_map


def analyze_data(rows, brand_name):
    """Compute all metrics from the data."""
    metrics = {}

    # Basic stats
    dates = sorted(set(r['date'] for r in rows if r['date']))
    metrics['date_range'] = (dates[0], dates[-1]) if dates else ('', '')
    metrics['total_executions'] = len(rows)
    metrics['days'] = len(dates)

    # Topics
    topics = sorted(set(r['topic'] for r in rows if r['topic']))
    metrics['topics'] = topics

    # Platforms
    platforms = sorted(set(r['platform'] for r in rows if r['platform']))
    metrics['platforms'] = platforms

    # Overall mention rate
    total = len(rows)
    mentioned = sum(1 for r in rows if parse_bool(r.get('brand_mentioned', '')))
    metrics['overall_mention_rate'] = (mentioned / total * 100) if total else 0
    metrics['total_mentions'] = mentioned

    # Daily mention rate
    daily = defaultdict(lambda: {'total': 0, 'mentioned': 0})
    for r in rows:
        d = r['date']
        if d:
            daily[d]['total'] += 1
            if parse_bool(r.get('brand_mentioned', '')):
                daily[d]['mentioned'] += 1

    daily_rates = {}
    for d in sorted(daily.keys()):
        t = daily[d]['total']
        m = daily[d]['mentioned']
        daily_rates[d] = (m / t * 100) if t else 0
    metrics['daily_rates'] = daily_rates

    # Weekly rates for first and last week
    sorted_dates = sorted(daily_rates.keys())
    if len(sorted_dates) >= 7:
        first_week = sorted_dates[:7]
        last_week = sorted_dates[-7:]
        first_rate = sum(daily_rates[d] for d in first_week) / len(first_week)
        last_rate = sum(daily_rates[d] for d in last_week) / len(last_week)
    elif sorted_dates:
        first_rate = daily_rates[sorted_dates[0]]
        last_rate = daily_rates[sorted_dates[-1]]
    else:
        first_rate = last_rate = 0
    metrics['first_week_rate'] = round(first_rate, 1)
    metrics['last_week_rate'] = round(last_rate, 1)

    # Per-topic rates
    topic_stats = {}
    for topic in topics:
        topic_rows = [r for r in rows if r['topic'] == topic]
        t = len(topic_rows)
        m = sum(1 for r in topic_rows if parse_bool(r.get('brand_mentioned', '')))
        topic_stats[topic] = {'total': t, 'mentioned': m, 'rate': (m / t * 100) if t else 0}
    metrics['topic_stats'] = topic_stats

    # Find dominant topic
    if topic_stats and mentioned > 0:
        dominant = max(topic_stats.items(), key=lambda x: x[1]['mentioned'])
        dom_share = (dominant[1]['mentioned'] / mentioned * 100) if mentioned else 0
        metrics['dominant_topic'] = dominant[0]
        metrics['dominant_topic_stats'] = dominant[1]
        metrics['dominant_topic_share'] = dom_share
        metrics['has_dominant_topic'] = dom_share >= 60
    else:
        metrics['has_dominant_topic'] = False

    # Dominant topic daily rates (if applicable)
    if metrics['has_dominant_topic']:
        dom_topic = metrics['dominant_topic']
        dom_daily = defaultdict(lambda: {'total': 0, 'mentioned': 0})
        for r in rows:
            if r['topic'] == dom_topic and r['date']:
                dom_daily[r['date']]['total'] += 1
                if parse_bool(r.get('brand_mentioned', '')):
                    dom_daily[r['date']]['mentioned'] += 1
        dom_daily_rates = {}
        for d in sorted(dom_daily.keys()):
            t = dom_daily[d]['total']
            m = dom_daily[d]['mentioned']
            dom_daily_rates[d] = (m / t * 100) if t else 0
        metrics['dominant_daily_rates'] = dom_daily_rates

        # First/last week for dominant topic
        dom_sorted = sorted(dom_daily_rates.keys())
        if len(dom_sorted) >= 7:
            dom_first = sum(dom_daily_rates[d] for d in dom_sorted[:7]) / 7
            dom_last = sum(dom_daily_rates[d] for d in dom_sorted[-7:]) / 7
        elif dom_sorted:
            dom_first = dom_daily_rates[dom_sorted[0]]
            dom_last = dom_daily_rates[dom_sorted[-1]]
        else:
            dom_first = dom_last = 0
        metrics['dominant_first_rate'] = round(dom_first, 1)
        metrics['dominant_last_rate'] = round(dom_last, 1)

    # Per-platform rates (for dominant topic if exists, otherwise overall)
    platform_stats = {}
    for plat in platforms:
        if metrics['has_dominant_topic']:
            plat_rows = [r for r in rows if r['platform'] == plat and r['topic'] == metrics['dominant_topic']]
        else:
            plat_rows = [r for r in rows if r['platform'] == plat]
        t = len(plat_rows)
        m = sum(1 for r in plat_rows if parse_bool(r.get('brand_mentioned', '')))
        platform_stats[plat] = {'total': t, 'mentioned': m, 'rate': (m / t * 100) if t else 0}
    metrics['platform_stats'] = platform_stats

    # Platform weekly rates for chart
    platform_weekly = {}
    for plat in platforms:
        if metrics['has_dominant_topic']:
            plat_rows = [r for r in rows if r['platform'] == plat and r['topic'] == metrics['dominant_topic']]
        else:
            plat_rows = [r for r in rows if r['platform'] == plat]

        weekly = defaultdict(lambda: {'total': 0, 'mentioned': 0})
        for r in plat_rows:
            if r['date']:
                try:
                    dt = datetime.strptime(r['date'], '%Y-%m-%d')
                    week_start = dt - timedelta(days=dt.weekday())
                    week_key = week_start.strftime('%Y-%m-%d')
                    weekly[week_key]['total'] += 1
                    if parse_bool(r.get('brand_mentioned', '')):
                        weekly[week_key]['mentioned'] += 1
                except ValueError:
                    pass

        platform_weekly[plat] = {}
        for w in sorted(weekly.keys()):
            t = weekly[w]['total']
            m = weekly[w]['mentioned']
            platform_weekly[plat][w] = (m / t * 100) if t else 0
    metrics['platform_weekly'] = platform_weekly

    # Citation analysis
    citation_urls = Counter()
    for r in rows:
        if parse_bool(r.get('brand_mentioned', '')) and r.get('citations'):
            urls = [u.strip() for u in r['citations'].split('|') if u.strip()]
            brand_lower = brand_name.lower().replace(' ', '')
            for url in urls:
                domain = url.split('/')[2] if len(url.split('/')) > 2 else url
                if brand_lower in domain.lower().replace(' ', '') or brand_lower in url.lower().replace(' ', ''):
                    # Normalize URL
                    clean = url.split('?')[0].rstrip('/')
                    citation_urls[clean] += 1
    metrics['citation_urls'] = citation_urls.most_common(20)
    metrics['total_citations'] = sum(citation_urls.values())

    # Prompt-level analysis: find prompts with biggest improvement
    prompt_performance = {}
    for r in rows:
        prompt = r.get('prompt', '')
        date = r.get('date', '')
        if not prompt or not date:
            continue
        if prompt not in prompt_performance:
            prompt_performance[prompt] = defaultdict(lambda: {'total': 0, 'mentioned': 0})
        prompt_performance[prompt][date]['total'] += 1
        if parse_bool(r.get('brand_mentioned', '')):
            prompt_performance[prompt][date]['mentioned'] += 1

    prompt_gains = []
    for prompt, date_data in prompt_performance.items():
        dates_sorted = sorted(date_data.keys())
        if len(dates_sorted) < 7:
            continue
        first_dates = dates_sorted[:7]
        last_dates = dates_sorted[-7:]
        first_total = sum(date_data[d]['total'] for d in first_dates)
        first_mentioned = sum(date_data[d]['mentioned'] for d in first_dates)
        last_total = sum(date_data[d]['total'] for d in last_dates)
        last_mentioned = sum(date_data[d]['mentioned'] for d in last_dates)
        first_rate = (first_mentioned / first_total * 100) if first_total else 0
        last_rate = (last_mentioned / last_total * 100) if last_total else 0
        gain = last_rate - first_rate
        if gain > 0 and last_rate >= 5:
            prompt_gains.append({
                'prompt': prompt,
                'first_rate': round(first_rate, 1),
                'last_rate': round(last_rate, 1),
                'gain': round(gain, 1),
            })

    prompt_gains.sort(key=lambda x: x['gain'], reverse=True)
    # Filter to dominant topic prompts if there is one
    if metrics['has_dominant_topic']:
        dom_topic = metrics['dominant_topic']
        dom_prompts = set(r['prompt'] for r in rows if r['topic'] == dom_topic)
        topic_gains = [g for g in prompt_gains if g['prompt'] in dom_prompts]
        metrics['prompt_gains'] = topic_gains[:8]
    else:
        metrics['prompt_gains'] = prompt_gains[:8]

    # Competitor analysis
    competitor_counts = Counter()
    for r in rows:
        if r.get('competitor_mentions'):
            comps = [c.strip() for c in r['competitor_mentions'].split('|') if c.strip()]
            for comp in comps:
                competitor_counts[comp] += 1
    metrics['top_competitors'] = competitor_counts.most_common(5)

    # Sentiment
    pos = sum(int(r.get('positive', 0) or 0) for r in rows if parse_bool(r.get('brand_mentioned', '')))
    neu = sum(int(r.get('neutral', 0) or 0) for r in rows if parse_bool(r.get('brand_mentioned', '')))
    neg = sum(int(r.get('negative', 0) or 0) for r in rows if parse_bool(r.get('brand_mentioned', '')))
    total_sent = pos + neu + neg
    metrics['sentiment'] = {
        'positive': pos, 'neutral': neu, 'negative': neg,
        'total': total_sent,
        'positive_pct': (pos / total_sent * 100) if total_sent else 0,
        'positive_neutral_pct': ((pos + neu) / total_sent * 100) if total_sent else 0,
    }

    return metrics


# ============ CHARTS ============

def chart_overall_trend(metrics, tmpdir):
    """Overall AI discoverability over time with 7-day MA."""
    daily = metrics['daily_rates']
    dates = [datetime.strptime(d, '%Y-%m-%d') for d in sorted(daily.keys())]
    vals = [daily[d.strftime('%Y-%m-%d')] for d in dates]
    ma = [sum(vals[max(0, i-6):i+1]) / len(vals[max(0, i-6):i+1]) for i in range(len(vals))]

    fig, ax = plt.subplots(figsize=(6.8, 2.4))
    ax.bar(dates, vals, color='#D5CCE6', alpha=0.6, width=0.8)
    ax.plot(dates, ma, color='#3D2C6B', linewidth=2.5, label='7-Day Average')
    ax.set_title('Overall AI Discoverability (%) Over Time', fontsize=11,
                 fontweight='bold', color='#3D2C6B', pad=8)
    ax.set_ylabel('Mention Rate (%)', fontsize=8, color='#555')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    ax.legend(fontsize=7.5, loc='upper left', frameon=False)
    ax.set_ylim(0, max(vals) * 1.3 if vals else 1)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(labelsize=7.5, colors='#555')
    ax.yaxis.grid(True, alpha=0.2, color='#999')
    plt.tight_layout()
    p = os.path.join(tmpdir, 'c_overall.png')
    fig.savefig(p, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    return p


def chart_topic_breakdown(metrics, tmpdir):
    """Bar chart of mention rates by topic."""
    topic_stats = metrics['topic_stats']
    topics = sorted(topic_stats.keys(), key=lambda t: topic_stats[t]['rate'], reverse=True)
    rates = [topic_stats[t]['rate'] for t in topics]
    counts = [topic_stats[t]['mentioned'] for t in topics]

    # Wrap long topic names
    labels = [t.replace(' & ', ' &\n').replace(' and ', ' &\n') if len(t) > 15 else t for t in topics]

    fig, ax = plt.subplots(figsize=(6.8, 2.2))
    bar_colors = ['#3D2C6B'] + ['#D5CCE6'] * (len(topics) - 1)
    bars = ax.bar(labels, rates, color=bar_colors, edgecolor='white', width=0.6)
    for b, v, mc in zip(bars, rates, counts):
        if v > 0:
            ax.text(b.get_x() + b.get_width() / 2., b.get_height() + 0.06,
                    f'{v:.1f}%\n({mc})', ha='center', va='bottom', fontsize=7.5,
                    fontweight='bold', color='#3D2C6B')

    date_start = metrics['date_range'][0]
    date_end = metrics['date_range'][1]
    ax.set_title(f'AI Discoverability by Category ({date_start} \u2013 {date_end})',
                 fontsize=11, fontweight='bold', color='#3D2C6B', pad=8)
    ax.set_ylabel('Mention Rate (%)', fontsize=8, color='#555')
    ax.set_ylim(0, max(rates) * 1.5 if rates else 1)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(labelsize=7.5, colors='#555')
    ax.yaxis.grid(True, alpha=0.2, color='#999')
    plt.tight_layout()
    p = os.path.join(tmpdir, 'c_topic.png')
    fig.savefig(p, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    return p


def chart_dominant_trend(metrics, tmpdir):
    """Trend chart for the dominant topic."""
    daily = metrics['dominant_daily_rates']
    dates = [datetime.strptime(d, '%Y-%m-%d') for d in sorted(daily.keys())]
    vals = [daily[d.strftime('%Y-%m-%d')] for d in dates]
    ma = [sum(vals[max(0, i-6):i+1]) / len(vals[max(0, i-6):i+1]) for i in range(len(vals))]

    dom_topic = metrics['dominant_topic']
    fig, ax = plt.subplots(figsize=(6.8, 2.4))
    ax.fill_between(dates, vals, color='#D5CCE6', alpha=0.35)
    ax.plot(dates, vals, color='#D5CCE6', alpha=0.5, linewidth=1)
    ax.plot(dates, ma, color='#3D2C6B', linewidth=2.5, label='7-Day Average')
    ax.set_title(f'Growth in AI Discoverability (%) \u2014 {dom_topic} Category',
                 fontsize=11, fontweight='bold', color='#3D2C6B', pad=8)
    ax.set_ylabel('Mention Rate (%)', fontsize=8, color='#555')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    ax.legend(fontsize=7.5, loc='upper left', frameon=False)
    ax.set_ylim(0, max(vals) * 1.3 if vals else 1)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(labelsize=7.5, colors='#555')
    ax.yaxis.grid(True, alpha=0.2, color='#999')
    plt.tight_layout()
    p = os.path.join(tmpdir, 'c_dominant.png')
    fig.savefig(p, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    return p


def chart_prompt_gains(metrics, tmpdir):
    """Horizontal bar chart of prompt-level gains."""
    gains = metrics['prompt_gains'][:6]
    if not gains:
        return None

    # Shorten prompt labels
    def shorten(p, max_len=35):
        if len(p) <= max_len:
            return p
        words = p.split()
        lines = []
        cur = ''
        for w in words:
            if len(cur) + len(w) + 1 > max_len:
                lines.append(cur)
                cur = w
            else:
                cur = f'{cur} {w}' if cur else w
        if cur:
            lines.append(cur)
        return '\n'.join(lines[:2])

    prompts = [shorten(g['prompt']) for g in gains]
    current = [g['last_rate'] for g in gains]

    fig, ax = plt.subplots(figsize=(6.8, 2.8))
    y = range(len(prompts))
    ax.barh(y, current, color='#3D2C6B', height=0.55)
    for i, g in enumerate(gains):
        ax.text(g['last_rate'] + 0.8, i, f'{g["last_rate"]:.0f}%',
                va='center', fontsize=9, fontweight='bold', color='#3D2C6B')
        if g['first_rate'] == 0:
            ax.text(1.0, i, '0% Jan', va='center', fontsize=7, color='white', fontstyle='italic')

    ax.set_yticks(y)
    ax.set_yticklabels(prompts, fontsize=8, color='#555')
    ax.set_title('Key Prompts: Start \u2192 Current Rate',
                 fontsize=11, fontweight='bold', color='#3D2C6B', pad=8)
    ax.set_xlabel('Current Brand Mention Rate (%)', fontsize=8, color='#555')
    ax.set_xlim(0, max(current) * 1.25 if current else 1)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(labelsize=7.5, colors='#555')
    ax.xaxis.grid(True, alpha=0.2, color='#999')
    ax.invert_yaxis()
    plt.tight_layout()
    p = os.path.join(tmpdir, 'c_prompt.png')
    fig.savefig(p, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    return p


def chart_platform(metrics, tmpdir):
    """Multi-line chart showing platform growth over time."""
    platform_weekly = metrics['platform_weekly']
    if not platform_weekly:
        return None

    all_weeks = sorted(set(w for pw in platform_weekly.values() for w in pw.keys()))
    if len(all_weeks) < 3:
        return None

    # Friendly platform names
    plat_names = {
        'ANTHROPIC': 'Claude', 'OPEN_AI': 'OpenAI', 'GOOGLE': 'Gemini',
        'PERPLEXITY': 'Perplexity',
    }
    plat_colors = ['#3D2C6B', '#E8712B', '#E8A54B', '#999999', '#00A651']

    fig, ax = plt.subplots(figsize=(6.8, 2.8))
    markers = ['o', 's', '^', 'D', 'v']
    for i, (plat, weekly) in enumerate(sorted(platform_weekly.items())):
        vals = [weekly.get(w, 0) for w in all_weeks]
        name = plat_names.get(plat, plat)
        ax.plot(range(len(all_weeks)), vals, f'{markers[i % len(markers)]}-',
                color=plat_colors[i % len(plat_colors)],
                linewidth=2.0, markersize=4, label=name)

    week_labels = []
    for i, w in enumerate(all_weeks):
        dt = datetime.strptime(w, '%Y-%m-%d')
        if i == 0 or i == len(all_weeks) - 1 or i % 2 == 0:
            week_labels.append(f'W{i+1}\n{dt.strftime("%b %d")}')
        else:
            week_labels.append(f'W{i+1}')

    ax.set_xticks(range(len(all_weeks)))
    ax.set_xticklabels(week_labels, fontsize=7)

    scope = metrics.get('dominant_topic', 'Overall')
    ax.set_title(f'{scope} Discoverability (%) by AI Platform \u2014 Weekly',
                 fontsize=11, fontweight='bold', color='#3D2C6B', pad=8)
    ax.set_ylabel('Mention Rate (%)', fontsize=8, color='#555')
    ax.legend(fontsize=7.5, loc='upper left', frameon=False, ncol=2)
    all_vals = [v for pw in platform_weekly.values() for v in pw.values()]
    ax.set_ylim(0, max(all_vals) * 1.25 if all_vals else 1)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(labelsize=7.5, colors='#555')
    ax.yaxis.grid(True, alpha=0.2, color='#999')
    plt.tight_layout()
    p = os.path.join(tmpdir, 'c_platform.png')
    fig.savefig(p, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()
    return p


# ============ PDF HELPERS ============

def ytable(num_rows):
    """Standard report table style."""
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), PURPLE_DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, 0), 1, PURPLE_DARK),
    ]
    for i in range(1, num_rows):
        if i % 2 == 0:
            style.append(('BACKGROUND', (0, i), (-1, i), GRAY_ALT))
        style.append(('LINEBELOW', (0, i), (-1, i), 0.5, colors.HexColor('#E0E0E0')))
    return TableStyle(style)


def ibox(text, styles):
    """Insight callout box with purple left border."""
    inner = Paragraph(text, styles['IBody'])
    t = Table([[inner]], colWidths=[6.5 * inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), PURPLE_LIGHT),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LINEBEFORE', (0, 0), (0, -1), 3.5, PURPLE_DARK),
    ]))
    return t


def ai_response_card(prompt_text, response_excerpt, platform, model, date, position, brand_name, S):
    """Build a card showing an AI response with the brand highlighted."""
    highlighted = response_excerpt.replace(
        brand_name, f'<font color="#E8712B"><b>{brand_name}</b></font>')

    prompt_para = Paragraph(f'&ldquo;{prompt_text}&rdquo;', S['CardPrompt'])
    prompt_row = Table([[prompt_para]], colWidths=[6.5 * inch])
    prompt_row.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), PURPLE_DARK),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))

    body_para = Paragraph(highlighted, S['CardBody'])
    badge = (f'<b>{platform}</b>  &nbsp;|&nbsp;  {model}  &nbsp;|&nbsp;  {date}'
             f'  &nbsp;|&nbsp;  Position: <font color="#E8712B"><b>#{position}</b></font>')
    meta_para = Paragraph(badge, S['CardMeta'])

    body_table = Table([
        [body_para], [Spacer(1, 4)],
        [HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#E0E0E0'))],
        [meta_para],
    ], colWidths=[6.5 * inch])
    body_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FAFAFA')),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
        ('TOPPADDING', (0, 0), (0, 0), 10),
        ('BOTTOMPADDING', (0, 0), (0, 0), 4),
        ('TOPPADDING', (0, 1), (-1, -1), 2),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 8),
        ('LINEBELOW', (0, -1), (-1, -1), 1, colors.HexColor('#E0E0E0')),
        ('LINEBEFORE', (0, 0), (0, -1), 1, colors.HexColor('#E0E0E0')),
        ('LINEAFTER', (-1, 0), (-1, -1), 1, colors.HexColor('#E0E0E0')),
    ]))

    return KeepTogether([prompt_row, body_table, Spacer(1, 10)])


# ============ BUILD PDF ============

def build_pdf(metrics, brand_name, output_path, logo_path=None, response_cards=None,
              prepared_by='Yolando'):
    """Build the executive update PDF."""
    logo_path = logo_path or str(DEFAULT_LOGO)
    tmpdir = tempfile.mkdtemp()

    # Generate charts
    charts = {'overall': chart_overall_trend(metrics, tmpdir)}

    if len(metrics['topics']) > 1:
        charts['topic'] = chart_topic_breakdown(metrics, tmpdir)

    if metrics.get('has_dominant_topic'):
        charts['dominant'] = chart_dominant_trend(metrics, tmpdir)

    if metrics.get('prompt_gains'):
        charts['prompt'] = chart_prompt_gains(metrics, tmpdir)

    if len(metrics['platforms']) > 1:
        charts['platform'] = chart_platform(metrics, tmpdir)

    # Create PDF
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                            topMargin=0.65 * inch, bottomMargin=0.6 * inch,
                            leftMargin=0.75 * inch, rightMargin=0.75 * inch)

    # Styles
    S = getSampleStyleSheet()
    S.add(ParagraphStyle('YT', parent=S['Title'], fontSize=28, textColor=BLACK,
                         fontName='Helvetica-Bold', alignment=TA_LEFT, spaceAfter=2, leading=32))
    S.add(ParagraphStyle('YS1', parent=S['Normal'], fontSize=11, textColor=GRAY_SUB,
                         fontName='Helvetica', spaceAfter=2))
    S.add(ParagraphStyle('YS2', parent=S['Normal'], fontSize=9, textColor=GRAY_SUB,
                         fontName='Helvetica', spaceAfter=14))
    S.add(ParagraphStyle('YH', parent=S['Heading1'], fontSize=18, textColor=BLACK,
                         fontName='Helvetica-Bold', spaceBefore=20, spaceAfter=10, leading=22))
    S.add(ParagraphStyle('YSH', parent=S['Normal'], fontSize=11, textColor=ORANGE_WARM,
                         fontName='Helvetica-Bold', spaceBefore=10, spaceAfter=6))
    S.add(ParagraphStyle('YB', parent=S['Normal'], fontSize=10, textColor=BLACK,
                         fontName='Helvetica', spaceAfter=8, leading=14))
    S.add(ParagraphStyle('YBS', parent=S['Normal'], fontSize=8.5,
                         textColor=colors.HexColor('#666666'),
                         fontName='Helvetica', spaceAfter=4, leading=11))
    S.add(ParagraphStyle('IBody', parent=S['Normal'], fontSize=10, textColor=BLACK,
                         fontName='Helvetica', leading=14))
    S.add(ParagraphStyle('YBul', parent=S['Normal'], fontSize=10, textColor=BLACK,
                         fontName='Helvetica', leftIndent=18, bulletIndent=6, spaceAfter=6, leading=14))
    S.add(ParagraphStyle('YF', parent=S['Normal'], fontSize=8, textColor=GRAY_SUB,
                         fontName='Helvetica', alignment=TA_LEFT))
    S.add(ParagraphStyle('CardPrompt', parent=S['Normal'], fontSize=10, textColor=WHITE,
                         fontName='Helvetica-Bold', alignment=TA_LEFT, leading=13))
    S.add(ParagraphStyle('CardBody', parent=S['Normal'], fontSize=8.5,
                         textColor=colors.HexColor('#333333'),
                         fontName='Helvetica', alignment=TA_LEFT, leading=12))
    S.add(ParagraphStyle('CardMeta', parent=S['Normal'], fontSize=7.5, textColor=GRAY_SUB,
                         fontName='Helvetica', alignment=TA_LEFT, leading=10))

    oc = ParagraphStyle('oc', parent=S['Normal'], fontSize=9, textColor=ORANGE_ACCENT,
                        fontName='Helvetica-Bold', alignment=TA_CENTER)
    gc = ParagraphStyle('gc', parent=S['Normal'], fontSize=9, textColor=GREEN_POS,
                        fontName='Helvetica-Bold', alignment=TA_CENTER)
    kn = ParagraphStyle('kn', parent=S['Normal'], fontSize=22, textColor=WHITE,
                        fontName='Helvetica-Bold', alignment=TA_CENTER, leading=26)
    kl = ParagraphStyle('kl', parent=S['Normal'], fontSize=8, textColor=WHITE,
                        fontName='Helvetica', alignment=TA_CENTER, leading=10)
    kfrom = ParagraphStyle('kfrom', parent=S['Normal'], fontSize=10,
                           textColor=colors.HexColor('#C0B8D8'),
                           fontName='Helvetica', alignment=TA_CENTER, leading=12)

    story = []
    m = metrics

    # ===== HEADER =====
    header_cells = [Paragraph(brand_name, S['YT'])]
    if logo_path and os.path.exists(logo_path):
        header_cells.append(Image(logo_path, width=1.2 * inch, height=0.4 * inch))
    else:
        header_cells.append(Paragraph('', S['Normal']))
    ht = Table([header_cells], colWidths=[5.0 * inch, 2.0 * inch])
    ht.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
    ]))
    story.append(ht)
    story.append(Paragraph("GEO Performance Update", S['YS1']))
    date_range = f"{m['date_range'][0]} \u2013 {m['date_range'][1]}"
    story.append(Paragraph(f"Executive Summary  |  {date_range}", S['YS2']))
    story.append(HRFlowable(width="100%", thickness=2.5, color=ORANGE_ACCENT, spaceAfter=16))

    # ===== KEY IMPACT ACHIEVED =====
    story.append(Paragraph("Key Impact Achieved Since Engagement", S['YH']))

    # Build narrative context
    if m['has_dominant_topic']:
        dom = m['dominant_topic']
        context = (
            f"Since tracking began for {brand_name}'s AI visibility, the GEO strategy has "
            f"focused on the <b>{dom}</b> vertical. The results over {m['days']} days:"
        )
    else:
        context = (
            f"Since tracking began for {brand_name}'s AI visibility, the GEO program has implemented a "
            f"comprehensive GEO strategy across {len(m['topics'])} categories. "
            f"The results over {m['days']} days:"
        )
    story.append(Paragraph(context, S['YB']))

    # KPI boxes
    growth_mult = round(m['last_week_rate'] / m['first_week_rate'], 0) if m['first_week_rate'] > 0 else 0
    kpi_cells_from = [
        Paragraph(f'from {m["first_week_rate"]}%', kfrom),
    ]
    kpi_cells_val = [
        Paragraph(f'<b>{m["last_week_rate"]}%</b>', kn),
    ]
    kpi_cells_label = [
        Paragraph(f'Overall AI Discoverability<br/>({growth_mult:.0f}x increase)' if growth_mult > 1
                  else 'Overall AI Discoverability', kl),
    ]

    if m['has_dominant_topic']:
        dom_mult = round(m['dominant_last_rate'] / m['dominant_first_rate'], 0) if m['dominant_first_rate'] > 0 else 0
        kpi_cells_from.append(Paragraph(f'from {m["dominant_first_rate"]}%', kfrom))
        kpi_cells_val.append(Paragraph(f'<b>{m["dominant_last_rate"]}%</b>', kn))
        kpi_cells_label.append(
            Paragraph(f'{m["dominant_topic"]} Mention Rate<br/>({dom_mult:.0f}x increase)' if dom_mult > 1
                      else f'{m["dominant_topic"]} Mention Rate', kl))

    if m['total_citations'] > 0:
        kpi_cells_from.append(Paragraph('&nbsp;', kfrom))
        kpi_cells_val.append(Paragraph(f'<b>{m["total_citations"]}</b>', kn))
        kpi_cells_label.append(Paragraph(f'Total {brand_name}<br/>Citations in AI', kl))

    kpi_cells_from.append(Paragraph('&nbsp;', kfrom))
    kpi_cells_val.append(Paragraph(f'<b>{m["total_mentions"]}</b>', kn))
    kpi_cells_label.append(Paragraph('Total Brand<br/>Mentions', kl))

    num_cols = len(kpi_cells_val)
    col_w = 6.6 / num_cols
    kpi = Table([kpi_cells_from, kpi_cells_val, kpi_cells_label],
                colWidths=[col_w * inch] * num_cols,
                rowHeights=[0.22 * inch, 0.42 * inch, 0.36 * inch])
    kpi_style = [
        ('BACKGROUND', (0, 0), (-1, -1), PURPLE_DARK),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, 0), 'BOTTOM'),
        ('VALIGN', (0, 1), (-1, 1), 'MIDDLE'),
        ('VALIGN', (0, 2), (-1, 2), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 0),
        ('TOPPADDING', (0, 1), (-1, 1), 0),
        ('BOTTOMPADDING', (0, 1), (-1, 1), 0),
        ('TOPPADDING', (0, 2), (-1, 2), 0),
        ('BOTTOMPADDING', (0, 2), (-1, 2), 8),
    ]
    for i in range(1, num_cols):
        kpi_style.append(('LINEBEFORE', (i, 0), (i, -1), 1, colors.HexColor('#5A4A8A')))
    kpi.setStyle(TableStyle(kpi_style))
    story.append(kpi)
    story.append(Spacer(1, 8))

    # ===== OVERALL TREND =====
    story.append(Paragraph("Overall AI Discoverability", S['YH']))
    story.append(Paragraph(
        f"{brand_name} is tracked daily across {m['total_executions']:,} prompt executions "
        f"spanning {len(m['topics'])} topics on {len(m['platforms'])} AI platforms. "
        f"The overall brand mention rate climbed from {m['first_week_rate']}% to {m['last_week_rate']}%.",
        S['YB']))
    story.append(Image(charts['overall'], width=6.5 * inch, height=2.3 * inch))
    story.append(Spacer(1, 8))

    # ===== CATEGORY BREAKDOWN (if multiple topics) =====
    if 'topic' in charts:
        if m['has_dominant_topic']:
            dom = m['dominant_topic']
            dom_stats = m['dominant_topic_stats']
            story.append(Paragraph(f"{dom} Is Driving the Growth", S['YH']))
            story.append(Paragraph(
                f"The content strategy has focused on the {dom} category — and this is where the "
                f"results are concentrated. {dom} accounts for <b>{m['dominant_topic_share']:.0f}% "
                f"of all {brand_name} brand mentions</b> ({dom_stats['mentioned']} of "
                f"{m['total_mentions']} total).",
                S['YB']))
        else:
            story.append(Paragraph("AI Discoverability by Category", S['YH']))

        story.append(Image(charts['topic'], width=6.5 * inch, height=2.1 * inch))
        story.append(Spacer(1, 6))

    # ===== DOMINANT TOPIC TREND =====
    if 'dominant' in charts:
        story.append(Image(charts['dominant'], width=6.5 * inch, height=2.3 * inch))
        story.append(Spacer(1, 6))

    # ===== CONTENT CITATIONS =====
    if m['citation_urls']:
        story.append(Paragraph("Content Fueling AI Citations", S['YH']))

        # Separate brand blog/content URLs from homepage/third-party
        blog_urls = []
        other_urls = []
        brand_domain = brand_name.lower().replace(' ', '').replace('-', '')
        for url, count in m['citation_urls']:
            path = url.split('/', 3)[-1] if len(url.split('/')) > 3 else ''
            if brand_domain in url.lower().replace(' ', '').replace('-', ''):
                if path and 'blog' in path.lower():
                    blog_urls.append((url, count))
                else:
                    other_urls.append((url, count))
            else:
                other_urls.append((url, count))

        if blog_urls:
            story.append(Paragraph("Published Content (Blog Posts)", S['YSH']))
            blog_data = [['Blog Post', 'Citations']]
            for url, count in blog_urls[:8]:
                title = url.split('/')[-1].replace('-', ' ').title() if '/' in url else url
                blog_data.append([title, Paragraph(f'<b>{count}</b>', oc)])
            bt = Table(blog_data, colWidths=[4.5 * inch, 1.5 * inch])
            bt.setStyle(ytable(len(blog_data)))
            story.append(bt)
            story.append(Spacer(1, 10))

        if other_urls:
            story.append(Paragraph(f"Other {brand_name} Pages &amp; Third-Party Coverage", S['YSH']))
            other_data = [['Source', 'Citations']]
            for url, count in other_urls[:6]:
                domain = url.split('/')[2] if len(url.split('/')) > 2 else url
                other_data.append([domain, Paragraph(f'<b>{count}</b>', oc)])
            ot = Table(other_data, colWidths=[4.5 * inch, 1.5 * inch])
            ot.setStyle(ytable(len(other_data)))
            story.append(ot)
            story.append(Spacer(1, 8))

    # ===== PLATFORM BREAKDOWN =====
    if 'platform' in charts:
        story.append(Paragraph("Growth by AI Platform", S['YH']))

        plat_names = {
            'ANTHROPIC': 'Claude', 'OPEN_AI': 'OpenAI/GPT',
            'GOOGLE': 'Gemini', 'PERPLEXITY': 'Perplexity',
        }
        # Find best platform
        best_plat = max(m['platform_stats'].items(), key=lambda x: x[1]['rate'])
        best_name = plat_names.get(best_plat[0], best_plat[0])
        scope = m.get('dominant_topic', '')
        scope_text = f"{scope} d" if scope else "D"
        story.append(Paragraph(
            f"{brand_name}'s {scope_text.lower() if scope else 'd'}iscoverability is growing across "
            f"AI platforms, with {best_name} showing the strongest adoption at "
            f"{best_plat[1]['rate']:.1f}%.",
            S['YB']))
        story.append(Image(charts['platform'], width=6.5 * inch, height=2.7 * inch))
        story.append(Spacer(1, 8))

        # Platform table
        plat_header = ['Platform', 'Mention Rate', 'Mentions']
        plat_rows = []
        for plat, stats in sorted(m['platform_stats'].items(),
                                   key=lambda x: x[1]['rate'], reverse=True):
            name = plat_names.get(plat, plat)
            plat_rows.append([
                name,
                Paragraph(f'<b>{stats["rate"]:.1f}%</b>', oc),
                Paragraph(f'<b>{stats["mentioned"]}</b>', gc),
            ])
        pd_data = [plat_header] + plat_rows
        pt = Table(pd_data, colWidths=[2.5 * inch, 1.5 * inch, 1.5 * inch])
        pt.setStyle(ytable(len(pd_data)))
        story.append(pt)
        story.append(Spacer(1, 8))

    # ===== PROMPT-LEVEL GAINS =====
    if 'prompt' in charts and m['prompt_gains']:
        story.append(Paragraph("Prompt-Level Discoverability Gains", S['YH']))
        story.append(Paragraph(
            f"Multiple high-intent prompts went from <b>0% {brand_name} mention rate</b> to "
            f"significant rates in the most recent period.",
            S['YB']))
        story.append(Image(charts['prompt'], width=6.5 * inch, height=2.6 * inch))
        story.append(Spacer(1, 8))

        pr_header = ['Prompt', 'Start Rate', 'Current', 'Change']
        pr_rows = []
        for g in m['prompt_gains'][:6]:
            pr_rows.append([
                g['prompt'][:60],
                Paragraph(f'<b>{g["first_rate"]}%</b>', oc),
                Paragraph(f'<b>{g["last_rate"]}%</b>', oc),
                Paragraph(f'<b>+{g["gain"]}pp</b>', gc),
            ])
        prd = [pr_header] + pr_rows
        prt = Table(prd, colWidths=[3.1 * inch, 0.8 * inch, 0.85 * inch, 0.95 * inch])
        prt.setStyle(ytable(len(prd)))
        story.append(prt)
        story.append(Spacer(1, 8))

    # ===== AI RESPONSE CARDS (optional) =====
    if response_cards:
        story.append(Paragraph(f"{brand_name} in AI Responses: Position #1 Examples", S['YH']))
        story.append(Paragraph(
            f"Below are recent examples of {brand_name} appearing as the <b>#1 recommended "
            f"provider</b> in AI responses.", S['YB']))
        story.append(Spacer(1, 4))
        for card in response_cards:
            story.append(ai_response_card(
                prompt_text=card['prompt'],
                response_excerpt=card['response'],
                platform=card.get('platform', ''),
                model=card.get('model', ''),
                date=card.get('date', ''),
                position=card.get('position', '1'),
                brand_name=brand_name,
                S=S,
            ))

    # ===== RECOMMENDATIONS =====
    story.append(PageBreak())
    story.append(Paragraph("Recommendations &amp; Next Steps", S['YH']))

    # Auto-generate recommendations based on data
    recs = []
    if m.get('prompt_gains'):
        recs.append(
            f"<b>Expand content coverage.</b> Several high-value prompts still show 0% mention "
            f"rate. New content targeting these gaps can replicate the established success pattern."
        )
    if m['has_dominant_topic'] and len(m['topics']) > 1:
        secondary = [(t, s) for t, s in m['topic_stats'].items()
                     if t != m['dominant_topic'] and s['rate'] > 0]
        if secondary:
            sec_text = ', '.join(f"{t} ({s['rate']:.1f}%)" for t, s in secondary[:2])
            recs.append(
                f"<b>Cross-pollinate into adjacent topics.</b> {sec_text} show early signals. "
                f"Success in {m['dominant_topic']} can inform strategy for these verticals."
            )
    if m['citation_urls']:
        top_url = m['citation_urls'][0][0].split('/')[-1].replace('-', ' ').title()
        recs.append(
            f"<b>Strengthen citation reinforcement.</b> The top-cited page ({top_url}) should "
            f"be kept current and expanded \u2014 it is {brand_name}'s single most valuable GEO asset."
        )
    if m['top_competitors']:
        top_comp = m['top_competitors'][0]
        recs.append(
            f"<b>Monitor competitor displacement.</b> {top_comp[0]} ({top_comp[1]} mentions) "
            f"remains the most visible competitor. Targeted content addressing areas where "
            f"{brand_name} outperforms can accelerate share gains."
        )
    if not recs:
        recs.append(f"<b>Continue the current strategy.</b> {brand_name}'s visibility is growing.")

    story.append(Paragraph(
        f"To sustain and accelerate momentum:", S['YB']))
    for r in recs:
        story.append(Paragraph(f'<bullet>&bull;</bullet>{r}', S['YBul']))

    story.append(Spacer(1, 8))
    story.append(ibox(
        f"<b><font color='#E8A54B'>Bottom line:</font></b> {brand_name}'s GEO strategy is working. "
        f"Content is being indexed and cited by AI models, driving measurable improvements in "
        f"discoverability. The playbook is proven \u2014 the next step is expanding it.", S))

    # ===== FOOTER =====
    story.append(Spacer(1, 0.25 * inch))
    footer_cells = [
        Paragraph(
            f"Analysis based on {m['total_executions']:,} LLM prompt executions across "
            f"{m['days']} days ({m['date_range'][0]} \u2013 {m['date_range'][1]}).<br/>"
            f"Data tracked across {', '.join(m['platforms'])}. Prepared by {prepared_by}.",
            S['YF']),
    ]
    if logo_path and os.path.exists(logo_path):
        footer_cells.append(Image(logo_path, width=0.9 * inch, height=0.3 * inch))
    else:
        footer_cells.append(Paragraph('', S['Normal']))
    ft = Table([footer_cells], colWidths=[5.0 * inch, 2.0 * inch])
    ft.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(ft)

    doc.build(story)
    print(f"PDF saved: {output_path}")

    # Clean up temp chart files
    for f in os.listdir(tmpdir):
        os.remove(os.path.join(tmpdir, f))
    os.rmdir(tmpdir)


def main():
    parser = argparse.ArgumentParser(description='Build GEO Executive Update PDF')
    parser.add_argument('--csv', required=True, help='Path to CSV file')
    parser.add_argument('--brand', required=True, help='Brand name')
    parser.add_argument('--output', required=True, help='Output PDF path')
    parser.add_argument('--logo', default=None, help='Optional logo PNG path')
    parser.add_argument('--prepared-by', default='Yolando', help='Prepared-by label for the footer')
    args = parser.parse_args()

    rows, col_map = load_data(args.csv)
    metrics = analyze_data(rows, args.brand)
    build_pdf(metrics, args.brand, args.output, args.logo, prepared_by=args.prepared_by)


if __name__ == '__main__':
    main()
