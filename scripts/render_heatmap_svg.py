"""data/contributions.json -> contrib-heatmap.svg (53x7 rounded boxes, diagonal slide-in, plays once)."""
import json
from datetime import date

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
BOX, GAP, LEFT, TOP = 12, 3, 40, 44
STEP = BOX + GAP

data = json.load(open("data/contributions.json"))
days = data["days"]
first = date.fromisoformat(days[0]["date"])
offset = (first.weekday() + 1) % 7  # GitHub weeks start on Sunday

max_count = max(d["count"] for d in days) or 1
def level(d):  # use level 5 as a neon top end for the busiest days
    return 5 if d["level"] == 4 and d["count"] >= 0.75 * max_count else d["level"]

cols = (len(days) + offset + 6) // 7
W = LEFT + cols * STEP + 20
H = TOP + 7 * STEP + 52

o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
     """<style>
text{font-family:'SFMono-Regular',Consolas,Menlo,monospace;font-size:10px;fill:#8b949e}
.c{opacity:0;animation:s .45s ease-out forwards}
@keyframes s{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:none}}
</style>""",
     f'<rect width="{W}" height="{H}" rx="10" fill="#0d1117" stroke="#30363d"/>']

# month labels
seen = None
for i, d in enumerate(days):
    col, m = (i + offset) // 7, d["date"][5:7]
    if m != seen and (i + offset) % 7 < 7:
        seen = m
        name = date.fromisoformat(d["date"]).strftime("%b")
        o.append(f'<text x="{LEFT + col*STEP}" y="{TOP-10}">{name}</text>')
for r, lab in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
    o.append(f'<text x="8" y="{TOP + r*STEP + 10}">{lab}</text>')

for i, d in enumerate(days):
    col, row = (i + offset) // 7, (i + offset) % 7
    delay = (col + row) * 0.018
    o.append(f'<rect class="c" style="animation-delay:{delay:.2f}s" x="{LEFT+col*STEP}" y="{TOP+row*STEP}" '
             f'width="{BOX}" height="{BOX}" rx="3" fill="{PALETTE[level(d)]}"><title>{d["count"]} on {d["date"]}</title></rect>')

# legend + stats footer
ly = TOP + 7 * STEP + 20
o.append(f'<text x="{LEFT}" y="{ly+9}">{data["total"]:,} contributions in the last year · '
         f'current streak {data["current_streak"]}d · longest {data["longest_streak"]}d · '
         f'best day {data["best_day"]["count"]}</text>')
lx = W - 20 - (len(PALETTE) * STEP + 70)
o.append(f'<text x="{lx}" y="{ly+9}">Less</text>')
for i, c in enumerate(PALETTE):
    o.append(f'<rect x="{lx+30+i*STEP}" y="{ly}" width="{BOX}" height="{BOX}" rx="3" fill="{c}"/>')
o.append(f'<text x="{lx+34+len(PALETTE)*STEP}" y="{ly+9}">More</text>')
o.append("</svg>")

open("contrib-heatmap.svg", "w", encoding="utf-8").write("\n".join(o))
print("wrote contrib-heatmap.svg")
