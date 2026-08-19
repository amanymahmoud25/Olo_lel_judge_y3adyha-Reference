from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Preformatted, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from xml.sax.saxutils import escape

# =========================
# Settings
# =========================

ROOT = Path(".")
OUTPUT = "CP_Reference.pdf"

# =========================
# Find files
# =========================

files = sorted(
    p for p in ROOT.rglob("*")
    if p.is_file()
    and ".git" not in p.parts
    and p.name != OUTPUT
    and p.name != "make_pdf.py"
)

# =========================
# Fonts
# =========================

try:
    pdfmetrics.registerFont(
        TTFont(
            "DejaVu",
            "C:/Windows/Fonts/DejaVuSansMono.ttf"
        )
    )
    CODE_FONT = "DejaVu"
except:
    CODE_FONT = "Courier"

# =========================
# PDF
# =========================

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=35,
    leftMargin=35,
    topMargin=40,
    bottomMargin=35
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "MainTitle",
    parent=styles["Title"],
    fontSize=22,
    leading=26,
    alignment=TA_CENTER,
    spaceAfter=15
)

subtitle_style = ParagraphStyle(
    "Subtitle",
    parent=styles["Normal"],
    fontSize=10,
    leading=14,
    alignment=TA_CENTER,
    spaceAfter=25
)

file_style = ParagraphStyle(
    "FileTitle",
    parent=styles["Heading1"],
    fontSize=14,
    leading=18,
    spaceBefore=5,
    spaceAfter=12
)

code_style = ParagraphStyle(
    "Code",
    fontName=CODE_FONT,
    fontSize=7.2,
    leading=9,
    leftIndent=5,
    rightIndent=5,
    spaceAfter=10
)

story = []

# =========================
# Cover
# =========================

story.append(
    Paragraph(
        "CP REFERENCE",
        title_style
    )
)

story.append(
    Paragraph(
        "Competitive Programming Reference Repository",
        subtitle_style
    )
)

story.append(
    Paragraph(
        f"Total files: {len(files)}",
        styles["Normal"]
    )
)

story.append(Spacer(1, 20))

story.append(
    Paragraph(
        "Generated automatically from the repository",
        styles["Normal"]
    )
)

story.append(PageBreak())

# =========================
# Files
# =========================

for index, file in enumerate(files, 1):

    filename = str(file).replace("\\", "/")

    story.append(
        Paragraph(
            f"[{index}] {escape(filename)}",
            file_style
        )
    )

    story.append(
        Paragraph(
            "-" * 90,
            styles["Normal"]
        )
    )

    try:
        content = file.read_text(
            encoding="utf-8",
            errors="replace"
        )
    except Exception as e:
        content = f"ERROR READING FILE: {e}"

    if not content.strip():
        content = "[ EMPTY FILE ]"

    story.append(
        Preformatted(
            content,
            code_style
        )
    )

    story.append(PageBreak())


# =========================
# Page number
# =========================

def add_page_number(canvas, document):

    canvas.saveState()

    canvas.setFont("Helvetica", 8)

    canvas.drawCentredString(
        A4[0] / 2,
        18,
        f"Page {document.page}"
    )

    canvas.restoreState()


# =========================
# Build PDF
# =========================

doc.build(
    story,
    onFirstPage=add_page_number,
    onLaterPages=add_page_number
)

print()
print("=" * 50)
print("PDF CREATED SUCCESSFULLY")
print("=" * 50)
print(f"File: {OUTPUT}")
print(f"Files included: {len(files)}")
print("=" * 50)