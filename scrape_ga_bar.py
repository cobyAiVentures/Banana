"""
Georgia Bar Medical Malpractice Attorney Scraper
Scrapes: https://gabar.reliaguide.com
Output:  medical_malpractice_georgia.csv
"""

import csv
import json
import time
import sys

try:
    import requests
except ImportError:
    sys.exit("Missing dependency. Run:  pip install requests")

try:
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("Missing dependency. Run:  pip install beautifulsoup4")

# ── Configuration ────────────────────────────────────────────────────────────
BASE_URL   = "https://gabar.reliaguide.com"
SEARCH_URL = (
    f"{BASE_URL}/lawyer/search"
    "?category.equals=Medical%20Malpractice"
    "&categoryId.equals=454"
    "&memberTypeId.equals=1"
)
OUTPUT_FILE = "medical_malpractice_georgia.csv"
PAGE_SIZE   = 25        # adjust if the site uses a different page size
DELAY_SEC   = 1.5       # polite delay between requests

HEADERS = {
    "User-Agent":      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/122.0.0.0 Safari/537.36",
    "Accept":          "text/html,application/xhtml+xml,application/xml;q=0.9,"
                       "image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer":         BASE_URL,
    "Connection":      "keep-alive",
}

CSV_FIELDS = [
    "First Name", "Middle Name", "Last Name",
    "Firm Name", "Firm Location",
    "Office Phone", "Cell Phone", "Email",
]

# ── Helpers ──────────────────────────────────────────────────────────────────

def get_session() -> requests.Session:
    s = requests.Session()
    s.headers.update(HEADERS)
    # warm-up: visit homepage to get cookies
    try:
        s.get(BASE_URL, timeout=15)
        time.sleep(1)
    except requests.RequestException:
        pass
    return s


def parse_name(full_name: str) -> tuple[str, str, str]:
    """Split 'First [Middle] Last' into three parts (best-effort)."""
    parts = full_name.strip().split()
    if len(parts) == 1:
        return parts[0], "", ""
    if len(parts) == 2:
        return parts[0], "", parts[1]
    # 3+ parts: first, middle(s), last
    return parts[0], " ".join(parts[1:-1]), parts[-1]


def extract_attorneys_html(soup: BeautifulSoup) -> list[dict]:
    """
    Parse attorney cards from HTML.
    The selectors below are best-guess from common reliaguide layouts —
    the script will print a warning if nothing is found so you can adjust.
    """
    attorneys = []

    # Try common card/row selectors used by reliaguide sites
    cards = (
        soup.select("div.lawyer-card")
        or soup.select("div.attorney-card")
        or soup.select("div.search-result-item")
        or soup.select("tr.lawyer-row")
        or soup.select("li.lawyer-list-item")
        or soup.select("[class*='lawyer']")
        or soup.select("[class*='attorney']")
    )

    if not cards:
        print("[WARN] No attorney cards found with default selectors.")
        print("       Saving raw HTML to 'debug_page.html' for inspection.")
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(str(soup))
        return attorneys

    for card in cards:
        text = lambda sel: (card.select_one(sel) or {}).get_text(strip=True) if card.select_one(sel) else ""

        full_name = (
            text(".lawyer-name") or text(".attorney-name")
            or text("h2") or text("h3") or text(".name") or ""
        )
        first, middle, last = parse_name(full_name)

        firm = (
            text(".firm-name") or text(".organization") or text(".company") or ""
        )
        location = (
            text(".location") or text(".city") or text(".address") or ""
        )
        office_phone = (
            text(".office-phone") or text(".phone") or text("[class*='phone']") or ""
        )
        cell_phone = text(".cell-phone") or text(".mobile") or ""
        email_tag = card.select_one("a[href^='mailto:']")
        email = email_tag["href"].replace("mailto:", "") if email_tag else ""

        attorneys.append({
            "First Name":    first,
            "Middle Name":   middle,
            "Last Name":     last,
            "Firm Name":     firm,
            "Firm Location": location,
            "Office Phone":  office_phone,
            "Cell Phone":    cell_phone,
            "Email":         email,
        })

    return attorneys


def extract_attorneys_json(data) -> list[dict]:
    """Handle JSON API responses (common with JHipster / Spring Boot backends)."""
    attorneys = []
    items = data if isinstance(data, list) else data.get("content", data.get("results", []))

    for item in items:
        full_name = (
            item.get("name") or item.get("fullName") or
            f"{item.get('firstName','')} {item.get('lastName','')}".strip()
        )
        first, middle, last = parse_name(full_name)
        if item.get("firstName"):
            first  = item.get("firstName", first)
            middle = item.get("middleName", middle)
            last   = item.get("lastName", last)

        attorneys.append({
            "First Name":    first,
            "Middle Name":   middle,
            "Last Name":     last,
            "Firm Name":     item.get("firmName") or item.get("organization") or "",
            "Firm Location": item.get("city") or item.get("location") or item.get("address") or "",
            "Office Phone":  item.get("officePhone") or item.get("phone") or "",
            "Cell Phone":    item.get("cellPhone") or item.get("mobile") or "",
            "Email":         item.get("email") or "",
        })

    return attorneys


def fetch_page(session: requests.Session, url: str, page: int) -> requests.Response | None:
    params = {"page": page, "size": PAGE_SIZE}
    try:
        resp = session.get(url, params=params, timeout=20)
        resp.raise_for_status()
        return resp
    except requests.HTTPError as e:
        print(f"[ERROR] HTTP {e.response.status_code} on page {page}: {e}")
    except requests.RequestException as e:
        print(f"[ERROR] Network error on page {page}: {e}")
    return None


def scrape_all(session: requests.Session) -> list[dict]:
    all_attorneys = []
    page = 0

    while True:
        print(f"  Fetching page {page + 1}...", end=" ", flush=True)
        resp = fetch_page(session, SEARCH_URL, page)
        if resp is None:
            break

        content_type = resp.headers.get("Content-Type", "")

        if "application/json" in content_type:
            try:
                data = resp.json()
            except json.JSONDecodeError:
                print("JSON decode error — stopping.")
                break
            batch = extract_attorneys_json(data)
        else:
            soup  = BeautifulSoup(resp.text, "html.parser")
            batch = extract_attorneys_html(soup)

        print(f"found {len(batch)} attorneys.")

        if not batch:
            break

        all_attorneys.extend(batch)
        page += 1
        time.sleep(DELAY_SEC)

        # Safety: if fewer results than page size, we're on the last page
        if len(batch) < PAGE_SIZE:
            break

    return all_attorneys


def save_csv(attorneys: list[dict], filename: str) -> None:
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(attorneys)
    print(f"\n[OK] Saved {len(attorneys)} attorneys to '{filename}'")


def preview(attorneys: list[dict], n: int = 3) -> None:
    print(f"\n── Sample Output (first {min(n, len(attorneys))} records) ──")
    for a in attorneys[:n]:
        for k, v in a.items():
            print(f"  {k:<16}: {v}")
        print()


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("Georgia Bar — Medical Malpractice Scraper")
    print(f"Target : {SEARCH_URL}")
    print(f"Output : {OUTPUT_FILE}\n")

    session = get_session()
    attorneys = scrape_all(session)

    if not attorneys:
        print("\n[WARN] No data collected.")
        print("  The site may require JavaScript rendering (try Playwright/Selenium),")
        print("  or check 'debug_page.html' to inspect what was returned.")
        sys.exit(1)

    preview(attorneys)
    save_csv(attorneys, OUTPUT_FILE)


if __name__ == "__main__":
    main()
