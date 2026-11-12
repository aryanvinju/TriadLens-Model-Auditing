"""Render the six editable TriadLens Markdown documents as submission PDFs."""
from __future__ import annotations

import html
import math
import re
from pathlib import Path

from reportlab.graphics import renderSVG
from reportlab.graphics.shapes import Circle, Drawing, Ellipse, Line, Polygon, Rect, String
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (KeepTogether, Paragraph, Preformatted,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

HERE = Path(__file__).parent
OUT = HERE / "pdf"
OUT.mkdir(exist_ok=True)
NAVY = colors.black
TEAL = colors.black
PALE = colors.white

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="DocTitleX", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=16, leading=19, alignment=TA_LEFT, textColor=NAVY, spaceAfter=10))
styles.add(ParagraphStyle(name="H1X", parent=styles["Heading1"], fontSize=11.5, leading=14.5, textColor=NAVY, spaceBefore=12, spaceAfter=5, keepWithNext=1))
styles.add(ParagraphStyle(name="H2X", parent=styles["Heading2"], fontSize=9.8, leading=12.5, textColor=TEAL, spaceBefore=8, spaceAfter=4, keepWithNext=1))
styles.add(ParagraphStyle(name="BodyX", parent=styles["BodyText"], fontSize=8.5, leading=11.8, spaceAfter=4))
styles.add(ParagraphStyle(name="IdentityX", parent=styles["BodyText"], fontSize=8, leading=10, spaceAfter=2))
styles.add(ParagraphStyle(name="CellX", parent=styles["BodyText"], fontSize=7.7, leading=10.5))
styles.add(ParagraphStyle(name="HeaderCellX", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=7.7, leading=10.5, textColor=colors.black))
styles.add(ParagraphStyle(name="DiagramTextX", parent=styles["BodyText"], alignment=TA_CENTER, fontSize=8))
styles.add(ParagraphStyle(name="BulletX", parent=styles["BodyX"], leftIndent=12, firstLineIndent=-8, spaceAfter=4))
styles.add(ParagraphStyle(name="CodeX", fontName="Courier", fontSize=7.3, leading=10, leftIndent=12, spaceBefore=4, spaceAfter=8))


def markup(text):
    value = html.escape(text.replace("·", " - ").replace("≤", "<=" ).replace("≥", ">=").replace("→", " to ").replace("–", "-").replace("—", "-"))
    value = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: f"<link href='{html.escape(m.group(2), quote=True)}' color='black'><u>{m.group(1)}</u></link>", value)
    value = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", value)
    return value


def plain(text):
    """Keep Markdown syntax out of diagrams and preformatted blocks."""
    return re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text).replace("–", "-").replace("—", "-")


def label(d, x, y, text, size=8, color=NAVY):
    d.add(String(x, y, text, fontName="Helvetica", fontSize=size, fillColor=color, textAnchor="middle"))


def arrow(d, x1, y1, x2, y2, color=TEAL):
    d.add(Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=1.2))
    length = math.hypot(x2-x1, y2-y1) or 1
    ux, uy = (x2-x1)/length, (y2-y1)/length
    px, py = -uy, ux
    d.add(Polygon([x2, y2, x2-6*ux+3*px, y2-6*uy+3*py,
                   x2-6*ux-3*px, y2-6*uy-3*py], fillColor=color, strokeColor=color))


def box(d, x, y, width, height, title, details=()):
    d.add(Rect(x, y, width, height, strokeColor=NAVY, strokeWidth=1.1,
               fillColor=colors.white, rx=3, ry=3))
    label(d, x+width/2, y+height-18, title, 8.3)
    for index, detail in enumerate(details):
        label(d, x+width/2, y+height-35-index*12, detail, 7.2)


def diagram(kind):
    d = Drawing(480, 270 if kind == "usecase" else 210)
    if kind == "three-tier":
        box(d, 8, 70, 140, 94, "1  Presentation", ("Browser form", "Input / process / output", "Session comparison"))
        box(d, 170, 70, 140, 94, "2  Application", ("Flask validation", "ML / DL / QML inference", "Disagreement audit"))
        box(d, 332, 70, 140, 94, "3  Data + artifacts", ("Saved model files", "Metrics and split reports", "Offline survey CSV"))
        arrow(d, 148, 117, 170, 117)
        arrow(d, 310, 117, 332, 117)
        label(d, 240, 189, "Three-tier request path", 10)
        label(d, 240, 45, "Browser request -> validated inference -> JSON audit result", 8)
        label(d, 240, 26, "The CSV is used for offline training; the browser cannot read model files.", 7.3)
    elif kind == "usecase":
        gray = colors.HexColor('#667085')
        d.add(Rect(89, 14, 302, 244, strokeColor=NAVY, strokeWidth=1.5,
                   fillColor=colors.white, rx=10, ry=10))
        label(d, 240, 238, "TriadLens", 11)

        def actor(x, name):
            d.add(Circle(x, 153, 7, strokeColor=NAVY, strokeWidth=1.4, fillColor=colors.white))
            for coords in [(x,146,x,119),(x-13,134,x+13,134),
                           (x,119,x-12,100),(x,119,x+12,100)]:
                d.add(Line(*coords, strokeColor=NAVY, strokeWidth=1.4))
            label(d, x, 85, name, 8.5)

        actor(39, "Student")
        actor(441, "Lab Operator")

        cases = [
            (190, 199, "Load example", "UC-01"),
            (190, 151, "Enter features", "UC-02"),
            (190, 103, "Compare models", "UC-03"),
            (190, 55, "Inspect metrics", "UC-04"),
            (312, 175, "Train models", "UC-05"),
            (312, 79, "Deploy service", "UC-06"),
        ]
        # Association lines are drawn before the ovals so the use cases stay legible.
        for y in (199, 151, 103, 55):
            d.add(Line(59, 134, 128, y, strokeColor=gray, strokeWidth=1))
        for y in (175, 79):
            d.add(Line(421, 134, 374, y, strokeColor=gray, strokeWidth=1))
        for x, y, title, identifier in cases:
            d.add(Ellipse(x, y, 62, 18, strokeColor=NAVY, strokeWidth=1.2,
                          fillColor=colors.HexColor('#f6f7f8')))
            label(d, x, y+2, title, 8)
            label(d, x, y-9, identifier, 6.7, gray)
    elif kind == "component":
        label(d, 240, 187, "Online inference components", 10)
        box(d, 12, 72, 90, 86, "Browser UI", ("Form and results", "Test-flow view"))
        box(d, 130, 72, 100, 86, "Flask API", ("Schema validation", "HTTP and errors"))
        box(d, 258, 72, 110, 86, "Model audit", ("ML / DL / QML", "Agreement and slices"))
        box(d, 396, 72, 72, 86, "Artifacts", ("Models", "Reports"))
        arrow(d, 102, 115, 130, 115)
        arrow(d, 230, 115, 258, 115)
        arrow(d, 396, 115, 368, 115)
        label(d, 240, 43, "Validated request and JSON response", 8)
    elif kind == "deployment":
        label(d, 240, 190, "Local Kubernetes deployment", 10)
        box(d, 8, 75, 78, 65, "Browser", ("port-forward",))
        box(d, 112, 75, 98, 65, "Service", ("port 80", "load balancing"))
        box(d, 240, 116, 110, 52, "Pod 1", ("Gunicorn + Flask",))
        box(d, 240, 48, 110, 52, "Pod 2", ("Gunicorn + Flask",))
        box(d, 380, 116, 90, 52, "Docker Hub", ("source-only image",))
        box(d, 380, 48, 90, 52, "Secrets", ("private artifacts",))
        arrow(d, 86, 107, 112, 107)
        arrow(d, 210, 112, 240, 142)
        arrow(d, 210, 100, 240, 74)
        arrow(d, 380, 142, 350, 142)
        arrow(d, 380, 74, 350, 74)
        label(d, 240, 20, "Each Pod mounts models and reports read-only.", 7.7)
    else:
        training = kind == "train"
        names=["Operator" if training else "Student","train.py" if training else "Browser","Models" if training else "Flask API","Reports" if training else "Adapters"]
        xs=[50,165,300,425]
        for x,n in zip(xs,names):
            d.add(Rect(x-37,150,74,22,strokeColor=NAVY,fillColor=PALE))
            label(d,x,158,n,8)
            d.add(Line(x,20,x,150,strokeColor=colors.black,strokeWidth=.7,strokeDashArray=[3,3]))
        messages=([("Enter features",0,1),("POST /api/predict",1,2),("Validate input",2,2),("Run ML, DL, QML",2,3),("Results + audit",2,1)] if not training else
                  [("Run training",0,1),("Clean and split",1,1),("Fit three models",1,2),("Evaluate test set",2,1),("Save evidence",1,3)])
        for i,(t,a,b) in enumerate(messages):
            y=132-i*25
            arrow(d,xs[a],y,xs[b],y)
            label(d,(xs[a]+xs[b])/2,y+5,t,6.6)
    return d


def parse(path):
    lines=path.read_text(encoding="utf-8").splitlines()
    if len(lines) > 1 and lines[0].startswith("# ") and lines[1].startswith("# "):
        lines = lines[1:]
    placeholder_prefixes = (
        "Student: project team",
        "Project team:",
        "Tester: project team",
        "Class, section and instructor: complete on the private submission copy",
        "Instructor review: pending",
    )
    lines = [line for line in lines if not line.startswith(placeholder_prefixes)]
    story=[]
    private_meta=HERE.parent / ".private_submission.txt"
    i=0
    mermaid_number=0
    while i<len(lines):
        line=lines[i].strip()
        if not line:
            i+=1;continue
        if line.startswith("```mermaid"):
            i+=1
            while i<len(lines) and not lines[i].startswith("```"):
                i+=1
            i+=1
            if path.name == "SRS.md":
                kind="usecase"
            elif mermaid_number==0:
                kind="three-tier"
            elif mermaid_number==1:
                kind="component"
            elif mermaid_number==2:
                kind="deployment"
            elif mermaid_number==3:
                kind="compare"
            else:
                kind="train"
            mermaid_number+=1
            story.extend([diagram(kind),Spacer(1,6)])
            continue
        if line.startswith("![TriadLens UML use case diagram](diagrams/use_case.svg)"):
            story.extend([diagram("usecase"), Spacer(1, 6)])
            i += 1
            continue
        if line.startswith("```"):
            i += 1
            block = []
            while i < len(lines) and not lines[i].startswith("```"):
                block.append(plain(lines[i]).expandtabs(2))
                i += 1
            story.append(Preformatted("\n".join(block), styles["CodeX"], maxLineLength=94, splitChars=" "))
            i += 1
            continue
        if line.startswith("|"):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith("|"):
                cells=[x.strip() for x in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?",x) for x in cells):
                    rows.append(cells)
                i+=1
            if rows:
                widths = [511/len(rows[0])]*len(rows[0])
                if len(rows[0]) == 3:
                    widths = [115, 240, 156]
                elif len(rows[0]) == 6:
                    widths = [46, 240, 91, 45, 45, 44]
                table=Table([[Paragraph(markup(c),styles["HeaderCellX"] if n==0 else styles["CellX"]) for c in row] for n,row in enumerate(rows)],colWidths=widths,repeatRows=1,hAlign="LEFT")
                table.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor('#eeeeee')),("VALIGN",(0,0),(-1,-1),"TOP"),("LINEBELOW",(0,0),(-1,0),.7,colors.black),("LINEBELOW",(0,1),(-1,-1),.25,colors.HexColor('#aaaaaa')),("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]))
                wrapped = [Spacer(1,5),table,Spacer(1,8)]
                story.extend([KeepTogether(wrapped)] if len(rows) <= 9 else wrapped)
            continue
        if line.startswith("# "):
            story.append(Paragraph(markup(line[2:]),styles["DocTitleX"]))
            if private_meta.exists():
                identities = [value.strip() for value in private_meta.read_text(encoding="utf-8").splitlines() if value.strip()]
                if identities:
                    story.append(Paragraph(markup(identities[0]), styles["IdentityX"]))
                    for offset in range(1, len(identities), 2):
                        story.append(Paragraph(markup(";  ".join(identities[offset:offset + 2])), styles["IdentityX"]))
        elif line.startswith("## "):
            story.append(Paragraph(markup(line[3:]),styles["H1X"]))
        elif line.startswith("### "):
            story.append(Paragraph(markup(line[4:]),styles["H2X"]))
        elif re.match(r"^([-*]|\d+\.)\s+", line):
            content = re.sub(r"^([-*]|\d+\.)\s+", "", line)
            prefix = re.match(r"^([-*]|\d+\.)", line).group(0)
            story.append(Paragraph(markup(prefix + "  " + content), styles["BulletX"]))
        else:
            parts=[line]
            while i+1<len(lines) and lines[i+1].strip() and not lines[i+1].lstrip().startswith(("#","|","```","- ","* ")) and not re.match(r"^\d+\.\s", lines[i+1].lstrip()):
                i+=1;parts.append(lines[i].strip())
            story.append(Paragraph(markup(" ".join(parts)),styles["BodyX"]))
        i+=1
    return story


diagram_dir = HERE / "diagrams"
diagram_dir.mkdir(exist_ok=True)
renderSVG.drawToFile(diagram("usecase"), str(diagram_dir / "use_case.svg"))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor('#bbbbbb'))
    canvas.line(42, 32, 553, 32)
    canvas.setFont('Helvetica', 7)
    canvas.drawString(42, 20, doc.title.replace('_', ' '))
    canvas.drawRightString(553, 20, f"Page {doc.page}")
    canvas.restoreState()


for source in [
    HERE/"SRS.md",
    HERE/"System_Test_Plan.md",
    HERE/"Architecture_Design.md",
    HERE/"Product_Backlog_and_Two_Sprints.md",
    HERE/"Sprint_Execution_and_Demo.md",
    HERE/"DevOps_Verification.md",
]:
    target=OUT/source.with_suffix(".pdf").name
    doc=SimpleDocTemplate(str(target),pagesize=(595.28,841.89),leftMargin=42,rightMargin=42,topMargin=38,bottomMargin=42,title=source.stem,author="Project team")
    doc.build(parse(source), onFirstPage=footer, onLaterPages=footer)
    print(target)
