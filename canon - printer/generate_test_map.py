from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from decimal import Decimal, getcontext

getcontext().prec = 30
width, height = A4

def cm_to_pt(cm):
    return Decimal(cm) * (Decimal(72) / Decimal('2.54'))


c = canvas.Canvas("map.pdf", pagesize=A4)
c.setFillColorRGB(0.0, 0.0, 0.0)
c.setLineWidth(0.1)
c.rect(1, 1, width-2, height-2, stroke=1, fill=0)
c.save()