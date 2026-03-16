from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from decimal import Decimal, getcontext

getcontext().prec = 30
width, height = A4

# Distance from each paper edge to the box, in millimeters.
BOX_EDGE_DISTANCE_MM = Decimal("5")


def mm_to_pt(mm):
    return Decimal(mm) * (Decimal(72) / Decimal('25.4'))


margin_pt = float(mm_to_pt(BOX_EDGE_DISTANCE_MM))
if margin_pt * 2 >= width or margin_pt * 2 >= height:
    raise ValueError("BOX_EDGE_DISTANCE_MM is too large for the selected page size.")


c = canvas.Canvas("map.pdf", pagesize=A4)
c.setFillColorRGB(0.0, 0.0, 0.0)
c.setLineWidth(0.1)
c.rect(margin_pt, margin_pt, width - 2 * margin_pt, height - 2 * margin_pt, stroke=1, fill=0)
c.save()