"""Scrape the public contribution calendar (no token needed) -> data/contributions.json
Username comes from GITHUB_USERNAME, else GITHUB_REPOSITORY_OWNER (set automatically in Actions)."""
import json, os, re, sys
from datetime import date, timedelta

import requests
from bs4 import BeautifulSoup

user = os.environ.get("GITHUB_USERNAME") or os.environ.get("GITHUB_REPOSITORY_OWNER") or (sys.argv[1] if len(sys.argv) > 1 else None)
if not user:
    sys.exit("Set GITHUB_USERNAME or pass the username as an argument")

html = requests.get(f"https://github.com/users/{user}/contributions", timeout=30,
                    headers={"User-Agent": "profile-readme-bot"}).text
soup = BeautifulSoup(html, "html.parser")

tips = {t.get("for"): t.get_text(" ", strip=True) for t in soup.find_all("tool-tip")}
days = []
for td in soup.select("td.ContributionCalendar-day[data-date]"):
    m = re.match(r"(\d+)", tips.get(td.get("id"), ""))
    days.append({"date": td["data-date"], "level": int(td.get("data-level", 0)),
                 "count": int(m.group(1)) if m else 0})
days.sort(key=lambda d: d["date"])
if not days:
    sys.exit("No contribution cells found — GitHub markup may have changed")

total = sum(d["count"] for d in days)
longest = cur = 0
for d in days:
    cur = cur + 1 if d["count"] else 0
    longest = max(longest, cur)
# current streak: allow today to still be empty
streak, i = 0, len(days) - 1
if days[i]["count"] == 0:
    i -= 1
while i >= 0 and days[i]["count"]:
    streak += 1
    i -= 1
best = max(days, key=lambda d: d["count"])
months = {}
for d in days:
    months[d["date"][:7]] = months.get(d["date"][:7], 0) + d["count"]

os.makedirs("data", exist_ok=True)
with open("data/contributions.json", "w") as f:
    json.dump({"user": user, "total": total, "current_streak": streak, "longest_streak": longest,
               "best_day": best, "months": months, "days": days}, f, indent=1)
print(f"{user}: {total} contributions, streak {streak}, longest {longest}")
