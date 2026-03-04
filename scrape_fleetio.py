"""
Crawl fleetio.com and export every page's content to fleetio_pages.csv
Columns: url, title, meta_description, h1, h2s, body_text
"""
import csv, re, time
from collections import deque
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

DOMAIN = "fleetio.com"
START  = "https://www.fleetio.com/"
OUT    = "fleetio_pages.csv"
DELAY  = 0.5          # seconds between requests
MAX    = 500          # safety cap

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    )
}

SKIP_EXTS = re.compile(
    r"\.(pdf|png|jpg|jpeg|gif|svg|ico|webp|mp4|zip|xml|json|css|js)(\?.*)?$",
    re.IGNORECASE,
)

session = requests.Session()
session.headers.update(HEADERS)


def same_domain(url):
    h = urlparse(url).netloc.lstrip("www.")
    return h == DOMAIN or h.endswith("." + DOMAIN)


def clean(text):
    return " ".join(text.split())


def scrape(url):
    try:
        r = session.get(url, timeout=15, allow_redirects=True)
        if "text/html" not in r.headers.get("Content-Type", ""):
            return None, []
        r.raise_for_status()
    except Exception as e:
        print(f"  SKIP {url}: {e}")
        return None, []

    soup = BeautifulSoup(r.text, "lxml")

    # collect outgoing links on same domain
    links = []
    for a in soup.find_all("a", href=True):
        href = urljoin(url, a["href"].split("#")[0].strip())
        if same_domain(href) and not SKIP_EXTS.search(href):
            links.append(href)

    # remove nav / footer / script noise before extracting body text
    for tag in soup(["script", "style", "noscript", "header", "footer", "nav"]):
        tag.decompose()

    title       = clean(soup.title.get_text()) if soup.title else ""
    meta_desc   = ""
    md = soup.find("meta", attrs={"name": "description"})
    if md:
        meta_desc = clean(md.get("content", ""))
    h1 = clean(soup.h1.get_text()) if soup.h1 else ""
    h2s = " | ".join(clean(h.get_text()) for h in soup.find_all("h2"))
    body = clean(soup.get_text(" ", strip=True))

    row = {
        "url":              url,
        "title":            title,
        "meta_description": meta_desc,
        "h1":               h1,
        "h2s":              h2s,
        "body_text":        body[:4000],   # cap per-cell size
    }
    return row, links


visited = set()
queue   = deque([START])
rows    = []

with open(OUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["url", "title", "meta_description", "h1", "h2s", "body_text"],
    )
    writer.writeheader()

    while queue and len(visited) < MAX:
        url = queue.popleft()
        if url in visited:
            continue
        visited.add(url)

        print(f"[{len(visited):>3}] {url}")
        row, links = scrape(url)

        if row:
            writer.writerow(row)
            f.flush()
            rows.append(row)

        for link in links:
            if link not in visited:
                queue.append(link)

        time.sleep(DELAY)

print(f"\nDone — {len(rows)} pages written to {OUT}")
