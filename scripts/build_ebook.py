"""Gera o PDF a partir do Markdown paginado, sem acesso à rede."""
from pathlib import Path
from html import escape
import re
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Flowable
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
FONT_DIRS = [Path('C:/Windows/Fonts'), Path('/usr/share/fonts/truetype/dejavu')]
for fontdir in FONT_DIRS:
    regular = next((fontdir / n for n in ['arial.ttf', 'DejaVuSans.ttf'] if (fontdir / n).exists()), None)
    bold = next((fontdir / n for n in ['arialbd.ttf', 'DejaVuSans-Bold.ttf'] if (fontdir / n).exists()), None)
    if regular and bold:
        break
else:
    raise RuntimeError('Instale Arial ou DejaVu Sans para gerar o PDF com acentos.')
pdfmetrics.registerFont(TTFont('Body', str(regular)))
pdfmetrics.registerFont(TTFont('BodyBold', str(bold)))
pdfmetrics.registerFontFamily('Body', normal='Body', bold='BodyBold', italic='Body', boldItalic='BodyBold')

W, H = 420, 595
M = 42
INK = colors.HexColor('#173C40')
GREEN = colors.HexColor('#2C604A')
CREAM = colors.HexColor('#F9F7EE')
PALE = colors.HexColor('#EAF0E7')
WIDTH = W - M * 2
BODY = ParagraphStyle('Body', fontName='Body', fontSize=10.2, leading=14.5, textColor=INK, spaceAfter=10)
TITLE = ParagraphStyle('Title', parent=BODY, fontName='BodyBold', fontSize=22, leading=26, spaceAfter=18)
CELL = ParagraphStyle('Cell', parent=BODY, fontSize=8.5, leading=11, spaceAfter=0)
SMALL = ParagraphStyle('Small', parent=BODY, fontSize=8, leading=10, spaceAfter=0)
CHECK = ParagraphStyle('Check', parent=BODY, fontSize=9.8, leading=13.5, spaceAfter=5)

def inline(text):
    text = escape(text)
    text = re.sub(r'\[([^\]]+)\]\((https://[^)]+)\)', r'<link href="\2" color="#2C604A"><u>\1</u></link>', text)
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)

class CoverSpace(Flowable):
    def __init__(self):
        super().__init__()
        self.width = 1
        self.height = 1
    def draw(self):
        pass

def decorate(c, doc):
    c.saveState()
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    if doc.page == 1:
        image = ImageReader(str(ROOT / 'assets/images/capa.jpg'))
        iw, ih = image.getSize()
        scale = min(W / iw, H / ih)
        c.drawImage(image, (W-iw*scale)/2, (H-ih*scale)/2, width=iw*scale, height=ih*scale)
    else:
        c.setFillColor(GREEN)
        c.setFont('BodyBold', 7)
        c.drawString(M, H-28, 'SEU DINHEIRO EM ORDEM')
        c.setStrokeColor(colors.HexColor('#CBD6C7'))
        c.line(M, 35, W-M, 35)
        c.setFont('Body', 7)
        c.drawString(M, 23, 'FINANÇAS PESSOAIS | MARCOSSLV')
        c.drawRightString(W-M, 23, f'{doc.page:02d}')
    c.restoreState()

def parse_page(source):
    result = []
    lines = source.strip().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith('## '):
            result.append(Paragraph(inline(line[3:]), TITLE))
        elif line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells = [x.strip() for x in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r'[:\- ]+', x) for x in cells):
                    rows.append([Paragraph(inline(x or ' '), CELL) for x in cells])
                i += 1
            count = len(rows[0])
            if count == 2:
                widths = [WIDTH * .66, WIDTH * .34]
            elif count == 4:
                widths = [WIDTH * .14, WIDTH * .36, WIDTH * .28, WIDTH * .22]
            else:
                widths = [WIDTH * .46, WIDTH * .27, WIDTH * .27]
            # The action-plan table needs more room for full sentences.
            if count == 3 and 'Período' in lines[i-len(rows)-1]:
                widths = [WIDTH*.21, WIDTH*.44, WIDTH*.35]
            table = Table(rows, colWidths=widths, hAlign='LEFT', repeatRows=1)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), PALE),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LINEBELOW', (0,0), (-1,0), .7, GREEN),
                ('LINEBELOW', (0,1), (-1,-1), .3, colors.HexColor('#D8DED3')),
                ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
                ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
            ]))
            result += [table, Spacer(1,12)]
            continue
        elif line.startswith('- [ ] '):
            result.append(Paragraph('&#9633; ' + inline(line[6:]), CHECK))
        elif line.startswith('- '):
            result.append(Paragraph('• ' + inline(line[2:]), BODY))
        elif re.fullmatch('_+', line):
            result.append(Spacer(1,8))
            result.append(Paragraph('_' * 45, SMALL))
            result.append(Spacer(1,8))
        else:
            result.append(Paragraph(inline(line), BODY))
        i += 1
    return result

def main():
    source = (ROOT / 'ebook/seu-dinheiro-em-ordem.md').read_text(encoding='utf-8')
    sections = source.split('<!-- page -->')
    story = [CoverSpace(), PageBreak()]
    for index, section in enumerate(sections[1:]):
        story += parse_page(section)
        if index < len(sections)-2:
            story.append(PageBreak())
    output = ROOT / 'ebook/seu-dinheiro-em-ordem.pdf'
    doc = SimpleDocTemplate(str(output), pagesize=(W,H), rightMargin=M, leftMargin=M,
        topMargin=55, bottomMargin=48, title='Seu dinheiro em ordem', author='MarcosSlv',
        subject='Guia educativo de finanças pessoais com exercícios', pageCompression=1)
    doc.build(story, onFirstPage=decorate, onLaterPages=decorate)
    reader = PdfReader(output)
    if len(reader.pages) != len(sections):
        raise RuntimeError(f'Paginação inesperada: {len(reader.pages)} páginas; esperadas {len(sections)}. Revise o layout.')
    print(f'PDF gerado: {len(reader.pages)} páginas; {output.stat().st_size} bytes')

if __name__ == '__main__':
    main()
