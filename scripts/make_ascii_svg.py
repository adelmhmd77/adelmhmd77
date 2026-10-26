"""source-prepped.png -> adel-ascii.svg (monochrome, rows wipe in left-to-right, prints once)."""
import numpy as np
from PIL import Image
from xml.sax.saxutils import escape

RAMP = " .`:-=+*cs#%@"  # bright (sparse) -> dark (dense)
COLS = 100
FONT, CW, RH = 7, 4.2, 8     # font size, char width, row height
COLOR = "#c9d1d9"

img = Image.open("source-prepped.png").convert("L")
rows = max(1, int(COLS * img.height / img.width * 0.5))
a = np.array(img.resize((COLS, rows), Image.LANCZOS)) / 255.0

W, H = COLS * CW, rows * RH + 8
o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}">',
     f'<rect width="100%" height="100%" fill="#0d1117"/>',
     f'<style>text{{font-family:Menlo,Consolas,"Liberation Mono",monospace;font-size:{FONT}px;fill:{COLOR};white-space:pre}}</style>',
     "<defs>"]
for r in range(rows):
    b = r * 0.06
    o.append(f'<clipPath id="c{r}"><rect x="0" y="{r*RH+4}" height="{RH}" width="0">'
             f'<animate attributeName="width" from="0" to="{W:.0f}" dur="0.5s" begin="{b:.2f}s" fill="freeze"/></rect></clipPath>')
o.append("</defs>")
for r in range(rows):
    line = "".join(RAMP[min(len(RAMP) - 1, int((1 - v) * len(RAMP)))] for v in a[r])
    if line.strip():
        o.append(f'<text x="0" y="{r*RH+RH+2}" textLength="{W:.0f}" lengthAdjust="spacing" '
                 f'clip-path="url(#c{r})" xml:space="preserve">{escape(line)}</text>')
o.append("</svg>")
open("adel-ascii.svg", "w", encoding="utf-8").write("\n".join(o))
print(f"wrote adel-ascii.svg ({COLS}x{rows})")
