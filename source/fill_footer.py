# Extends the blue footer band on the last PDF page down to the page edge.
import sys, io
import pypdfium2 as pdfium
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
path = sys.argv[1]
doc = pdfium.PdfDocument(path); last = doc[len(doc) - 1]
img = last.render(scale=1).to_pil().convert('RGB'); W, H = img.size
blue = (40, 120, 184)
near = lambda p: all(abs(a - b) < 12 for a, b in zip(p, blue))
bottom = None
for y in range(H - 1, -1, -1):
    if near(img.getpixel((2, y))):
        bottom = y; break
doc.close()
if bottom is None or bottom >= H - 2:
    print('no fill needed'); sys.exit()
r = PdfReader(path); page = r.pages[-1]
pw, ph = float(page.mediabox.width), float(page.mediabox.height)
gap = (H - 1 - bottom) * ph / H
buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(pw, ph))
c.setFillColorRGB(40/255, 120/255, 184/255); c.setStrokeColorRGB(40/255, 120/255, 184/255)
c.rect(0, 0, pw, gap + 1.5, stroke=0, fill=1); c.save(); buf.seek(0)
page.merge_page(PdfReader(buf).pages[0])
w = PdfWriter(); [w.add_page(p) for p in r.pages]
with open(path, 'wb') as fh: w.write(fh)
print(f'filled {gap:.0f}pt under footer')
