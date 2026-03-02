import csv, json, time, urllib.request

BASE_URL = (
    "https://gabar.reliaguide.com/api/public/profiles"
    "?category.equals=Medical+Malpractice"
    "&categoryId.equals=454"
    "&memberTypeId.equals=1"
    "&size=20"
    "&page={page}"
)

FIELDS = ["First Name", "Middle Name", "Last Name", "Firm Name",
          "Firm Location", "Office Phone", "Cell Phone", "Email"]


def fetch_page(page):
    url = BASE_URL.format(page=page)
    req = urllib.request.Request(url, headers={
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    })
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode())


def row(a):
    loc = a.get("primaryLocation") or {}
    return {
        "First Name":    a.get("firstName", ""),
        "Middle Name":   a.get("middleName", ""),
        "Last Name":     a.get("lastName", ""),
        "Firm Name":     a.get("firmName", ""),
        "Firm Location": f"{loc.get('city','')}, {loc.get('region','')}".strip(", "),
        "Office Phone":  loc.get("phone") or "",
        "Cell Phone":    loc.get("cell") or "",
        "Email":         a.get("email") or "",
    }


all_rows = []
page = 0
while True:
    print(f"Fetching page {page}...", end=" ", flush=True)
    try:
        data = fetch_page(page)
    except Exception as e:
        print(f"ERROR: {e}")
        break

    if not data:
        print("empty — done.")
        break

    all_rows.extend(row(a) for a in data)
    print(f"{len(data)} records (total so far: {len(all_rows)})")

    if len(data) < 20:
        break

    page += 1
    time.sleep(0.5)   # be polite

with open("medical_malpractice_georgia.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    w.writeheader()
    w.writerows(all_rows)

print(f"\nDone — {len(all_rows)} total records written to medical_malpractice_georgia.csv")
