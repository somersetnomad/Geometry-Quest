"""Generate Geometry Quest worksheets and answer sheets (A4 PDFs)."""
import math, os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import simpleSplit

pdfmetrics.registerFont(TTFont('Sans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('Sans-B', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Mono', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'))

W, H = A4
M = 1.6 * cm
INK = HexColor('#13173A'); MUTED = HexColor('#566089'); LINE = HexColor('#C9D3EA'); SOFT = HexColor('#EEF3FF')
ANS = HexColor('#00876A'); PINK = HexColor('#FF3D7F'); BLUE = HexColor('#2F6BFF'); YEL = HexColor('#FFB000')
COLS = {'c1': '#FF3D7F', 'c2': '#2F6BFF', 'c3': '#FFB000', 'c4': '#00A88F', 'c5': '#7C4DFF'}
OUT = '/home/claude/worksheets'
os.makedirs(OUT, exist_ok=True)

WORLDS = [
 ('w01', 'Points & Lines', 'c2'), ('w02', 'Angles', 'c1'), ('w03', 'Protractor Skills', 'c5'), ('w04', 'Angle Rules', 'c4'),
 ('w05', 'Triangles', 'c3'), ('w06', 'Polygons', 'c5'), ('w07', 'Circles & π', 'c2'), ('w08', '3D Shapes & Nets', 'c3'),
 ('w09', 'Parallel Lines', 'c4'), ('w10', 'Symmetry', 'c1'), ('w11', 'Coordinates', 'c2'), ('w12', 'Transformations', 'c5'),
 ('w13', 'Constructions', 'c3'), ('w14', 'Congruence', 'c5'), ('w15', 'Pythagoras & √2', 'c1'), ('w16', 'Fractals', 'c4')]


def mascot(c, x, y, s=1.0):
    """Vertex, the guide: a rounded yellow triangle with eyes. (x,y)=bottom centre."""
    c.saveState(); c.translate(x, y); c.scale(s, s)
    p = c.beginPath(); p.moveTo(0, 46); p.lineTo(24, 4); p.lineTo(-24, 4); p.close()
    c.setFillColor(YEL); c.setStrokeColor(INK); c.setLineWidth(2.4); c.setLineJoin(1); c.drawPath(p, fill=1, stroke=1)
    for ex in (-7, 7):
        c.setFillColor(white); c.circle(ex, 20, 5, fill=1, stroke=1); c.setFillColor(INK); c.circle(ex, 19.5, 2.3, fill=1, stroke=0)
    c.setFillColor(PINK); c.circle(0, 47, 3.2, fill=1, stroke=1)
    c.setLineWidth(1.8); p = c.beginPath(); p.moveTo(-5, 11); p.curveTo(-2, 7, 2, 7, 5, 11); c.drawPath(p, stroke=1, fill=0)
    c.restoreState()


class Sheet:
    def __init__(self, c, idx, name, col, answers):
        self.c, self.idx, self.name, self.col, self.answers = c, idx, name, HexColor(COLS[col]), answers
        self.n = 0; self.page = 0
        self.new_page(first=True)

    def new_page(self, first=False):
        c = self.c
        if not first:
            c.showPage()
        self.page += 1
        if first:
            c.setFillColor(self.col); c.roundRect(M, H - M - 3.2 * cm, W - 2 * M, 3.2 * cm, 14, fill=1, stroke=0)
            c.setFillColor(INK); c.setFont('Sans-B', 9); c.drawString(M + 0.6 * cm, H - M - 0.9 * cm, f'GEOMETRY QUEST · WORLD {self.idx}')
            c.setFont('Sans-B', 24); c.drawString(M + 0.6 * cm, H - M - 1.9 * cm, self.name)
            c.setFont('Sans-B', 11); c.drawString(M + 0.6 * cm, H - M - 2.65 * cm, 'ANSWER SHEET · for the grown-up' if self.answers else 'WORKSHEET')
            mascot(c, W - M - 1.6 * cm, H - M - 2.9 * cm, 1.2)
            self.y = H - M - 4.0 * cm
            if not self.answers:
                c.setFont('Sans', 10); c.setFillColor(MUTED)
                c.drawString(M, self.y, 'Name ______________________________     Date ________________     Stars I give myself:  ☆ ☆ ☆')
                self.y -= 0.9 * cm
            else:
                c.setFont('Sans', 9.5); c.setFillColor(MUTED)
                c.drawString(M, self.y, 'Answers are shown in green. “Check” means look at the child’s drawing or measuring: allow ±2° or ±2 mm.')
                self.y -= 0.9 * cm
        else:
            c.setFillColor(self.col); c.rect(M, H - M - 0.25 * cm, W - 2 * M, 0.25 * cm, fill=1, stroke=0)
            c.setFillColor(MUTED); c.setFont('Sans-B', 9)
            c.drawString(M, H - M - 0.8 * cm, f'World {self.idx} · {self.name} · {"Answers" if self.answers else "Worksheet"} (continued)')
            self.y = H - M - 1.5 * cm
        c.setFont('Sans', 8); c.setFillColor(MUTED)
        c.drawString(M, 0.9 * cm, f'Geometry Quest · World {self.idx} · page {self.page}')
        c.drawRightString(W - M, 0.9 * cm, 'Adapted from Geometry for Elementary School, Wikibooks, CC BY-SA 3.0')

    def q(self, text, space):
        """Write a numbered question; reserve `space` below it. Returns (top_y_of_space, bottom_y)."""
        c = self.c
        lines = simpleSplit(text, 'Sans', 11.5, W - 2 * M - 1.1 * cm)
        need = len(lines) * 15 + space + 14
        if self.y - need < 1.8 * cm:
            self.new_page()
        self.n += 1
        c.setFillColor(INK); c.circle(M + 0.32 * cm, self.y - 4, 0.32 * cm, fill=1, stroke=0)
        c.setFillColor(white); c.setFont('Sans-B', 10); c.drawCentredString(M + 0.32 * cm, self.y - 7.5, str(self.n))
        c.setFillColor(INK); c.setFont('Sans', 11.5)
        yy = self.y - 8
        for ln in lines:
            c.drawString(M + 1.0 * cm, yy, ln); yy -= 15
        top = yy - 2
        self.y = top - space - 12
        return top, top - space

    def a(self, x, y, text, size=11, anchor='l'):
        if not self.answers:
            return
        c = self.c; c.setFillColor(ANS); c.setFont('Sans-B', size)
        {'l': c.drawString, 'c': c.drawCentredString, 'r': c.drawRightString}[anchor](x, y, text)

    def lines(self, top, n, gap=0.85 * cm, x0=None, x1=None, answer=None):
        c = self.c; c.setStrokeColor(LINE); c.setLineWidth(0.8)
        x0 = x0 or M + 1.0 * cm; x1 = x1 or W - M
        for i in range(n):
            yy = top - (i + 1) * gap
            c.line(x0, yy, x1, yy)
        if answer:
            self.a(x0 + 4, top - gap + 4, answer)

    def blank(self, x, y, w=2.2 * cm, answer=None, unit=''):
        c = self.c; c.setStrokeColor(INK); c.setLineWidth(0.8); c.line(x, y, x + w, y)
        if unit:
            c.setFillColor(INK); c.setFont('Sans', 11); c.drawString(x + w + 3, y + 2, unit)
        if answer is not None:
            self.a(x + 4, y + 3, str(answer))


# ---------- drawing helpers ----------
def pt(x, y, a, r):
    t = math.radians(a); return x + r * math.cos(t), y + r * math.sin(t)


def draw_angle(c, x, y, a0, a1, L=4.2 * cm, arc=None, arc_r=0.7 * cm, label=None, col=INK, w=1.6):
    c.setStrokeColor(col); c.setLineWidth(w); c.setLineCap(1)
    c.line(x, y, *pt(x, y, a0, L)); c.line(x, y, *pt(x, y, a1, L))
    c.setFillColor(col); c.circle(x, y, 2.2, fill=1, stroke=0)
    if arc:
        lo, hi = arc
        c.setLineWidth(1.1); c.arc(x - arc_r, y - arc_r, x + arc_r, y + arc_r, startAng=lo, extent=hi - lo)
    if label:
        mid = (arc[0] + arc[1]) / 2 if arc else (a0 + a1) / 2
        lx, ly = pt(x, y, mid, arc_r + 0.45 * cm)
        c.setFont('Sans-B', 11); c.setFillColor(col); c.drawCentredString(lx, ly - 4, label)


def grid(c, x0, y0, u, lo, hi, axes=True, labels=True):
    """Coordinate grid: origin at (x0,y0), unit u, from lo..hi on both axes."""
    c.setStrokeColor(LINE); c.setLineWidth(0.6)
    for i in range(lo, hi + 1):
        c.line(x0 + i * u, y0 + lo * u, x0 + i * u, y0 + hi * u); c.line(x0 + lo * u, y0 + i * u, x0 + hi * u, y0 + i * u)
    if axes:
        c.setStrokeColor(INK); c.setLineWidth(1.3)
        c.line(x0 + lo * u, y0, x0 + hi * u + 6, y0); c.line(x0, y0 + lo * u, x0, y0 + hi * u + 6)
        c.setFont('Sans-B', 9); c.setFillColor(INK)
        c.drawString(x0 + hi * u + 8, y0 - 3, 'x'); c.drawString(x0 - 3, y0 + hi * u + 9, 'y')
        if labels:
            c.setFont('Sans', 7); c.setFillColor(MUTED)
            for i in range(lo, hi + 1):
                if i == 0:
                    continue
                c.drawCentredString(x0 + i * u, y0 - 9, str(i)); c.drawRightString(x0 - 3, y0 + i * u - 2.5, str(i))
            c.drawString(x0 - 9, y0 - 9, '0')


def poly(c, pts, x0, y0, u, fill=None, stroke=INK, w=1.6, alpha=0.25, dash=None):
    p = c.beginPath(); p.moveTo(x0 + pts[0][0] * u, y0 + pts[0][1] * u)
    for q in pts[1:]:
        p.lineTo(x0 + q[0] * u, y0 + q[1] * u)
    p.close(); c.saveState(); c.setStrokeColor(stroke); c.setLineWidth(w)
    if dash:
        c.setDash(*dash)
    if fill is not None:
        c.setFillColor(fill); c.setFillAlpha(alpha)
    c.drawPath(p, fill=1 if fill is not None else 0, stroke=1); c.restoreState()


def squares(c, x, y, cells, u, fill=None):
    c.setStrokeColor(INK); c.setLineWidth(1.2)
    for (i, j) in cells:
        if fill:
            c.setFillColor(fill); c.rect(x + i * u, y + j * u, u, u, fill=1, stroke=1)
        else:
            c.rect(x + i * u, y + j * u, u, u, fill=0, stroke=1)


# ---------- worlds ----------
def w01(s):
    c = s.c
    top, bot = s.q('Name each one: line segment, ray or line.', 2.4 * cm)
    xs = [M + 1.2 * cm, M + 6.8 * cm, M + 12.4 * cm]
    for k, (x, kind, ans) in enumerate(zip(xs, ['seg', 'ray', 'line'], ['segment', 'ray', 'line'])):
        y = top - 0.9 * cm
        c.setStrokeColor(INK); c.setLineWidth(1.6); c.line(x, y, x + 4.2 * cm, y)
        c.setFillColor(INK)
        if kind == 'seg':
            c.circle(x, y, 2.6, fill=1); c.circle(x + 4.2 * cm, y, 2.6, fill=1)
        if kind in ('ray', 'line'):
            c.circle(x if kind == 'ray' else x + 1.4 * cm, y, 2.6, fill=1)
            p = c.beginPath(); p.moveTo(x + 4.2 * cm + 6, y); p.lineTo(x + 4.2 * cm - 4, y + 5); p.lineTo(x + 4.2 * cm - 4, y - 5); p.close(); c.drawPath(p, fill=1, stroke=0)
        if kind == 'line':
            p = c.beginPath(); p.moveTo(x - 6, y); p.lineTo(x + 4, y + 5); p.lineTo(x + 4, y - 5); p.close(); c.drawPath(p, fill=1, stroke=0)
        s.blank(x + 0.6 * cm, bot + 0.2 * cm, 3 * cm, ans)
    top, bot = s.q('Three of these points are collinear (on the same straight line). Which three? Use a ruler to check.', 4.2 * cm)
    pts = {'P': (1, 1), 'Q': (3.5, 2), 'R': (6, 3), 'S': (3, 3.4), 'T': (7.5, 0.6)}
    ox, oy = M + 1.4 * cm, bot + 0.2 * cm
    for k, (px, py) in pts.items():
        c.setFillColor(INK); c.circle(ox + px * cm, oy + py * cm * 0.85, 2.8, fill=1); c.setFont('Sans-B', 11); c.drawString(ox + px * cm + 6, oy + py * cm * 0.85 + 4, k)
    s.blank(W - M - 5 * cm, bot + 0.6 * cm, 4 * cm, 'P, Q and R')
    if s.answers:
        c.setStrokeColor(ANS); c.setDash(4, 3); c.line(ox + 1 * cm, oy + 0.85 * cm, ox + 6 * cm, oy + 3 * 0.85 * cm); c.setDash()
    top, bot = s.q('Measure line segment AB with a ruler. How long is it?', 1.6 * cm)
    x = M + 1.4 * cm; y = top - 0.8 * cm
    c.setStrokeColor(INK); c.setLineWidth(1.6); c.line(x, y, x + 7.5 * cm, y); c.setFillColor(INK)
    c.circle(x, y, 2.6, fill=1); c.circle(x + 7.5 * cm, y, 2.6, fill=1); c.setFont('Sans-B', 11); c.drawString(x - 4, y + 7, 'A'); c.drawString(x + 7.5 * cm - 4, y + 7, 'B')
    s.blank(W - M - 4 * cm, y - 2, 2.2 * cm, '7.5', 'cm')
    top, bot = s.q('How many different straight lines can you draw through two points?', 0.9 * cm)
    s.blank(M + 1.0 * cm, bot + 0.1 * cm, 2.5 * cm, 'exactly 1')
    top, bot = s.q('Draw a line segment exactly 6 cm long. Label its ends C and D.', 1.6 * cm)
    s.a(M + 1.0 * cm, bot + 0.6 * cm, 'Check: 6 cm, both ends labelled.')
    top, bot = s.q('Real-life hunt: name something at home that is like a ray, and something like a line segment.', 1.8 * cm)
    s.lines(top, 2, answer='e.g. ray: torch beam, sunbeam · segment: pencil, table edge')


def w02(s):
    c = s.c
    top, bot = s.q('Write acute, right, obtuse, straight or reflex under each angle.', 4.2 * cm)
    specs = [(0, 35, 'acute'), (0, 90, 'right'), (0, 130, 'obtuse'), (0, 180, 'straight'), (0, 250, 'reflex')]
    for k, (a0, a1, ans) in enumerate(specs):
        x = M + 1.8 * cm + k * 3.35 * cm; y = bot + 1.9 * cm
        draw_angle(c, x, y, a0, a1, L=1.45 * cm, arc=(a0, a1), arc_r=0.45 * cm)
        if a1 == 90:
            c.rect(x, y, 7, 7, fill=0, stroke=1)
        s.blank(x - 1.1 * cm, bot + 0.15 * cm, 2.3 * cm, ans)
    top, bot = s.q('What angle do the hands of a clock make at each time? (Think: 360° ÷ 12 = 30° per hour.)', 1.2 * cm)
    for k, (t, a) in enumerate([('3:00', 90), ('6:00', 180), ('2:00', 60), ('4:00', 120)]):
        x = M + 1.0 * cm + k * 4.1 * cm; c.setFillColor(INK); c.setFont('Sans-B', 11); c.drawString(x, bot + 0.45 * cm, t + ' →'); s.blank(x + 1.5 * cm, bot + 0.4 * cm, 1.6 * cm, a, '°')
    top, bot = s.q('Fill in the gaps.', 2.8 * cm)
    rows = [('Two angles that add up to 90° are called', 'complementary'), ('Two angles that add up to 180° are called', 'supplementary'),
            ('The complement of 35° is', '55°'), ('The supplement of 110° is', '70°')]
    for k, (t, a) in enumerate(rows):
        y = top - (k + 1) * 0.65 * cm; c.setFillColor(INK); c.setFont('Sans', 11); c.drawString(M + 1.0 * cm, y, t); s.blank(M + 1.2 * cm + c.stringWidth(t, 'Sans', 11), y, 3.2 * cm, a)
    top, bot = s.q('Turning. You face North. Which way are you facing after each turn (from North each time)?', 2.0 * cm)
    rows = [('a quarter turn clockwise (90°)', 'East'), ('a half turn (180°)', 'South'), ('270° clockwise', 'West')]
    for k, (t, a) in enumerate(rows):
        y = top - (k + 1) * 0.6 * cm; c.setFillColor(INK); c.setFont('Sans', 11); c.drawString(M + 1.0 * cm, y, t); s.blank(M + 8.5 * cm, y, 3 * cm, a)
    top, bot = s.q('Skater challenge: a “540” is how many full turns?', 0.9 * cm)
    s.blank(M + 1.0 * cm, bot + 0.1 * cm, 3 * cm, '1½ turns')


def w03(s):
    c = s.c
    top, bot = s.q('Measure each angle with a protractor. Put the centre on the corner and count up from the 0 on one arm. (Drawn to size: print at 100%.)', 11.2 * cm)
    boxes = [(M + 2.4 * cm, top - 4.9 * cm, 0, 40, '40', M + 1.0 * cm, top - 0.4 * cm), (M + 12.0 * cm, top - 4.9 * cm, 0, 125, '125', M + 9.4 * cm, top - 0.4 * cm),
             (M + 6.6 * cm, bot + 1.0 * cm, 180, 105, '75', M + 1.0 * cm, top - 5.8 * cm), (M + 12.4 * cm, bot + 1.0 * cm, 0, 160, '160', M + 9.4 * cm, top - 5.8 * cm)]
    for k, (x, y, a0, a1, ans, lx, ly) in enumerate(boxes):
        lo, hi = sorted([a0, a1])
        draw_angle(c, x, y, a0, a1, L=4.4 * cm, arc=(lo, hi), arc_r=0.6 * cm)
        c.setFont('Sans-B', 12); c.setFillColor(INK); c.drawString(lx, ly, 'abcd'[k] + ')')
        s.blank(x + (-2.8 if a0 == 180 else 0.4) * cm, y - 0.75 * cm, 1.8 * cm, ans, '°')
    top, bot = s.q('Use your protractor to draw these angles on the lines below. Mark the angle with an arc.', 4.4 * cm)
    for k, (deg, x) in enumerate([(50, M + 1.6 * cm), (135, M + 10.6 * cm)]):
        y = bot + 0.7 * cm; c.setStrokeColor(INK); c.setLineWidth(1.6)
        c.line(x, y, x + 5 * cm, y) if k == 0 else c.line(x, y, x + 5 * cm, y)
        c.setFillColor(INK); c.circle(x, y, 2.4, fill=1); c.setFont('Sans-B', 11); c.drawString(x + 2.5 * cm, y - 0.55 * cm, f'{"ab"[k]}) {deg}°')
        if s.answers:
            c.setStrokeColor(ANS); c.setLineWidth(1.6); c.line(x, y, *pt(x, y, deg, 3.4 * cm))
    top, bot = s.q('This is a reflex angle. Measure it. (Tip: measure the small angle, then take it away from 360°.)', 4.6 * cm)
    x, y = M + 5.5 * cm, bot + 2.3 * cm
    draw_angle(c, x, y, 0, 290, L=2.4 * cm, arc=(0, 290), arc_r=0.6 * cm)
    s.blank(M + 10 * cm, y, 2 * cm, '290', '°')
    s.a(M + 10 * cm, y - 0.7 * cm, '(small angle 70°, 360 − 70 = 290)', 9)
    top, bot = s.q('Sam measured an angle and wrote 140°. But the angle is clearly smaller than a right angle. What went wrong, and what is the real size?', 1.8 * cm)
    s.lines(top, 2, answer='Read the wrong scale. The angle is 180 − 140 = 40°.')


def w04(s):
    c = s.c
    top, bot = s.q('Two straight lines cross. Find a, b and c. Give a reason for each. (Not drawn to scale.)', 5.0 * cm)
    x, y = M + 4.0 * cm, bot + 2.4 * cm
    c.setStrokeColor(INK); c.setLineWidth(1.6)
    for a in (25, 115):
        c.line(*pt(x, y, a, 2.6 * cm), *pt(x, y, a + 180, 2.6 * cm))
    labels = [(70, '65°'), (160, 'a'), (250, 'b'), (340, 'c')]
    c.setFont('Sans-B', 12)
    for mid, t in labels:
        lx, ly = pt(x, y, mid, 1.0 * cm); c.setFillColor(PINK if t == '65°' else INK); c.drawCentredString(lx, ly - 4, t)
    for k, (t, a) in enumerate([('a =', '115° (angles on a straight line)'), ('b =', '65° (vertically opposite)'), ('c =', '115° (vertically opposite a)')]):
        yy = top - (k + 1) * 1.2 * cm; c.setFillColor(INK); c.setFont('Sans-B', 11); c.drawString(M + 8.5 * cm, yy, t); s.blank(M + 9.4 * cm, yy, 7 * cm, a)
    top, bot = s.q('These angles sit on a straight line. Find x.', 3.0 * cm)
    x, y = M + 4.5 * cm, bot + 0.6 * cm
    c.setStrokeColor(INK); c.setLineWidth(1.6); c.line(x - 3.5 * cm, y, x + 3.5 * cm, y)
    c.line(x, y, *pt(x, y, 48, 2.4 * cm)); c.line(x, y, *pt(x, y, 105, 2.4 * cm))
    c.setFont('Sans-B', 12)
    for mid, t in [(24, '48°'), (76.5, 'x'), (142.5, '75°')]:
        lx, ly = pt(x, y, mid, 1.1 * cm); c.setFillColor(PINK if t != 'x' else INK); c.drawCentredString(lx, ly - 4, t)
    s.blank(M + 10.5 * cm, y + 1 * cm, 2 * cm, '57', '°'); c.setFillColor(INK); c.setFont('Sans-B', 11); c.drawString(M + 9.6 * cm, y + 1 * cm + 2, 'x =')
    top, bot = s.q('These angles meet at a point. Find y.', 4.6 * cm)
    x, y = M + 4.5 * cm, bot + 2.3 * cm
    c.setStrokeColor(INK); c.setLineWidth(1.6)
    for a in (20, 120, 235):
        c.line(x, y, *pt(x, y, a, 2.0 * cm))
    c.setFont('Sans-B', 12)
    for mid, t in [(70, '100°'), (177.5, '115°'), (307.5, 'y')]:
        lx, ly = pt(x, y, mid, 0.95 * cm); c.setFillColor(PINK if t != 'y' else INK); c.drawCentredString(lx, ly - 4, t)
    c.setFillColor(INK); c.setFont('Sans-B', 11); c.drawString(M + 9.6 * cm, y + 2, 'y ='); s.blank(M + 10.5 * cm, y, 2 * cm, '145', '°')
    top, bot = s.q('Four equal angles meet at a point. How big is each one?', 0.9 * cm)
    s.blank(M + 1.0 * cm, bot + 0.1 * cm, 2 * cm, '90', '°')
    top, bot = s.q('Open a pair of scissors. Explain why the angle between the blades always equals the angle between the handles.', 1.8 * cm)
    s.lines(top, 2, answer='Two straight lines cross, so vertically opposite angles are equal.')


def w05(s):
    c = s.c
    top, bot = s.q('Find the missing angle in each triangle. (Not drawn to scale.)', 3.6 * cm)
    tris = [((0, 0), (3.6, 0), (1.6, 2.6), ['50°', '60°', '?'], '70'), ((0, 0), (3.4, 0), (0, 2.6), ['90°', '35°', '?'], '55'), ((0, 0), (3.6, 0), (1.8, 2.8), ['?', '?', '40°'], '70 each')]
    for k, (A, B, C, labs, ans) in enumerate(tris):
        ox, oy = M + 1.2 * cm + k * 5.6 * cm, bot + 0.9 * cm
        P = [(ox + A[0] * cm, oy + A[1] * cm), (ox + B[0] * cm, oy + B[1] * cm), (ox + C[0] * cm, oy + C[1] * cm)]
        p = c.beginPath(); p.moveTo(*P[0]); p.lineTo(*P[1]); p.lineTo(*P[2]); p.close(); c.setStrokeColor(INK); c.setLineWidth(1.6); c.drawPath(p, fill=0, stroke=1)
        cx_, cy_ = sum(q[0] for q in P) / 3, sum(q[1] for q in P) / 3
        c.setFont('Sans-B', 10)
        for q, t in zip(P, labs):
            lx, ly = q[0] + (cx_ - q[0]) * 0.32, q[1] + (cy_ - q[1]) * 0.32
            c.setFillColor(PINK if t != '?' else INK); c.drawCentredString(lx, ly - 3, t)
        if k == 1:
            c.rect(P[0][0], P[0][1], 8, 8, fill=0, stroke=1)
        if k == 2:
            for (u, v) in ((P[0], P[2]), (P[1], P[2])):
                mx, my = (u[0] + v[0]) / 2, (u[1] + v[1]) / 2; c.line(mx - 4, my - 3, mx + 4, my + 3)
        s.blank(ox + 0.4 * cm, bot + 0.1 * cm, 2.4 * cm, ans + '°')
    top, bot = s.q('Classify each triangle by its sides (equilateral, isosceles, scalene) and its angles (acute, right, obtuse).', 2.4 * cm)
    rows = [('sides 5, 5, 5 cm', 'equilateral, acute'), ('angles 90°, 45°, 45°', 'isosceles, right'), ('angles 120°, 40°, 20°', 'scalene, obtuse')]
    for k, (t, a) in enumerate(rows):
        y = top - (k + 1) * 0.7 * cm; c.setFillColor(INK); c.setFont('Sans', 11); c.drawString(M + 1.0 * cm, y, t); s.blank(M + 6.5 * cm, y, 7 * cm, a)
    top, bot = s.q('Area of a triangle = ½ × base × height. Work these out.', 1.6 * cm)
    for k, (b, h, a) in enumerate([(8, 5, 20), (12, 7, 42), (9, 4, 18)]):
        x = M + 1.0 * cm + k * 5.4 * cm; y = bot + 0.6 * cm; c.setFillColor(INK); c.setFont('Sans', 11); c.drawString(x, y + 0.6 * cm, f'base {b} cm, height {h} cm'); s.blank(x, y - 0.1 * cm, 2 * cm, a, 'cm²')
    top, bot = s.q('An equilateral triangle has sides of 7 cm. What is its perimeter?', 0.9 * cm)
    s.blank(M + 1.0 * cm, bot + 0.1 * cm, 2 * cm, 21, 'cm')
    top, bot = s.q('Experiment: draw any big triangle. Measure its three angles with a protractor and add them up. What do you get?', 2.0 * cm)
    s.lines(top, 2, answer='About 180° (within a few degrees because of measuring).')


def w06(s):
    c = s.c
    top, bot = s.q('Name the polygon with this many sides.', 1.4 * cm)
    for k, (n, a) in enumerate([(5, 'pentagon'), (6, 'hexagon'), (8, 'octagon'), (12, 'dodecagon')]):
        x = M + 1.0 * cm + k * 4.1 * cm; c.setFillColor(INK); c.setFont('Sans-B', 11); c.drawString(x, bot + 0.7 * cm, f'{n} sides'); s.blank(x, bot + 0.05 * cm, 3.3 * cm, a)
    top, bot = s.q('Angle total = (sides − 2) × 180°. Find the total of the inside angles.', 1.4 * cm)
    for k, (n, nm, a) in enumerate([(6, 'hexagon', 720), (8, 'octagon', 1080), (10, 'decagon', 1440)]):
        x = M + 1.0 * cm + k * 5.4 * cm; c.setFillColor(INK); c.setFont('Sans', 11); c.drawString(x, bot + 0.7 * cm, nm); s.blank(x, bot + 0.05 * cm, 2.4 * cm, a, '°')
    top, bot = s.q('Each inside angle of a regular polygon = angle total ÷ number of sides. Find one angle of a regular pentagon and a regular hexagon.', 1.0 * cm)
    c.setFillColor(INK); c.setFont('Sans', 11); c.drawString(M + 1.0 * cm, bot + 0.25 * cm, 'pentagon'); s.blank(M + 3.0 * cm, bot + 0.2 * cm, 2 * cm, 108, '°')
    c.drawString(M + 8.0 * cm, bot + 0.25 * cm, 'hexagon'); s.blank(M + 10.0 * cm, bot + 0.2 * cm, 2 * cm, 120, '°')
    top, bot = s.q('True or false?', 2.8 * cm)
    rows = [('A square is a rectangle.', 'true'), ('Every rectangle is a square.', 'false'), ('A rhombus has four equal sides.', 'true'), ('A trapezium has two pairs of parallel sides.', 'false')]
    for k, (t, a) in enumerate(rows):
        y = top - (k + 1) * 0.62 * cm; c.setFillColor(INK); c.setFont('Sans', 11); c.drawString(M + 1.0 * cm, y, t); s.blank(M + 11 * cm, y, 2.4 * cm, a)
    top, bot = s.q('Find: (a) the area of a parallelogram with base 9 cm and height 4 cm; (b) the perimeter of a 7 cm by 3 cm rectangle.', 1.0 * cm)
    c.setFont('Sans', 11); c.setFillColor(INK); c.drawString(M + 1.0 * cm, bot + 0.25 * cm, '(a)'); s.blank(M + 1.8 * cm, bot + 0.2 * cm, 2 * cm, 36, 'cm²')
    c.drawString(M + 8.0 * cm, bot + 0.25 * cm, '(b)'); s.blank(M + 8.8 * cm, bot + 0.2 * cm, 2 * cm, 20, 'cm')
    top, bot = s.q('Polygon hunt: find three polygons at home or outside. Name each one and say where you found it.', 2.6 * cm)
    s.lines(top, 3, answer='Any sensible answers, e.g. hexagon: nut on a bolt.')


def w07(s):
    c = s.c
    top, bot = s.q('Which line is the radius, which is the diameter, and which is a chord?', 4.4 * cm)
    x, y, r = M + 3.6 * cm, bot + 2.2 * cm, 2.0 * cm
    c.setStrokeColor(INK); c.setLineWidth(1.6); c.circle(x, y, r); c.setFillColor(INK); c.circle(x, y, 2.2, fill=1)
    c.setStrokeColor(BLUE); c.line(x - r, y, x + r, y); c.setStrokeColor(PINK); c.line(x, y, *pt(x, y, 70, r))
    c.setStrokeColor(HexColor('#00A88F')); c.line(*pt(x, y, 200, r), *pt(x, y, 300, r))
    c.setFont('Sans-B', 12); c.setFillColor(BLUE); c.drawString(x + r + 6, y - 4, 'p'); c.setFillColor(PINK); c.drawString(*[v + 4 for v in pt(x, y, 70, r)], 'q'); c.setFillColor(HexColor('#00A88F')); c.drawString(*[v - 12 for v in pt(x, y, 250, r)], 'r')
    for k, (t, a) in enumerate([('radius:', 'q'), ('diameter:', 'p'), ('chord:', 'r')]):
        yy = top - (k + 1) * 1.1 * cm; c.setFillColor(INK); c.setFont('Sans', 11); c.drawString(M + 8.5 * cm, yy, t); s.blank(M + 10.6 * cm, yy, 2 * cm, a)
    top, bot = s.q('Fill in: a radius of 4 cm means a diameter of ___ cm. A diameter of 15 cm means a radius of ___ cm.', 0.9 * cm)
    s.blank(M + 1.0 * cm, bot + 0.1 * cm, 2 * cm, 8, 'cm'); s.blank(M + 5 * cm, bot + 0.1 * cm, 2 * cm, 7.5, 'cm')
    top, bot = s.q('Circumference = π × diameter. Use π ≈ 3.14. Find the circumference when the diameter is 10 cm, and when it is 50 cm.', 0.9 * cm)
    s.blank(M + 1.0 * cm, bot + 0.1 * cm, 2 * cm, 31.4, 'cm'); s.blank(M + 5 * cm, bot + 0.1 * cm, 2 * cm, 157, 'cm')
    top, bot = s.q('Area = π × radius × radius. Find the area when the radius is 5 cm, and when it is 10 cm.', 0.9 * cm)
    s.blank(M + 1.0 * cm, bot + 0.1 * cm, 2 * cm, 78.5, 'cm²'); s.blank(M + 5 * cm, bot + 0.1 * cm, 2 * cm, 314, 'cm²')
    top, bot = s.q('A bike wheel is 70 cm across. How far does the bike travel in 10 full turns of the wheel? Give your answer in metres.', 1.0 * cm)
    s.blank(M + 1.0 * cm, bot + 0.1 * cm, 3 * cm, '≈ 22 m (2198 cm)')
    top, bot = s.q('Kitchen experiment: wrap string round a tin, measure it, then measure across the tin. Divide the first by the second.', 2.2 * cm)
    c.setFont('Sans', 11); c.setFillColor(INK)
    for k, t in enumerate(['Around:', 'Across:', 'Around ÷ across =']):
        yy = top - (k + 1) * 0.65 * cm; c.drawString(M + 1.0 * cm, yy, t); s.blank(M + 5 * cm, yy, 2.5 * cm, '≈ 3.1' if k == 2 else None)


def w08(s):
    c = s.c
    top, bot = s.q('Complete the table. Then check that faces + vertices − edges = 2 for every shape.', 4.4 * cm)
    rows = [('cube', 6, 12, 8), ('cuboid', 6, 12, 8), ('triangular prism', 5, 9, 6), ('square-based pyramid', 5, 8, 5), ('tetrahedron', 4, 6, 4)]
    x0, y = M + 1.0 * cm, top - 0.6 * cm; cw = [5.4 * cm, 2.6 * cm, 2.6 * cm, 2.6 * cm, 2.8 * cm]
    heads = ['shape', 'faces', 'edges', 'vertices', 'F + V − E']
    c.setFont('Sans-B', 10); c.setFillColor(INK)
    xx = x0
    for h_, w_ in zip(heads, cw):
        c.drawString(xx + 4, y, h_); xx += w_
    c.setStrokeColor(LINE)
    for k, r in enumerate(rows):
        yy = y - (k + 1) * 0.7 * cm; c.line(x0, yy + 0.5 * cm, x0 + sum(cw), yy + 0.5 * cm)
        c.setFont('Sans', 10.5); c.setFillColor(INK); c.drawString(x0 + 4, yy, r[0])
        vals = [r[1], r[2], r[3], r[1] + r[3] - r[2]]
        for j, v in enumerate(vals):
            xx = x0 + sum(cw[:j + 1]) + 4
            if k == 0 and j < 3 and not s.answers:
                c.setFont('Sans', 10.5); c.setFillColor(INK); c.drawString(xx, yy, str(v))
            else:
                s.a(xx, yy, str(v), 10.5)
    top, bot = s.q('Which of these nets fold up into a cube? Tick them. (Imagine folding, or copy them onto squared paper and try.)', 4.0 * cm)
    u = 0.62 * cm
    nets = [('A', [(1, 0), (1, 1), (1, 2), (1, 3), (0, 2), (2, 2)], 'yes'), ('B', [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (0, 2)], 'no'),
            ('C', [(0, 3), (1, 3), (1, 2), (2, 2), (2, 1), (3, 1)], 'yes'), ('D', [(0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)], 'no')]
    for k, (lab, cells, ans) in enumerate(nets):
        x = M + 1.0 * cm + k * 4.2 * cm; c.setFont('Sans-B', 12); c.setFillColor(INK); c.drawString(x, top - 0.5 * cm, lab)
        squares(c, x, bot + 0.6 * cm, cells, u); s.a(x + 0.5 * cm, bot + 0.05 * cm, ans)
    top, bot = s.q('Name the 3D shape.', 2.8 * cm)
    rows = [('I have 6 square faces.', 'cube'), ('1 square face + 4 triangles meeting at a point.', 'square-based pyramid'),
            ('I have 2 flat circles and 1 curved surface.', 'cylinder'), ('I have one curved surface and no edges at all.', 'sphere')]
    for k, (t, a) in enumerate(rows):
        y = top - (k + 1) * 0.62 * cm; c.setFillColor(INK); c.setFont('Sans', 11); c.drawString(M + 1.0 * cm, y, t); s.blank(M + 12.4 * cm, y, 3.6 * cm, a)
    top, bot = s.q('Cut out the dice net on the next page, fold along the lines and glue the tabs. Opposite faces of a real dice add up to 7. Do yours?', 0.8 * cm)
    s.a(M + 1.0 * cm, bot + 0.2 * cm, 'Yes: 1↔6, 2↔5, 3↔4 end up opposite.')
    # cut-out page
    s.new_page()
    u = 4.6 * cm; x0 = (W - 3 * u) / 2; y0 = 2.6 * cm
    cells = {'T': (1, 3), 'F': (1, 2), 'Bo': (1, 1), 'Ba': (1, 0), 'L': (0, 2), 'R': (2, 2)}
    pips = {'F': 1, 'T': 2, 'L': 3, 'R': 4, 'Bo': 5, 'Ba': 6}
    c.setFont('Sans-B', 14); c.setFillColor(INK); c.drawCentredString(W / 2, H - M - 1.6 * cm, 'Cut out, fold along every line, glue the grey tabs. Build your own dice!')

    def tab(xa, ya, xb, yb):
        dx, dy = xb - xa, yb - ya; L = math.hypot(dx, dy); nx, ny = dy / L, -dx / L; d = 0.8 * cm; ins = 0.8 * cm
        p = c.beginPath(); p.moveTo(xa, ya); p.lineTo(xa + dx * ins / L + nx * d, ya + dy * ins / L + ny * d); p.lineTo(xb - dx * ins / L + nx * d, yb - dy * ins / L + ny * d); p.lineTo(xb, yb); p.close()
        c.setFillColor(HexColor('#DDE3F0')); c.setStrokeColor(INK); c.setLineWidth(1); c.drawPath(p, fill=1, stroke=1)
    def cell(k):
        i, j = cells[k]; return x0 + i * u, y0 + j * u
    xL, yL = cell('L'); xR, yR = cell('R'); xB, yB = cell('Ba')
    tab(xL, yL + u, xL, yL)       # L left edge (outward = left)
    tab(xL + u, yL + u, xL, yL + u)   # L top
    tab(xL, yL, xL + u, yL)       # L bottom
    tab(xR, yR + u, xR + u, yR + u)   # R top
    tab(xR + u, yR, xR, yR)       # R bottom
    tab(xR + u, yR + u, xR + u, yR)   # R right
    tab(xB + u, yB, xB, yB)       # Back bottom
    face_cols = ['#FFD9E5', '#DCE6FF', '#FFF0C7', '#D3F5EE', '#E8DFFF', '#FFE4D2']
    for n, (k, (i, j)) in enumerate(cells.items()):
        x, y = x0 + i * u, y0 + j * u; c.setFillColor(HexColor(face_cols[n])); c.setStrokeColor(INK); c.setLineWidth(1.6); c.rect(x, y, u, u, fill=1, stroke=1)
        p = pips[k]; c.setFillColor(INK); g = u / 4
        spots = {1: [(2, 2)], 2: [(1, 3), (3, 1)], 3: [(1, 3), (2, 2), (3, 1)], 4: [(1, 1), (1, 3), (3, 1), (3, 3)], 5: [(1, 1), (1, 3), (2, 2), (3, 1), (3, 3)], 6: [(1, 1), (1, 2), (1, 3), (3, 1), (3, 2), (3, 3)]}[p]
        for (a_, b_) in spots:
            c.circle(x + a_ * g, y + b_ * g, 0.38 * cm, fill=1, stroke=0)
    mascot(c, W - M - 1.2 * cm, 1.4 * cm, 1.0)


def w09(s):
    c = s.c
    top, bot = s.q('The two rails are parallel. One angle is 70°. Find angles a to g. (Not drawn to scale.)', 6.0 * cm)
    ya, yb = bot + 4.4 * cm, bot + 1.4 * cm; x0, x1 = M + 1.0 * cm, M + 9.5 * cm; phi = 62
    c.setStrokeColor(INK); c.setLineWidth(1.8); c.line(x0, ya, x1, ya); c.line(x0, yb, x1, yb)
    for yy in (ya, yb):
        c.line(x1 - 1.0 * cm, yy + 4, x1 - 0.8 * cm, yy); c.line(x1 - 1.0 * cm, yy - 4, x1 - 0.8 * cm, yy)
    cx_, cy_ = M + 5.2 * cm, (ya + yb) / 2; xs = [cx_ + (ya - cy_) / math.tan(math.radians(phi)), cx_ - (cy_ - yb) / math.tan(math.radians(phi))]
    c.setStrokeColor(BLUE); c.line(*pt(cx_, cy_, phi, 3.2 * cm), *pt(cx_, cy_, phi + 180, 3.2 * cm))
    names = [['a', '70°', 'b', 'c'], ['d', 'e', 'f', 'g']]  # TL, TR, BL, BR
    mids = [(phi + 180) / 2, phi / 2, (180 + 180 + phi) / 2, (180 + phi + 360) / 2]
    c.setFont('Sans-B', 11)
    for j, yy in enumerate((ya, yb)):
        for k in range(4):
            lx, ly = pt(xs[j], yy, mids[k], 0.75 * cm); t = names[j][k]; c.setFillColor(PINK if t == '70°' else INK); c.drawCentredString(lx, ly - 4, t)
    ans = [('a', '110°'), ('b', '70°'), ('c', '110°'), ('d', '110°'), ('e', '70°'), ('f', '70°'), ('g', '110°')]
    for k, (t, a) in enumerate(ans):
        yy = top - (k + 1) * 0.72 * cm; c.setFillColor(INK); c.setFont('Sans-B', 11); c.drawString(M + 11.2 * cm, yy, t + ' ='); s.blank(M + 12.2 * cm, yy, 2 * cm, a)
    top, bot = s.q('Use the diagram. Which kind of angle pair is each one: corresponding (F), alternate (Z) or co-interior (C)?', 1.9 * cm)
    for k, (t, a) in enumerate([('70° and e', 'corresponding (F)'), ('b and e', 'alternate (Z)'), ('b and d', 'co-interior (C)')]):
        yy = top - (k + 1) * 0.6 * cm; c.setFillColor(INK); c.setFont('Sans', 11); c.drawString(M + 1.0 * cm, yy, t); s.blank(M + 5 * cm, yy, 4.5 * cm, a)
    top, bot = s.q('Two co-interior angles: one is 115°. What is the other?', 0.9 * cm)
    s.blank(M + 1.0 * cm, bot + 0.1 * cm, 2 * cm, 65, '°')
    top, bot = s.q('Parallel hunt: find four pairs of parallel lines at home (think shelves, stairs, window frames).', 2.0 * cm)
    s.lines(top, 2, answer='Any sensible answers.')


def w10(s):
    c = s.c
    top, bot = s.q('Draw all the lines of symmetry on each shape. How many does each have?', 3.8 * cm)
    shapes = [('square', 4, 4), ('rectangle', 4, 2), ('equilateral triangle', 3, 3), ('regular hexagon', 6, 6), ('parallelogram', 0, 0)]
    short = {'equilateral triangle': 'equilateral △', 'regular hexagon': 'reg. hexagon'}
    for k, (nm, n, ans) in enumerate(shapes):
        x, y = M + 1.9 * cm + k * 3.3 * cm, bot + 2.2 * cm; r = 1.0 * cm; c.setStrokeColor(INK); c.setLineWidth(1.5)
        if nm == 'rectangle':
            c.rect(x - 1.2 * cm, y - 0.7 * cm, 2.4 * cm, 1.4 * cm)
        elif nm == 'parallelogram':
            p = c.beginPath(); p.moveTo(x - 1.2 * cm, y - 0.7 * cm); p.lineTo(x + 0.6 * cm, y - 0.7 * cm); p.lineTo(x + 1.2 * cm, y + 0.7 * cm); p.lineTo(x - 0.6 * cm, y + 0.7 * cm); p.close(); c.drawPath(p)
        else:
            m = {'square': 4, 'equilateral triangle': 3, 'regular hexagon': 6}[nm]; a0 = 90 if m == 3 else (45 if m == 4 else 0)
            p = c.beginPath(); P = [pt(x, y, a0 + i * 360 / m, r) for i in range(m)]; p.moveTo(*P[0]); [p.lineTo(*q) for q in P[1:]]; p.close(); c.drawPath(p)
            if s.answers:
                c.setStrokeColor(ANS); c.setDash(3, 2); c.setLineWidth(1)
                for i in range(m):
                    a = a0 + i * 180 / m; c.line(*pt(x, y, a, r * 1.25), *pt(x, y, a + 180, r * 1.25))
                c.setDash()
        if s.answers and nm == 'rectangle':
            c.setStrokeColor(ANS); c.setDash(3, 2); c.setLineWidth(1); c.line(x - 1.5 * cm, y, x + 1.5 * cm, y); c.line(x, y - 1.0 * cm, x, y + 1.0 * cm); c.setDash()
        c.setFont('Sans', 9); c.setFillColor(MUTED); c.drawCentredString(x, bot + 0.6 * cm, short.get(nm, nm)); s.blank(x - 0.5 * cm, bot + 0.05 * cm, 1 * cm, ans)
    top, bot = s.q('Complete the picture so the dashed line is a line of symmetry.', 5.4 * cm)
    u = 0.6 * cm; x0, y0 = M + 3.0 * cm, bot + 0.4 * cm; cols, rows = 14, 8
    c.setStrokeColor(LINE); c.setLineWidth(0.6)
    for i in range(cols + 1):
        c.line(x0 + i * u, y0, x0 + i * u, y0 + rows * u)
    for j in range(rows + 1):
        c.line(x0, y0 + j * u, x0 + cols * u, y0 + j * u)
    mx = x0 + 7 * u; c.setStrokeColor(PINK); c.setDash(5, 3); c.setLineWidth(1.6); c.line(mx, y0 - 6, mx, y0 + rows * u + 6); c.setDash()
    half = [(7, 1), (4, 1), (4, 3), (2, 3), (2, 5), (5, 7), (7, 7)]
    c.setStrokeColor(INK); c.setLineWidth(2); p = c.beginPath(); p.moveTo(x0 + half[0][0] * u, y0 + half[0][1] * u); [p.lineTo(x0 + a * u, y0 + b * u) for a, b in half[1:]]; c.drawPath(p, fill=0, stroke=1)
    if s.answers:
        c.setStrokeColor(ANS); p = c.beginPath(); p.moveTo(x0 + (14 - half[0][0]) * u, y0 + half[0][1] * u); [p.lineTo(x0 + (14 - a) * u, y0 + b * u) for a, b in half[1:]]; c.drawPath(p, fill=0, stroke=1)
    top, bot = s.q('What is the order of rotational symmetry? (How many times does it fit onto itself in one full turn?)', 1.4 * cm)
    for k, (t, a) in enumerate([('letter S', 2), ('letter H', 2), ('equilateral △', 3), ('square', 4), ('recycling sign', 3)]):
        x = M + 1.0 * cm + k * 3.3 * cm; c.setFont('Sans', 10); c.setFillColor(INK); c.drawString(x, bot + 0.75 * cm, t); s.blank(x, bot + 0.1 * cm, 1.4 * cm, a)
    top, bot = s.q('Circle the capital letters that have a vertical line of symmetry:   A   B   F   H   J   M   P   T   U   W   Y   Z', 0.8 * cm)
    s.a(M + 1.0 * cm, bot + 0.15 * cm, 'A  H  M  T  U  W  Y')


def w11(s):
    c = s.c
    top, bot = s.q('Write the coordinates of each point. Remember: across first, then up (x, y).', 7.6 * cm)
    u = 0.65 * cm; ox, oy = M + 4.4 * cm, bot + 3.8 * cm; grid(c, ox, oy, u, -5, 5)
    P = {'A': (2, 3), 'B': (-4, 1), 'C': (-2, -3), 'D': (3, -2), 'E': (0, 4), 'F': (-5, 0)}
    for k, (n, (x, y)) in enumerate(P.items()):
        c.setFillColor(PINK); c.circle(ox + x * u, oy + y * u, 3, fill=1, stroke=0); c.setFillColor(INK); c.setFont('Sans-B', 10); c.drawString(ox + x * u + 4, oy + y * u + 4, n)
        yy = top - (k + 1) * 1.05 * cm; c.setFont('Sans-B', 11); c.drawString(M + 9.6 * cm, yy, f'{n} = (       ,       )')
        bx = M + 9.6 * cm; s.a(bx + c.stringWidth(f'{n} = (', 'Sans-B', 11) + 4, yy, str(x)); s.a(bx + c.stringWidth(f'{n} = (       ,', 'Sans-B', 11) + 4, yy, str(y))
    top, bot = s.q('Plot these points and join them in order: (−3, −2), (3, −2), (3, 2), (−3, 2), back to the start. What shape is it?', 7.4 * cm)
    ox, oy = M + 4.4 * cm, bot + 3.7 * cm; grid(c, ox, oy, u, -5, 5)
    if s.answers:
        poly(c, [(-3, -2), (3, -2), (3, 2), (-3, 2)], ox, oy, u, fill=ANS, stroke=ANS)
    c.setFillColor(INK); c.setFont('Sans', 11); c.drawString(M + 9.6 * cm, oy, 'Shape:'); s.blank(M + 11.2 * cm, oy, 3.4 * cm, 'rectangle')
    top, bot = s.q('A square has corners at (1, 1), (4, 1) and (4, 4). Where is the fourth corner?', 0.9 * cm)
    s.blank(M + 1.0 * cm, bot + 0.1 * cm, 3 * cm, '(1, 4)')
    top, bot = s.q('Which quarter (quadrant) of the grid is each point in: top-left, top-right, bottom-left or bottom-right?', 1.0 * cm)
    for k, (t, a) in enumerate([('(−2, 5)', 'top-left'), ('(4, −1)', 'bottom-right'), ('(−3, −3)', 'bottom-left')]):
        x = M + 1.0 * cm + k * 5.4 * cm; c.setFont('Sans-B', 11); c.setFillColor(INK); c.drawString(x, bot + 0.25 * cm, t); s.blank(x + 1.6 * cm, bot + 0.2 * cm, 3 * cm, a)


def w12(s):
    c = s.c
    u = 0.5 * cm
    tri = [(-5, 1), (-3, 1), (-5, 4)]
    def task(text, obj, img, extra=None, desc=None):
        top, bot = s.q(text, 6.6 * cm)
        ox, oy = M + 4.2 * cm, bot + 3.3 * cm; grid(c, ox, oy, u, -6, 6)
        poly(c, obj, ox, oy, u, fill=BLUE, stroke=BLUE)
        c.setFillColor(BLUE); c.setFont('Sans-B', 9); c.drawString(ox + obj[0][0] * u - 9, oy + obj[0][1] * u - 9, 'A')
        if extra:
            extra(ox, oy)
        if s.answers and img:
            poly(c, img, ox, oy, u, fill=ANS, stroke=ANS); c.setFillColor(ANS); c.setFont('Sans-B', 9); c.drawString(ox + img[0][0] * u + 3, oy + img[0][1] * u - 10, "A′")
        c.setFillColor(INK); c.setFont('Sans', 11)
        if desc:
            c.drawString(M + 9.0 * cm, oy + 0.6 * cm, desc[0]); s.blank(M + 9.0 * cm, oy - 0.2 * cm, 7 * cm, desc[1])
        else:
            c.drawString(M + 9.0 * cm, oy + 0.6 * cm, "Write the coordinates of A′:"); s.blank(M + 9.0 * cm, oy - 0.2 * cm, 3 * cm, f'({img[0][0]}, {img[0][1]})')
    task('Translate the triangle 6 squares right and 4 squares down. Label the image A′.', tri, [(x + 6, y - 4) for x, y in tri])
    def ymirror(ox, oy):
        c.setStrokeColor(PINK); c.setLineWidth(1.6); c.setDash(4, 3); c.line(ox, oy - 6.3 * u, ox, oy + 6.3 * u); c.setDash()
    task('Reflect the triangle in the y-axis (the pink mirror line).', tri, [(-x, y) for x, y in tri], ymirror)
    flag = [(1, 1), (1, 5), (3, 4), (1, 3)]
    def centre(ox, oy):
        c.setFillColor(PINK); c.circle(ox, oy, 3.2, fill=1, stroke=0); c.setFont('Sans-B', 9); c.drawString(ox - 12, oy - 12, 'O')
    task('Rotate the flag 90° clockwise about the origin O. (Tracing paper helps!)', flag, [(y, -x) for x, y in flag], centre)
    P = [(2, 1), (5, 1), (2, 3)]
    def shapeQ(ox, oy):
        poly(c, [(x, -y) for x, y in P], ox, oy, u, fill=PINK, stroke=PINK); c.setFillColor(PINK); c.setFont('Sans-B', 10); c.drawString(ox + 6 * u * 0.85, oy - 2.3 * u, 'Q')
    top_text = 'Shape A was moved onto shape Q with one transformation. Describe it fully.'
    task(top_text, P, None, shapeQ, ('Describe the transformation:', 'Reflection in the x-axis'))
    top, bot = s.q('After a translation, reflection or rotation, what stays the same about the shape? Tick: size ☐  shape ☐  angles ☐  position ☐', 0.6 * cm)
    s.a(M + 1.0 * cm, bot, 'size, shape and angles (it is congruent). Position changes.')


def w13(s):
    c = s.c
    top, bot = s.q('Construct an equilateral triangle with sides of 6 cm. Only measure the first side; use your compass for the rest. Leave your arcs showing!', 7.5 * cm)
    c.setFont('Sans', 9.5); c.setFillColor(MUTED)
    steps = ['1. Draw AB = 6 cm.', '2. Compass on A, open to B. Draw an arc.', '3. Same opening, compass on B. Draw an arc.', '4. Where the arcs cross is C. Join AC and BC.']
    for k, t in enumerate(steps):
        c.drawString(M + 11.2 * cm, top - (k + 1) * 0.55 * cm, t)
    if s.answers:
        x, y = M + 3.0 * cm, bot + 1.0 * cm; L = 6 * cm
        c.setStrokeColor(ANS); c.setLineWidth(1.4); c.line(x, y, x + L, y); cx_, cy_ = x + L / 2, y + L * math.sqrt(3) / 2; c.line(x, y, cx_, cy_); c.line(x + L, y, cx_, cy_)
        c.setDash(3, 2); c.arc(x - L, y - L, x + L, y + L, 45, 30); c.arc(x, y - L, x + 2 * L, y + L, 105, 30); c.setDash()
        s.a(M + 11.2 * cm, bot + 1.0 * cm, 'Check: all sides 6 cm,', 10); s.a(M + 11.2 * cm, bot + 0.5 * cm, 'all angles 60°.', 10)
    top, bot = s.q('Can these three sticks make a triangle? Write yes, no, or flat.', 1.6 * cm)
    for k, (t, a) in enumerate([('3, 4, 5 cm', 'yes'), ('2, 2, 5 cm', 'no'), ('5, 5, 10 cm', 'flat'), ('6, 7, 8 cm', 'yes')]):
        x = M + 1.0 * cm + k * 4.1 * cm; c.setFont('Sans-B', 11); c.setFillColor(INK); c.drawString(x, bot + 0.8 * cm, t); s.blank(x, bot + 0.1 * cm, 2 * cm, a)
    top, bot = s.q('Bisect (cut exactly in half) this 8 cm line with a compass: open it more than halfway, draw arcs above and below from each end, and join the crossings.', 3.6 * cm)
    x, y = M + 4.0 * cm, bot + 1.8 * cm; c.setStrokeColor(INK); c.setLineWidth(1.6); c.line(x, y, x + 8 * cm, y); c.setFillColor(INK); c.circle(x, y, 2.4, fill=1); c.circle(x + 8 * cm, y, 2.4, fill=1)
    if s.answers:
        c.setStrokeColor(ANS); c.line(x + 4 * cm, y - 1.6 * cm, x + 4 * cm, y + 1.6 * cm); s.a(x + 8.4 * cm, y - 3, 'Check: 4 cm each side', 10)
    top, bot = s.q('Construct a triangle with sides 5 cm, 6 cm and 7 cm. (Draw the 7 cm side, then use arcs of 5 cm and 6 cm from its ends.)', 6.0 * cm)
    s.a(M + 1.0 * cm, bot + 0.3 * cm, 'Check the three sides with a ruler: 5, 6 and 7 cm.')


def w14(s):
    c = s.c
    top, bot = s.q('Two triangles share these facts. Which rule proves they are congruent: SSS, SAS, ASA, AAS, RHS or “not enough”?', 4.0 * cm)
    rows = [('all three sides match', 'SSS'), ('two sides and the angle between them match', 'SAS'), ('two angles and the side between them match', 'ASA'),
            ('a right angle, the hypotenuse and one other side match', 'RHS'), ('all three angles match', 'not enough'), ('two sides and an angle NOT between them match', 'not enough')]
    for k, (t, a) in enumerate(rows):
        y = top - (k + 1) * 0.62 * cm; c.setFont('Sans', 11); c.setFillColor(INK); c.drawString(M + 1.0 * cm, y, t); s.blank(M + 12.6 * cm, y, 3 * cm, a)
    top, bot = s.q('△ABC ≅ △PQR. AB = 5 cm, BC = 7 cm and angle A = 40°. Find PQ, QR and angle P.', 1.0 * cm)
    for k, (t, a) in enumerate([('PQ =', '5 cm'), ('QR =', '7 cm'), ('∠P =', '40°')]):
        x = M + 1.0 * cm + k * 5 * cm; c.setFont('Sans-B', 11); c.setFillColor(INK); c.drawString(x, bot + 0.25 * cm, t); s.blank(x + 1.3 * cm, bot + 0.2 * cm, 2 * cm, a)
    top, bot = s.q('Draw two triangles that both have angles of 50°, 60° and 70° but are different sizes. What does this show?', 5.0 * cm)
    s.a(M + 1.0 * cm, bot + 0.3 * cm, 'Matching angles (AAA) is not enough: same shape, different size (similar).')
    top, bot = s.q('Why does a garden gate have a diagonal piece of wood across it?', 1.8 * cm)
    s.lines(top, 2, answer='The brace makes triangles, which are rigid (SSS), so the gate can’t sag.')


def w15(s):
    c = s.c
    top, bot = s.q('Find the hypotenuse (longest side) of each right-angled triangle. a² + b² = c².', 1.4 * cm)
    for k, (a, b, h) in enumerate([(3, 4, 5), (5, 12, 13), (8, 15, 17), (9, 12, 15)]):
        x = M + 1.0 * cm + k * 4.1 * cm; c.setFont('Sans', 11); c.setFillColor(INK); c.drawString(x, bot + 0.75 * cm, f'{a} and {b}'); s.blank(x, bot + 0.1 * cm, 2 * cm, h)
    top, bot = s.q('Find the missing shorter side.', 1.4 * cm)
    for k, (h, a, b) in enumerate([(10, 6, 8), (13, 5, 12), (25, 7, 24)]):
        x = M + 1.0 * cm + k * 5.4 * cm; c.setFont('Sans', 11); c.setFillColor(INK); c.drawString(x, bot + 0.75 * cm, f'hypotenuse {h}, side {a}'); s.blank(x, bot + 0.1 * cm, 2 * cm, b)
    top, bot = s.q('A 5 m ladder leans on a wall. Its foot is 1.4 m from the wall. How high up the wall does it reach?', 3.8 * cm)
    x, y = M + 2.0 * cm, bot + 0.4 * cm; c.setStrokeColor(INK); c.setLineWidth(1.6); c.line(x - 0.4 * cm, y, x + 4 * cm, y); c.line(x + 3.2 * cm, y, x + 3.2 * cm, y + 3.3 * cm)
    c.setStrokeColor(HexColor('#C8894B')); c.setLineWidth(3); c.line(x + 2.3 * cm, y, x + 3.2 * cm, y + 3.1 * cm)
    c.setFont('Sans', 10); c.setFillColor(INK); c.drawString(x + 1.2 * cm, y + 1.8 * cm, '5 m'); c.drawString(x + 2.3 * cm, y - 0.45 * cm, '1.4 m'); c.drawString(x + 3.4 * cm, y + 1.5 * cm, '?')
    s.blank(M + 8.5 * cm, bot + 1.6 * cm, 3 * cm, '4.8', 'm'); s.a(M + 8.5 * cm, bot + 0.9 * cm, '√(25 − 1.96) = √23.04 = 4.8', 10)
    top, bot = s.q('Is a triangle with sides 7, 24 and 25 right-angled? Show your working.', 1.8 * cm)
    s.lines(top, 2, answer='7² + 24² = 49 + 576 = 625 = 25². Yes, it is right-angled.')
    top, bot = s.q('Paper investigation: measure a sheet of A4. Divide the long side by the short side. Fold it in half and do the same for the new A5 size.', 1.8 * cm)
    c.setFont('Sans', 11); c.setFillColor(INK); c.drawString(M + 1.0 * cm, top - 0.7 * cm, 'A4:'); s.blank(M + 2.2 * cm, top - 0.7 * cm, 3 * cm, '297 ÷ 210 ≈ 1.41')
    c.drawString(M + 8.0 * cm, top - 0.7 * cm, 'A5:'); s.blank(M + 9.2 * cm, top - 0.7 * cm, 3 * cm, '210 ÷ 148 ≈ 1.42')
    s.a(M + 1.0 * cm, bot + 0.2 * cm, 'Both are about √2 = 1.414…, so the shape stays the same.', 10)


def w16(s):
    c = s.c
    top, bot = s.q('Cantor set: each step removes the middle third of every piece. Complete the table.', 3.0 * cm)
    rows = [(0, '1', '1'), (1, '2', '2/3'), (2, '4', '4/9'), (3, '8', '8/27'), (4, '16', '16/81')]
    x0, y = M + 1.0 * cm, top - 0.5 * cm
    c.setFont('Sans-B', 10); c.setFillColor(INK); c.drawString(x0, y, 'step'); c.drawString(x0 + 2.5 * cm, y, 'pieces'); c.drawString(x0 + 5.5 * cm, y, 'length left (start = 1)')
    for k, (st, pc, ln) in enumerate(rows):
        yy = y - (k + 1) * 0.45 * cm; c.setFont('Sans', 10); c.setFillColor(INK); c.drawString(x0, yy, str(st))
        if k < 2 and not s.answers:
            c.drawString(x0 + 2.5 * cm, yy, pc); c.drawString(x0 + 5.5 * cm, yy, ln)
        else:
            s.a(x0 + 2.5 * cm, yy, pc, 10); s.a(x0 + 5.5 * cm, yy, ln, 10)
    top, bot = s.q('Koch snowflake: start with a triangle of side 9 cm. Each step, every edge becomes 4 edges, each a third as long. Complete the table.', 2.6 * cm)
    rows = [(0, '3', '27 cm'), (1, '12', '36 cm'), (2, '48', '48 cm'), (3, '192', '64 cm')]
    x0, y = M + 1.0 * cm, top - 0.5 * cm
    c.setFont('Sans-B', 10); c.setFillColor(INK); c.drawString(x0, y, 'step'); c.drawString(x0 + 2.5 * cm, y, 'edges'); c.drawString(x0 + 5.5 * cm, y, 'perimeter')
    for k, (st, e, p_) in enumerate(rows):
        yy = y - (k + 1) * 0.45 * cm; c.setFont('Sans', 10); c.setFillColor(INK); c.drawString(x0, yy, str(st))
        if k == 0 and not s.answers:
            c.drawString(x0 + 2.5 * cm, yy, e); c.drawString(x0 + 5.5 * cm, yy, p_)
        else:
            s.a(x0 + 2.5 * cm, yy, e, 10); s.a(x0 + 5.5 * cm, yy, p_, 10)
    top, bot = s.q('Draw step 1 of the Koch curve on this 9 cm line: split it into three 3 cm parts, draw an equilateral triangle on the middle part, then rub out its base.', 3.2 * cm)
    x, y = M + 4.0 * cm, bot + 0.6 * cm; c.setStrokeColor(INK); c.setLineWidth(1.6)
    if s.answers:
        c.setStrokeColor(ANS); p = c.beginPath(); p.moveTo(x, y); p.lineTo(x + 3 * cm, y); p.lineTo(x + 4.5 * cm, y + 3 * cm * math.sqrt(3) / 2); p.lineTo(x + 6 * cm, y); p.lineTo(x + 9 * cm, y); c.drawPath(p, fill=0, stroke=1)
    else:
        c.line(x, y, x + 9 * cm, y)
    top, bot = s.q('Fractal hunt: find three things in nature or at home that repeat their pattern when you zoom in. Draw one of them.', 4.0 * cm)
    s.a(M + 1.0 * cm, bot + 0.3 * cm, 'e.g. fern leaf, broccoli/cauliflower, tree branches, river deltas, frost, lightning.')


FUNCS = [w01, w02, w03, w04, w05, w06, w07, w08, w09, w10, w11, w12, w13, w14, w15, w16]

if __name__ == '__main__':
    pack = canvas.Canvas(f'{OUT}/geometry-quest-worksheet-pack.pdf', pagesize=A4)
    apack = canvas.Canvas(f'{OUT}/geometry-quest-answer-pack.pdf', pagesize=A4)
    for k, ((wid, name, col), fn) in enumerate(zip(WORLDS, FUNCS)):
        for ans in (False, True):
            fname = f'{OUT}/{wid}-{"answers" if ans else "worksheet"}.pdf'
            cv = canvas.Canvas(fname, pagesize=A4); cv.setTitle(f'Geometry Quest World {k + 1}: {name} ({"answers" if ans else "worksheet"})')
            fn(Sheet(cv, k + 1, name, col, ans)); cv.showPage(); cv.save()
            pk = apack if ans else pack
            fn(Sheet(pk, k + 1, name, col, ans)); pk.showPage()
    pack.setTitle('Geometry Quest worksheet pack'); apack.setTitle('Geometry Quest answer pack')
    pack.save(); apack.save()
    print('done')
