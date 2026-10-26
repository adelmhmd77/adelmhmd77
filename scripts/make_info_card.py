"""Hand-authored neofetch-style info card -> info-card.svg
Set STATIC=1 to emit a frozen frame (no animation) for local previews."""
import os
from xml.sax.saxutils import escape

STATIC = os.environ.get("STATIC") == "1"
W, H = 490, 340
BG, BORDER, BAR = "#0d1117", "#30363d", "#161b22"
KEY, VAL, DIM, ACCENT = "#58a6ff", "#c9d1d9", "#6e7681", "#3fb950"

# (key, value) rows; ("", "") = spacer; ("#", text) = section heading
ROWS = [
    ("name", "Adel Mohammed"),
    ("role", "Full-Stack Developer · SEO Specialist"),
    ("where", "Istanbul, Turkey · Cairo, Egypt"),
    ("status", "Open to freelance & full-time roles"),
    ("", ""),
    ("#", "stack"),
    ("front", "Next.js · React · TypeScript · Tailwind"),
    ("back", "Node.js · Express"),
    ("data", "PostgreSQL · Supabase · MongoDB · Firebase"),
    ("cms", "WordPress"),
    ("", ""),
    ("#", "highlights"),
    ("shipped", "20+ websites built"),
    ("seo", "10+ SEO projects managed"),
    ("speed", "New articles indexed within 48 hrs"),
]

LINE_H, TOP, LEFT = 18, 52, 24
out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
out.append("""<style>
text{font-family:'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace;font-size:12.5px;white-space:pre}
.k{fill:%s;font-weight:bold}.v{fill:%s}.h{fill:%s;font-weight:bold}.d{fill:%s}
.l{%s}
@keyframes in{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}
</style>""" % (KEY, VAL, ACCENT, DIM,
               "" if STATIC else "opacity:0;animation:in .35s ease-out forwards"))
out.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="10" fill="{BG}" stroke="{BORDER}"/>')
out.append(f'<path d="M.5 10.5a10 10 0 0 1 10-10h{W-21}a10 10 0 0 1 10 10V32H.5z" fill="{BAR}"/>')
for i, c in enumerate(("#ff5f56", "#ffbd2e", "#27c93f")):
    out.append(f'<circle cx="{20+i*18}" cy="17" r="5.5" fill="{c}"/>')
out.append(f'<text x="{W/2}" y="21" text-anchor="middle" class="d">adel@github: ~ — neofetch</text>')

y, n = TOP, 0
for k, v in ROWS:
    delay = f' style="animation-delay:{0.15 + n*0.12:.2f}s"'
    if k == "":
        y += LINE_H // 2
        continue
    if k == "#":
        out.append(f'<text x="{LEFT}" y="{y}" class="h l"{delay}>── {escape(v)} ──────────────</text>')
    else:
        out.append(f'<text x="{LEFT}" y="{y}" class="l"{delay}><tspan class="k">{k:<8}</tspan><tspan class="v">{escape(v)}</tspan></text>')
    y += LINE_H
    n += 1
out.append("</svg>")

with open("info-card.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("wrote info-card.svg")
