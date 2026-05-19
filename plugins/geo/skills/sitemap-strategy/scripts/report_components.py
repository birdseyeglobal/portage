"""Build a sitemap-strategy PDF from prepared GEO report data.

Treat this as a TEMPLATE. Clone it for each engagement, then fill in the data
structures at the bottom of the file. The flowable definitions and page chrome
should rarely need to change. Customize the `build()` function with your data.

The recommended section order (matches SKILL.md):
    01. Executive summary (recommendations-first, then findings, cap at 2 pages)
    02. Where the brand shows up today (owned-URLs table with % share)
    03. What competitor pages win citations (operator patterns)
    04. (optional) How aggregators earn their citations (affiliate patterns)
    05. Optimize existing pages (gap cards)
    06. Ship new pages (tier-by-tier proposed blocks)
    07. P0 page playbooks
    08. Appendix (full topic-by-funnel table)

Inputs you provide via the data dicts at the bottom:
    REPORT             - title, subtitle, date, brand_name, brand_domain
    KPIS               - 4 KPI card values for the executive summary
    RECOMMENDATIONS    - dict with optimize_recs + ship_recs lists of (label, action)
    FINDINGS           - 3-5 (headline, one-line-supporting-fact) tuples
    TOPIC_DATA         - rows for the topic-cluster table (appendix)
    OWNED_DATA         - rows for the owned-URLs table with a % share column
    COMP_DATA          - rows for the top-cited competitor URLs table (section 03)
    PATTERNS           - the operator competitor patterns (section 03)
    AFFILIATE_PATTERNS - optional, the aggregator tactics (section 04)
    GAP_BLOCKS         - one per existing page in the audit (section 05)
    PROPOSED           - one per new page in the strategy (section 06)
    PHASES             - optional. Three phase tables; omit unless client asked.
    PLAYBOOKS          - one per P0 page with the writer-ready brief (section 07)

External assets:
    LOGO_PATH    - defaults to the Yolando logo from the styleguide plugin.
                   Pass logo_path to build() to override it.

After building, run the empty-page cleanup pass:
    from pypdf import PdfReader, PdfWriter
    r = PdfReader(OUT); w = PdfWriter()
    for p in r.pages:
        if len((p.extract_text() or '').strip()) < 350: continue
        w.add_page(p)
    with open(OUT, 'wb') as f: w.write(f)

USAGE PATTERN (recommended)
---------------------------
Don't call build() directly. Instead, write a per-engagement driver script
that imports the flowable helpers from this module and assembles the story
manually. That gives you full control over section ordering, the size of
the executive summary, and which sections to include (e.g. the affiliate
section is optional).

Helpers exported for use in driver scripts:
    toc_table(entries, avail)                    - clickable table of contents
    numbered_recs_table(items, avail, start_n=1) - tight 2-column numbered list
    owned_table_with_share(owned_data, avail)    - owned-URLs with % share col
    rollup_matrix(rows, ...)                     - citation roll-up with heatmap
    pattern_card(title, url, body, stat, avail)  - competitor or affiliate card
    gap_block(priority, title, url, meta, ...)   - per-page audit gap card
    proposed_block(priority, urls, body, avail)  - new-page proposed block
    playbook(num, slug, title, ...)              - one P0 page playbook
    phase_table(rows)                            - optional phased roadmap
    alert_box(title, body, avail)                - callout box
    make_table(data, col_widths, num_cols, ...)  - standard data table
    KPICard, Chip, Eyebrow, HRule                - decorative flowables

Section anchors. Add a clickable TOC by:
    1. Calling toc_table(entries, avail) on the page after the cover. Each
       entry is (num, title, sub, anchor_id).
    2. At the start of each section's rendering, place:
           story.append(Paragraph(f'<a name="{anchor_id}"/>', BODY_S))
       immediately before the Eyebrow flowable. The TOC link resolves to
       this anchor and jumps the reader to the section.

The build() function below is preserved as a v1 reference, but follows the
older section ordering (findings-before-recommendations, in-body topic table,
mandatory phased roadmap). Prefer the v2 pattern documented above.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    Paragraph, Spacer, PageBreak, Table, TableStyle,
    Frame, PageTemplate, BaseDocTemplate, NextPageTemplate, HRFlowable,
)
from reportlab.platypus.flowables import Flowable
from pathlib import Path

# ============================================================================
# Default report design tokens
# ============================================================================
FG = HexColor('#161518')
FG_2 = HexColor('#7e7e80')
FG_3 = HexColor('#a3a3a6')
BG = HexColor('#f8f8f8')
BG_ELEV = HexColor('#ffffff')
BG_SUNKEN = HexColor('#f0f0f0')
BORDER = HexColor('#cbcbcf')
BORDER_SOFT = HexColor('#e5e5e5')
ACCENT = HexColor('#9747ff')
ACCENT_SOFT = HexColor('#f5efff')
PRIMARY = HexColor('#a7a6fe')
LINK = HexColor('#583b9d')
MANGO = HexColor('#ea9e59')
RED = HexColor('#d80027')
P0_BG, P0_FG = RED, white
P1_BG, P1_FG = MANGO, FG
P2_BG, P2_FG = PRIMARY, FG

PAGE_W, PAGE_H = letter
MARGIN = 0.6 * inch

# ============================================================================
# Configure these per engagement
# ============================================================================
OUT = '/path/to/output.pdf'         # CHANGE per engagement
_SCRIPT_DIR = Path(__file__).resolve().parent
_PLUGINS_DIR = _SCRIPT_DIR.parents[3]
LOGO_PATH = str(
    _PLUGINS_DIR
    / 'styleguide'
    / 'skills'
    / 'visual-styleguide'
    / 'references'
    / 'yolando-design-system'
    / 'assets'
    / 'yolando-full-dark.png'
)

# ============================================================================
# Paragraph styles
# ============================================================================
H1 = ParagraphStyle('H1', fontName='Helvetica-Bold', fontSize=24, leading=28, spaceAfter=10, textColor=FG)
H2 = ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=16, leading=20, spaceBefore=18, spaceAfter=8, textColor=FG)
H3 = ParagraphStyle('H3', fontName='Helvetica-Bold', fontSize=11, leading=14, spaceBefore=8, spaceAfter=4, textColor=FG)
LEAD = ParagraphStyle('Lead', fontName='Helvetica', fontSize=11, leading=16, textColor=FG_2, spaceAfter=12)
BODY = ParagraphStyle('Body', fontName='Helvetica', fontSize=10, leading=14, textColor=FG, spaceAfter=6)
BODY_S = ParagraphStyle('BodyS', fontName='Helvetica', fontSize=9, leading=12, textColor=FG, spaceAfter=4)
BODY_XS = ParagraphStyle('BodyXS', fontName='Helvetica', fontSize=8.5, leading=11, textColor=FG, spaceAfter=3)
META = ParagraphStyle('Meta', fontName='Helvetica', fontSize=8.5, leading=11, textColor=FG_2, spaceAfter=4)
URL = ParagraphStyle('URL', fontName='Courier', fontSize=8.5, leading=11, textColor=LINK, spaceAfter=3)
LBL = ParagraphStyle('Lbl', fontName='Helvetica-Bold', fontSize=9.5, leading=12, textColor=FG, spaceBefore=4, spaceAfter=2)
COVER_TITLE = ParagraphStyle('CoverTitle', fontName='Helvetica-Bold', fontSize=32, leading=38, textColor=FG, spaceAfter=16)
COVER_SUB = ParagraphStyle('CoverSub', fontName='Helvetica', fontSize=12, leading=17, textColor=FG_2, spaceAfter=12)
COVER_EYE = ParagraphStyle('CoverEye', fontName='Courier-Bold', fontSize=8, leading=10, textColor=FG_3, spaceAfter=10)
PLAY_LBL = ParagraphStyle('PlayLbl', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=ACCENT, spaceBefore=6, spaceAfter=2)

# ============================================================================
# Custom flowables
# ============================================================================
class Eyebrow(Flowable):
    def __init__(self, text):
        Flowable.__init__(self); self.text = text; self.h = 14
    def wrap(self, w, h): self.w = w; return (w, self.h)
    def draw(self):
        c = self.canv
        c.setFillColor(ACCENT); c.circle(3, 6, 2.5, fill=1, stroke=0)
        c.setFillColor(FG_3); c.setFont('Courier-Bold', 8); c.drawString(12, 4, self.text.upper())

class HRule(Flowable):
    def __init__(self, color=BORDER_SOFT, thickness=0.5, w=None, space=4):
        Flowable.__init__(self); self.color=color; self.thickness=thickness; self.w=w; self.space=space
    def wrap(self, w, h):
        if self.w is None: self.w = w
        return (self.w, self.thickness + self.space*2)
    def draw(self):
        c = self.canv; c.setStrokeColor(self.color); c.setLineWidth(self.thickness)
        c.line(0, self.space + self.thickness, self.w, self.space + self.thickness)

class Chip(Flowable):
    def __init__(self, text, bg, fg=FG, w=30, h=14):
        Flowable.__init__(self); self.text=text; self.bg=bg; self.fg=fg; self.w=w; self.h=h
    def wrap(self, *a): return (self.w, self.h)
    def draw(self):
        c = self.canv
        c.setFillColor(self.bg); c.roundRect(0, 0, self.w, self.h, 3, fill=1, stroke=0)
        c.setFillColor(self.fg); c.setFont('Courier-Bold', 8)
        text_w = c.stringWidth(self.text, 'Courier-Bold', 8)
        c.drawString((self.w - text_w)/2, 4, self.text)

class KPICard(Flowable):
    def __init__(self, label, number, sub, w, accent=False):
        Flowable.__init__(self); self.label=label; self.number=number; self.sub=sub
        self.w=w; self.h=80; self.accent=accent
    def wrap(self, *a): return (self.w, self.h)
    def draw(self):
        c = self.canv
        c.setStrokeColor(BORDER); c.setFillColor(BG_ELEV); c.setLineWidth(0.5)
        c.roundRect(0, 0, self.w, self.h, 8, fill=1, stroke=1)
        c.setFillColor(FG_3); c.setFont('Courier-Bold', 7)
        c.drawString(10, self.h - 18, self.label.upper())
        c.setFillColor(ACCENT if self.accent else FG); c.setFont('Helvetica-Bold', 22)
        c.drawString(10, self.h - 46, self.number)
        c.setFillColor(FG_2); c.setFont('Helvetica', 7.5)
        from reportlab.lib.utils import simpleSplit
        lines = simpleSplit(self.sub, 'Helvetica', 7.5, self.w - 20)[:3]
        y = self.h - 58
        for ln in lines:
            c.drawString(10, y, ln); y -= 10

# ============================================================================
# Helpers
# ============================================================================

# Tight body style used for the numbered recommendations table.
REC_BODY = ParagraphStyle('RecBody', fontName='Helvetica', fontSize=8, leading=9.6,
                          textColor=FG, spaceAfter=0)
H2_TIGHT = ParagraphStyle('H2Tight', fontName='Helvetica-Bold', fontSize=16, leading=20,
                          spaceBefore=4, spaceAfter=2, textColor=FG)


def numbered_recs_table(items, avail, start_n=1):
    """Tight numbered list rendered as a 2-column table.

    items: list of (label, action) tuples.
    avail: page-body width.
    start_n: starting number (use start_n=12 for the second list if you want
             continuous numbering across A. Optimize and B. Ship).

    The result fits roughly 16 items on one letter-page below a 4-up KPI grid.
    """
    rows = []
    for i, (label, action) in enumerate(items, start=start_n):
        num_cell = Paragraph(
            f'<font face="Courier-Bold" color="#9747ff" size="8.5">{i:02d}</font>', BODY_S)
        body_cell = Paragraph(f'<b>{label}.</b>  {action}', REC_BODY)
        rows.append([num_cell, body_cell])
    t = Table(rows, colWidths=[0.26 * inch, avail - 0.26 * inch])
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 1), ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
    ]))
    return t


def owned_table_with_share(owned_data, avail):
    """Owned-URLs table with a % share column and wrapping inside each cell.

    owned_data: list of (url, citations_int, pct_share_float, notes) tuples,
                with the header row prepended ('URL', 'Citations', '% share', 'Notes').
    Returns a Table with monospace URL cells that wrap, so long URLs don't overflow.
    """
    rows = [[
        Paragraph(f'<font face="Courier" size="7.5">{owned_data[0][0]}</font>', BODY_XS),
        Paragraph(f'<b>{owned_data[0][1]}</b>', BODY_XS),
        Paragraph(f'<b>{owned_data[0][2]}</b>', BODY_XS),
        Paragraph(f'<b>{owned_data[0][3]}</b>', BODY_XS),
    ]]
    for row in owned_data[1:]:
        url, cites, pct, note = row[0], row[1], row[2], row[3]
        if isinstance(cites, int): cites = f'{cites:,}'
        if isinstance(pct, (int, float)): pct = f'{pct}%'
        rows.append([
            Paragraph(f'<font face="Courier" size="7">{url}</font>', BODY_XS),
            Paragraph(str(cites), BODY_XS),
            Paragraph(str(pct), BODY_XS),
            Paragraph(str(note), BODY_XS),
        ])
    t = Table(rows, colWidths=[2.95 * inch, 0.55 * inch, 0.55 * inch, 2.55 * inch])
    t.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 8.5),
        ('TEXTCOLOR', (0, 0), (-1, 0), FG_2),
        ('BACKGROUND', (0, 0), (-1, 0), BG_SUNKEN),
        ('TEXTCOLOR', (0, 1), (-1, -1), FG),
        ('LINEBELOW', (0, 0), (-1, -1), 0.4, BORDER_SOFT),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (1, 0), (2, -1), 'RIGHT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5), ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    return t


def toc_table(entries, avail):
    """Render a table-of-contents block with clickable section links.

    entries: list of (num, title, sub, anchor) tuples. The anchor matches the
    `<a name="..."/>` marker placed at the start of each section's rendering.

    Pair with: `story.append(Paragraph(f'<a name="{anchor}"/>', BODY_S))` placed
    immediately before each section's eyebrow so the link target resolves.
    """
    toc_rows = []
    for num, title, sub, anchor in entries:
        cell_num = Paragraph(
            f'<a href="#{anchor}"><font face="Courier-Bold" color="#9747ff" size="11">{num}</font></a>', BODY)
        cell_title = Paragraph(
            f'<a href="#{anchor}"><b><font color="#161518">{title}.</font></b> '
            f'<font color="#7e7e80">{sub}</font></a>', BODY)
        toc_rows.append([cell_num, cell_title])
    t = Table(toc_rows, colWidths=[0.5 * inch, avail - 0.5 * inch])
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 8), ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, -1), 0.4, BORDER_SOFT),
    ]))
    return t


def rollup_matrix(rows, brand_row_label=None, col_widths=None):
    """Citations roll-up matrix with per-column heatmap and a highlighted brand row.

    rows: list of lists. Row 0 is the header. Each subsequent row is:
        [player_name, type_label, *numeric_values, total]
    where type_label is one of 'Operator', 'Affiliate', or 'Brand'. The first
    numeric column starts at index 2; the Total column is the last one. The
    Total column is left neutral (no heatmap) so it stays readable as a sort
    signal.

    brand_row_label: optional. If a row's type_label equals 'Brand', the row
    gets a red left rule to distinguish the client's current position from
    the comparison set.

    col_widths: optional list of column widths in inches-aware units. Defaults
    to a layout tuned for ~7.3" body width and 10 columns total.
    """
    # Per-column max for heatmap intensity (skip the Total column at last index)
    n_cols = len(rows[0])
    total_idx = n_cols - 1
    col_max = [0] * n_cols
    for r in rows[1:]:
        for j in range(2, total_idx):
            if isinstance(r[j], (int, float)) and r[j] > col_max[j]:
                col_max[j] = r[j]

    def heat(val, cmax):
        """Pale-to-strong violet based on value share of column max."""
        if not cmax or not val:
            return None
        t = min(1.0, val / cmax)
        # interpolate from very pale (#f8f3ff) to strong violet (#a77aff)
        r = int(248 - (248 - 167) * t)
        g = int(243 - (243 - 122) * t)
        b = int(255 - (255 - 255) * t)
        return f'#{r:02x}{g:02x}{b:02x}'

    rendered = []
    cell_bg = {}
    brand_row_index = None
    for i, row in enumerate(rows):
        cells = []
        for j, cell in enumerate(row):
            if i == 0:
                cells.append(Paragraph(f'<b><font color="#7e7e80" size="7.5">{cell}</font></b>', BODY_XS))
            elif j == 0:
                cells.append(Paragraph(f'<b><font size="7.5">{cell}</font></b>', BODY_XS))
            elif j == 1:
                color = '#9747ff' if cell == 'Affiliate' else ('#d80027' if cell == 'Brand' else '#583b9d')
                cells.append(Paragraph(f'<font face="Courier-Bold" color="{color}" size="7">{cell.upper()}</font>', BODY_XS))
            else:
                is_brand = row[1] == 'Brand'
                if isinstance(cell, (int, float)):
                    display = f'~{cell:,}' if is_brand and cell > 0 else (f'{cell:,}' if cell else '0')
                else:
                    display = str(cell)
                cells.append(Paragraph(f'<font face="Courier" size="7.5">{display}</font>', BODY_XS))
                if 2 <= j < total_idx and isinstance(cell, (int, float)):
                    c = heat(cell, col_max[j])
                    if c:
                        cell_bg[(j, i)] = c
        if row[1] == 'Brand':
            brand_row_index = i
        rendered.append(cells)

    if col_widths is None:
        # Default layout: 10 columns assumed (matches the canonical roll-up shape).
        col_widths = [1.55 * inch, 0.7 * inch, 0.55 * inch, 0.65 * inch, 0.5 * inch,
                      0.55 * inch, 0.55 * inch, 0.55 * inch, 0.7 * inch, 0.6 * inch]
    t = Table(rendered, colWidths=col_widths)
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), BG_SUNKEN),
        ('LINEBELOW', (0, 0), (-1, -1), 0.3, BORDER_SOFT),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4), ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]
    for (col, row_i), color in cell_bg.items():
        style_cmds.append(('BACKGROUND', (col, row_i), (col, row_i), HexColor(color)))
    if brand_row_index is not None:
        style_cmds.append(('LINEBEFORE', (0, brand_row_index), (0, brand_row_index), 2.5, P0_BG))
        style_cmds.append(('FONT', (0, brand_row_index), (1, brand_row_index), 'Helvetica-Bold', 8))
    t.setStyle(TableStyle(style_cmds))
    return t


def pattern_card(title, url, body, stat, avail):
    """Render a single competitor-pattern card (sunken background, accent rule).

    Used for the operator-pattern cards in section 03 and the affiliate
    aggregator-tactic cards in section 04.
    """
    cells = [
        [Paragraph(f'<b>{title}</b>', BODY)],
        [Paragraph(f'<font face="Courier" size="8" color="#583b9d">{url}</font>', URL)],
        [Paragraph(body, BODY_S)],
    ]
    if stat:
        cells.append([Paragraph(f'<font face="Courier" size="8" color="#7e7e80">{stat}</font>', META)])
    pt = Table(cells, colWidths=[avail])
    pt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), BG_SUNKEN),
        ('BOX', (0, 0), (-1, -1), 0.4, BORDER_SOFT),
        ('LEFTPADDING', (0, 0), (-1, -1), 12), ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (0, 0), 8), ('BOTTOMPADDING', (0, -1), (-1, -1), 8),
    ]))
    return pt


def make_table(data, col_widths, num_cols=None, font_size=8.5):
    num_cols = num_cols or []
    style = TableStyle([
        ('FONT', (0,0), (-1,0), 'Helvetica-Bold', 8.5),
        ('TEXTCOLOR', (0,0), (-1,0), FG_2),
        ('BACKGROUND', (0,0), (-1,0), BG_SUNKEN),
        ('TEXTCOLOR', (0,1), (-1,-1), FG),
        ('FONT', (0,1), (-1,-1), 'Helvetica', font_size),
        ('LINEBELOW', (0,0), (-1,-1), 0.4, BORDER_SOFT),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 6), ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ])
    for col in num_cols:
        style.add('ALIGN', (col, 0), (col, -1), 'RIGHT')
        style.add('FONT', (col, 1), (col, -1), 'Courier', font_size)
    t = Table(data, colWidths=col_widths)
    t.setStyle(style)
    return t

def alert_box(title, body, avail):
    t = Table([
        [Paragraph(f'<b>{title}</b>', BODY_S)],
        [Paragraph(body, BODY_S)],
    ], colWidths=[avail])
    t.setStyle(TableStyle([
        ('LINEBEFORE', (0,0), (0,-1), 2.5, ACCENT),
        ('BOX', (0,0), (-1,-1), 0.4, BORDER),
        ('LEFTPADDING', (0,0), (-1,-1), 12), ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (0,0), 8), ('BOTTOMPADDING', (0,-1), (-1,-1), 8),
    ]))
    return t

def gap_head(priority, title, avail):
    chip_color = {'P0': (P0_BG, P0_FG), 'P1': (P1_BG, P1_FG), 'P2': (P2_BG, P2_FG)}[priority]
    chip = Chip(priority, chip_color[0], chip_color[1])
    head = Table([[chip, Paragraph(f'<b><font size="13">{title}</font></b>', BODY)]],
                 colWidths=[40, avail-40])
    head.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    return head

def gap_block(priority, title, url, meta, whats_there, edits):
    flowables = [gap_head(priority, title, PAGE_W - 2*MARGIN), Spacer(1, 4),
                 Paragraph(f'<font face="Courier" size="8" color="#583b9d">{url}</font>', URL),
                 Paragraph(f'<font color="#7e7e80" size="8">{meta}</font>', META)]
    if whats_there:
        flowables.append(Paragraph("<b>What's there now</b>", LBL))
        flowables.append(Paragraph(whats_there, BODY_S))
    flowables.append(Paragraph('<b>Specific edits</b>', LBL))
    for edit in edits:
        flowables.append(Paragraph(f'• {edit}', BODY_S))
    flowables.append(HRule(color=BORDER_SOFT, space=4))
    return flowables

def proposed_block(priority, urls, body, avail):
    chip_color = {'P0': (P0_BG, P0_FG), 'P1': (P1_BG, P1_FG), 'P2': (P2_BG, P2_FG)}[priority]
    chip = Chip(priority, chip_color[0], chip_color[1])
    url_paras = [Paragraph(f'<font face="Courier" size="9" color="#9747ff"><b>{u}</b></font>', BODY_S) for u in urls]
    head = Table([[chip, url_paras]], colWidths=[40, avail-40])
    head.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 2), ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    rows = [[head], [Paragraph(body, BODY_S)]]
    block = Table(rows, colWidths=[avail])
    block.setStyle(TableStyle([
        ('LINEBEFORE', (0,0), (0,-1), 2.5, ACCENT),
        ('BACKGROUND', (0,0), (-1,-1), BG_SUNKEN),
        ('BOX', (0,0), (-1,-1), 0.4, BORDER_SOFT),
        ('LEFTPADDING', (0,0), (-1,-1), 10), ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (0,0), 6), ('BOTTOMPADDING', (0,-1), (-1,-1), 6),
    ]))
    block.splitByRow = 1
    return [block, Spacer(1, 6)]

def phase_table(rows):
    data = [['Page', 'Type', 'Priority', 'Action']] + rows
    t = Table(data, colWidths=[2.7*inch, 0.7*inch, 0.6*inch, 2.2*inch])
    style = TableStyle([
        ('FONT', (0,0), (-1,0), 'Helvetica-Bold', 8.5),
        ('TEXTCOLOR', (0,0), (-1,0), FG_2),
        ('BACKGROUND', (0,0), (-1,0), BG_SUNKEN),
        ('TEXTCOLOR', (0,1), (-1,-1), FG),
        ('FONT', (0,1), (-1,-1), 'Helvetica', 8),
        ('LINEBELOW', (0,0), (-1,-1), 0.4, BORDER_SOFT),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (2,1), (2,-1), 'CENTER'),
        ('LEFTPADDING', (0,0), (-1,-1), 6), ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ])
    for i, r in enumerate(rows, start=1):
        p = r[2]
        if p == 'P0':
            style.add('BACKGROUND', (2,i), (2,i), P0_BG); style.add('TEXTCOLOR', (2,i), (2,i), white)
            style.add('FONT', (2,i), (2,i), 'Courier-Bold', 8)
        elif p == 'P1':
            style.add('BACKGROUND', (2,i), (2,i), P1_BG); style.add('FONT', (2,i), (2,i), 'Courier-Bold', 8)
        elif p == 'P2':
            style.add('BACKGROUND', (2,i), (2,i), P2_BG); style.add('FONT', (2,i), (2,i), 'Courier-Bold', 8)
    t.setStyle(style); return t

def playbook(num, slug, title, target_words, sample_prompts, sections, faqs, schema, links, sample_hero=None):
    """Returns a list of flowables for one P0 page playbook."""
    avail = PAGE_W - 2*MARGIN
    out = [Spacer(1, 14), HRule(color=ACCENT, thickness=1.5, space=2), Spacer(1, 4)]
    chip = Chip('P0', P0_BG, P0_FG)
    head = Table([[chip, Paragraph(f'<b><font size="13">{num} . {title}</font></b>', BODY)]], colWidths=[40, avail-40])
    head.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    out.append(head)
    out.append(Paragraph(f'<font face="Courier" size="9" color="#9747ff"><b>{slug}</b></font> <font color="#7e7e80" size="8">. target ~{target_words} words</font>', BODY_S))
    out.append(Paragraph(f'<font color="#7e7e80" size="8"><b>Target queries from prompt data:</b> {sample_prompts}</font>', META))
    if sample_hero:
        out.append(Paragraph('SAMPLE HERO COPY', PLAY_LBL))
        for line in sample_hero:
            out.append(Paragraph(f'<i>{line}</i>', BODY_S))
    out.append(Paragraph('PAGE OUTLINE. SECTION BY SECTION', PLAY_LBL))
    for sec in sections:
        out.append(Paragraph(f'<b>{sec[0]}</b>', BODY_XS))
        out.append(Paragraph(sec[1], BODY_XS))
    out.append(Paragraph('FAQ. Q&amp;AS TO PUBLISH', PLAY_LBL))
    for q, a in faqs:
        out.append(Paragraph(f'<b>Q. {q}</b>', BODY_XS))
        out.append(Paragraph(f'A. {a}', BODY_XS))
    out.append(Paragraph('SCHEMA MARKUP', PLAY_LBL))
    out.append(Paragraph(schema, BODY_XS))
    out.append(Paragraph('CROSS-LINKS', PLAY_LBL))
    out.append(Paragraph(links, BODY_XS))
    return out

# ============================================================================
# Page templates
# ============================================================================
class GEOReportDoc(BaseDocTemplate):
    def __init__(self, filename, logo_path=None, **kw):
        BaseDocTemplate.__init__(self, filename, pagesize=letter,
                                 leftMargin=MARGIN, rightMargin=MARGIN,
                                 topMargin=MARGIN, bottomMargin=MARGIN)
        self.logo_path = logo_path
        body_frame = Frame(MARGIN, MARGIN+30, PAGE_W-2*MARGIN, PAGE_H-2*MARGIN-50, id='body')
        cover_frame = Frame(MARGIN, MARGIN, PAGE_W-2*MARGIN, PAGE_H-2*MARGIN, id='cover')
        self.addPageTemplates([
            PageTemplate(id='cover', frames=[cover_frame], onPage=self._on_cover),
            PageTemplate(id='body', frames=[body_frame], onPage=self._on_body),
        ])
        self.header_text = ''  # set per-engagement before .build()

    def _on_cover(self, c, doc):
        if self.logo_path and Path(self.logo_path).exists():
            c.drawImage(self.logo_path, MARGIN, PAGE_H - MARGIN - 32,
                        width=130, height=27, mask='auto', preserveAspectRatio=True)
        else:
            c.setFont('Helvetica-Bold', 14)
            c.setFillColor(FG)
            c.drawString(MARGIN, PAGE_H - MARGIN - 20, 'GEO')

    def _on_body(self, c, doc):
        c.setFont('Helvetica', 8); c.setFillColor(FG_2)
        c.drawString(MARGIN, PAGE_H - MARGIN + 18, self.header_text)
        c.drawRightString(PAGE_W - MARGIN, PAGE_H - MARGIN + 18, doc.dateline if hasattr(doc, 'dateline') else '')
        c.setStrokeColor(BORDER_SOFT); c.setLineWidth(0.4)
        c.line(MARGIN, PAGE_H - MARGIN + 12, PAGE_W - MARGIN, PAGE_H - MARGIN + 12)
        c.setStrokeColor(BORDER_SOFT)
        c.line(MARGIN, MARGIN + 16, PAGE_W - MARGIN, MARGIN + 16)
        if self.logo_path and Path(self.logo_path).exists():
            c.drawImage(self.logo_path, MARGIN, MARGIN - 4, width=70, height=15, mask='auto', preserveAspectRatio=True)
        else:
            c.setFont('Helvetica-Bold', 8)
            c.setFillColor(FG_2)
            c.drawString(MARGIN, MARGIN + 2, 'GEO')
        c.setFont('Courier', 8); c.setFillColor(FG_3)
        c.drawCentredString(PAGE_W/2, MARGIN + 2, f'{doc.page:02d}')
        c.drawRightString(PAGE_W - MARGIN, MARGIN + 2, 'CONFIDENTIAL')

# ============================================================================
# build(). Orchestrates the full report
# ============================================================================
def build(report, kpis, findings, topic_data, owned_data, comp_data, patterns,
          gap_blocks, proposed, phases, playbooks, alerts, output_path=None,
          logo_path=None, prepared_by='Yolando'):
    """Render the full sitemap-optimization PDF.

    Args:
        report: dict with keys: title, subtitle, dateline, header_text,
                eyebrow_label (e.g. "MINTED SEARCH GROUP · GEO OPPORTUNITY PLAN · Q2 2026")
        kpis: list of 4 (label, number, sub, accent_bool) tuples
        findings: list of (headline, body) tuples. 5-6 items
        topic_data: [['Topic cluster', 'Executions', 'Brand %', 'Comp %', 'Funnel skew'], ...]
        owned_data: [['URL', 'Citations', 'Notes'], ...]
        comp_data:  [['URL', 'Domain', 'Citations', 'Pattern'], ...]
        patterns:   list of (title, url_string, body, stat_or_None) tuples. 4 patterns
        gap_blocks: list of dicts with keys: priority, title, url, meta, whats_there, edits
                    First page gap_blocks (2-3 of them) followed by an optional
                    "continued" page break + remaining ones.
        proposed:   dict with keys: tier1, tier2, tier3, tier4. Each a list of
                    (priority, urls_list, body) tuples
        phases:     list of 3 (heading, intro, rows) tuples
        playbooks:  list of dicts matching the playbook() signature
        alerts:     dict with keys: about_dominant_page, schema_markup,
                    crosslink_layer, playbooks_intro
    """
    doc = GEOReportDoc(output_path or OUT, logo_path=logo_path or LOGO_PATH)
    doc.header_text = report.get('header_text', '')
    doc.dateline = report.get('dateline', '')
    avail = PAGE_W - 2*MARGIN
    story = []

    # Cover
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph(report['eyebrow_label'], COVER_EYE))
    story.append(Paragraph(report['title'], COVER_TITLE))
    story.append(Paragraph(report['subtitle'], COVER_SUB))
    story.append(Spacer(1, 2.5*inch))
    story.append(Paragraph(f'<b>Prepared by {prepared_by}</b>', BODY))
    story.append(Paragraph(f'<font face="Courier" size="8" color="#a3a3a6">{report["dateline"]}</font>', BODY))
    story.append(HRFlowable(width=60, thickness=3, color=ACCENT, hAlign='LEFT', spaceBefore=4, spaceAfter=4))

    # Executive summary
    story.append(NextPageTemplate('body'))
    story.append(PageBreak())
    story.append(Eyebrow('01 · Executive summary'))
    story.append(Paragraph(report['exec_h1'], H1))
    story.append(Paragraph(report['exec_lead'], LEAD))
    kpi_w = (avail - 18) / 4
    kpi_table = Table([[KPICard(label, num, sub, kpi_w, accent=acc) for label, num, sub, acc in kpis]],
                      colWidths=[kpi_w]*4)
    kpi_table.setStyle(TableStyle([
        ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(kpi_table); story.append(Spacer(1, 12))
    story.append(Paragraph('Key findings', H3))
    for h, b in findings:
        story.append(Paragraph(f'<b>{h}</b>', BODY))
        story.append(Paragraph(b, BODY_S))
        story.append(Spacer(1, 4))

    # Section 02. Where the brand shows up today
    story.append(PageBreak())
    story.append(Eyebrow('02 · Where the brand shows up today'))
    story.append(Paragraph(report['s02_h1'], H1))
    story.append(Paragraph(report['s02_lead'], LEAD))
    story.append(Paragraph('Mention rate by topic and funnel', H2))
    story.append(Paragraph(report['s02_topic_intro'], BODY))
    story.append(make_table(topic_data, [2.6*inch, 0.9*inch, 0.7*inch, 0.7*inch, 1.0*inch], num_cols=[1,2,3]))
    story.append(Paragraph('Every brand page that has earned a citation', H2))
    story.append(Paragraph(report['s02_owned_intro'], BODY))
    story.append(make_table(owned_data, [2.4*inch, 0.7*inch, 3.6*inch], num_cols=[1]))
    story.append(Spacer(1, 6))
    story.append(alert_box(*alerts['about_dominant_page'], avail))

    # Section 03. Competitor patterns
    story.append(PageBreak())
    story.append(Eyebrow('03 · What competitor pages win citations'))
    story.append(Paragraph(report['s03_h1'], H1))
    story.append(Paragraph(report['s03_lead'], LEAD))
    story.append(Paragraph('Top cited competitor URLs', H2))
    story.append(make_table(comp_data, [2.7*inch, 1.4*inch, 0.7*inch, 1.4*inch], num_cols=[2], font_size=8))
    story.append(Paragraph('The four patterns competitors are exploiting', H2))
    for title, url, body, stat in patterns:
        cells = [
            [Paragraph(f'<b>{title}</b>', BODY)],
            [Paragraph(f'<font face="Courier" size="8" color="#583b9d">{url}</font>', URL)],
            [Paragraph(body, BODY_S)],
        ]
        if stat:
            cells.append([Paragraph(f'<font face="Courier" size="8" color="#7e7e80">{stat}</font>', META)])
        pt = Table(cells, colWidths=[avail])
        pt.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), BG_SUNKEN),
            ('BOX', (0,0), (-1,-1), 0.4, BORDER_SOFT),
            ('LEFTPADDING', (0,0), (-1,-1), 12), ('RIGHTPADDING', (0,0), (-1,-1), 12),
            ('TOPPADDING', (0,0), (0,0), 8), ('BOTTOMPADDING', (0,-1), (-1,-1), 8),
        ]))
        story.append(pt); story.append(Spacer(1, 8))

    # Section 04. Sitemap audit (existing pages)
    story.append(PageBreak())
    story.append(Eyebrow('04 · Sitemap audit · existing pages to deepen'))
    story.append(Paragraph(report['s04_h1'], H1))
    story.append(Paragraph(report['s04_lead'], LEAD))
    # Render gap_blocks split into pages (typical: first 2-3 on page 1, rest on page 2)
    split_at = report.get('gap_split_index', 2)
    for gb in gap_blocks[:split_at]:
        for fl in gap_block(gb['priority'], gb['title'], gb['url'], gb['meta'], gb['whats_there'], gb['edits']):
            story.append(fl)
    if len(gap_blocks) > split_at:
        story.append(PageBreak())
        story.append(Eyebrow('04 · Sitemap audit · continued'))
        for gb in gap_blocks[split_at:]:
            for fl in gap_block(gb['priority'], gb['title'], gb['url'], gb['meta'], gb['whats_there'], gb['edits']):
                story.append(fl)

    # Section 05. New pages strategy
    story.append(PageBreak())
    story.append(Eyebrow('05 · New pages · the location stack'))
    story.append(Paragraph(report['s05_t1_h1'], H1))
    story.append(Paragraph(report['s05_t1_lead'], LEAD))
    story.append(Paragraph('Tier 1 · City landing pages', H2))
    story.append(Paragraph(report['s05_t1_intro'], BODY))
    for pri, urls, body in proposed['tier1']:
        for fl in proposed_block(pri, urls, body, avail):
            story.append(fl)
    story.append(Spacer(1, 6))
    story.append(alert_box(*alerts['schema_markup'], avail))

    story.append(PageBreak())
    story.append(Eyebrow('05 · New pages · practice × city, role-level, trust'))
    story.append(Paragraph(report['s05_t234_h1'], H1))
    story.append(Paragraph(report['s05_t234_lead'], LEAD))
    story.append(Paragraph('Tier 2 · Practice-area × city compound pages', H2))
    for pri, urls, body in proposed['tier2']:
        for fl in proposed_block(pri, urls, body, avail):
            story.append(fl)
    story.append(Paragraph('Tier 3 · Role-specific landing pages', H2))
    for pri, urls, body in proposed['tier3']:
        for fl in proposed_block(pri, urls, body, avail):
            story.append(fl)
    story.append(Paragraph('Tier 4 · Trust and credentials pages', H2))
    for pri, urls, body in proposed['tier4']:
        for fl in proposed_block(pri, urls, body, avail):
            story.append(fl)

    # Section 06. Phased roadmap
    story.append(PageBreak())
    story.append(Eyebrow('06 · Phased roadmap'))
    story.append(Paragraph(report['s06_h1'], H1))
    story.append(Paragraph(report['s06_lead'], LEAD))
    for heading, intro, rows in phases:
        story.append(Paragraph(heading, H2))
        story.append(Paragraph(intro, BODY))
        story.append(phase_table(rows))
    story.append(Paragraph('What success looks like', H2))
    story.append(Paragraph(report['s06_success'], BODY))
    story.append(Spacer(1, 6))
    story.append(alert_box(*alerts['crosslink_layer'], avail))

    # Section 07. P0 page playbooks
    story.append(PageBreak())
    story.append(Eyebrow('07 · P0 page playbooks'))
    story.append(Paragraph(report['s07_h1'], H1))
    story.append(Paragraph(alerts['playbooks_intro'][0], LEAD))
    story.append(Paragraph(alerts['playbooks_intro'][1], BODY))

    # Index table
    story.append(Spacer(1, 8))
    idx_data = [['§', 'Page', 'Priority']]
    for pb in playbooks:
        idx_data.append([pb['num'], pb['title'], 'P0'])
    idx_t = Table(idx_data, colWidths=[0.5*inch, 5.5*inch, 0.7*inch])
    idx_style = TableStyle([
        ('FONT', (0,0), (-1,0), 'Helvetica-Bold', 8.5),
        ('TEXTCOLOR', (0,0), (-1,0), FG_2),
        ('BACKGROUND', (0,0), (-1,0), BG_SUNKEN),
        ('FONT', (0,1), (0,-1), 'Courier-Bold', 9),
        ('FONT', (1,1), (1,-1), 'Helvetica', 9),
        ('LINEBELOW', (0,0), (-1,-1), 0.4, BORDER_SOFT),
        ('LEFTPADDING', (0,0), (-1,-1), 6), ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('ALIGN', (2,1), (2,-1), 'CENTER'),
    ])
    for i in range(1, len(idx_data)):
        idx_style.add('BACKGROUND', (2,i), (2,i), P0_BG)
        idx_style.add('TEXTCOLOR', (2,i), (2,i), white)
        idx_style.add('FONT', (2,i), (2,i), 'Courier-Bold', 8)
    idx_t.setStyle(idx_style)
    story.append(idx_t)

    # Render each playbook on its own page
    for pb in playbooks:
        story.append(PageBreak())
        for fl in playbook(pb['num'], pb['slug'], pb['title'], pb['target_words'],
                           pb['sample_prompts'], pb['sections'], pb['faqs'],
                           pb['schema'], pb['links'], pb.get('sample_hero')):
            story.append(fl)

    # Closing alert
    story.append(Spacer(1, 12))
    story.append(alert_box(
        'Each playbook is a brief, not the final published copy.',
        'Treat sample hero copy and FAQ A. lines as drafts. The real value is the section structure, the entity coverage (city names, sub-disciplines, credentials), and the schema/cross-link wiring. Get those right and the LLMs will follow.', avail))

    doc.build(story)
    print(f'Wrote {output_path or OUT}')


if __name__ == '__main__':
    print('This module is a template. Import build() and pass in your data dicts.')
    print('See the docstring at the top of this file for the data structure shapes.')
    print('After build() finishes, run the empty-page cleanup pass with pypdf.')
