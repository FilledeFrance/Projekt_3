"""
main.py: třetí projekt do Engeto Online Python Akademie

author: Šárka Motylová
email: sarka.motylova@seznam.cz
"""

import sys
import csv
import time
import argparse
import threading
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ====================== Networking helpers ======================

def get_session():
    # Creates a requests session with retry logic.
    session = requests.Session()
    retries = Retry(
        total=5, backoff_factor=1,
        status_forcelist=[500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

session = get_session()

def soup(url: str) -> BeautifulSoup:
    # Safely requests a URL and returns BeautifulSoup.
    try:
        r = session.get(url, timeout=10)
        r.raise_for_status()
        return BeautifulSoup(r.text, "html.parser")
    except requests.RequestException as e:
        print(f"❌ Error downloading {url}: {e}")
        return BeautifulSoup("", "html.parser")

def clean(text: str) -> str:
    # Normalizes text by removing non-breaking spaces.
    return text.strip().replace("\xa0", " ")

# ====================== Scraping helpers ======================

def parse_district(s: BeautifulSoup):
    ids, towns, urls = [], [], []
    for row in s.select("table tr")[2:]:
        cells = row.find_all("td")
        if len(cells) < 3:
            continue
        town_id = clean(cells[0].get_text())
        town_name = clean(cells[1].get_text())
        link = cells[0].find("a")
        if link and "href" in link.attrs:
            url = "https://volby.cz/pls/ps2017nss/" + link["href"]
            ids.append(town_id)
            towns.append(town_name)
            urls.append(url)
    return ids, towns, urls

def parse_parties(s: BeautifulSoup):
    # Collects party names from party tables on a town page.
    # Matches cells whose 'headers' attribute contains both tokens:
    #   - t1sa1 & t1sb2  (first table)
    #   - t2sa1 & t2sb2  (second table)
    names = [
        clean(td.get_text())
        for td in s.select(
            'td[headers*="t1sa1"][headers*="t1sb2"], '
            'td[headers*="t2sa1"][headers*="t2sb2"]'
        )
    ]
    # Fallback: some variants use overflow_name on party cells
    if not names:
        names = [clean(td.get_text()) for td in s.select("td.overflow_name")]

    # Deduplicates while preserving order (just in case):
    seen = set()
    unique = []
    for n in names:
        if n and n not in seen:
            seen.add(n)
            unique.append(n)
    return unique

def parse_voter_stats(s: BeautifulSoup):
    voters = clean(s.select_one("td[headers='sa2']").get_text())
    envelopes = clean(s.select_one("td[headers='sa3']").get_text())
    valid = clean(s.select_one("td[headers='sa6']").get_text())
    return voters, envelopes, valid

def parse_votes_absolute(town: BeautifulSoup):
    # absolute counts from both tables
    cells = town.select('td.cislo[headers*="t1sb3"], td.cislo[headers*="t2sb3"]')
    if not cells:  # broad fallback
        cells = town.select('td[headers*="sb3"]')
    return [clean(c.get_text()) for c in cells]

def parse_votes_percent(town: BeautifulSoup):
    # percentages from both tables
    cells = town.select('td.cislo[headers*="t1sb4"], td.cislo[headers*="t2sb4"]')
    if not cells:  # broad fallback
        cells = town.select('td[headers*="sb4"]')
    return [clean(c.get_text()) for c in cells]

# ====================== Spinner ======================

class Spinner:
    def __init__(self, message="DOWNLOADING DATA FROM URL"):
        self.message = message
        self.running = False
        self.thread = None

    def spin(self):
        while self.running:
            for ch in "|/-\\":
                sys.stdout.write(f"\r{self.message}... {ch}")
                sys.stdout.flush()
                time.sleep(0.1)

    def __enter__(self):
        self.running = True
        self.thread = threading.Thread(target=self.spin)
        self.thread.start()

    def __exit__(self, exc_type, exc, tb):
        self.running = False
        if self.thread:
            self.thread.join()
        sys.stdout.write("\r" + " " * (len(self.message) + 10) + "\r")
        sys.stdout.flush()

# ====================== Runner ======================

def run(url: str, out_csv: str, debug: bool = False):
    dist = soup(url)
    ids, towns, urls = parse_district(dist)

    # Processes first town to get list of parties: 
    first_town_soup = soup(urls[0])
    parties = parse_parties(first_town_soup)

    if debug:
        print(f"Found {len(ids)} towns. Example: {ids[0]} {towns[0]}")
        print(f"Detected {len(parties)} parties. First 5: {parties[:5]}")

    rows = []
    total = len(urls)

    for i, (tid, tname, turl) in enumerate(zip(ids, towns, urls), 1):
        print(f" [{i}/{total}] {tid} {tname} …")

        # Reuses already parsed first town:
        if i == 1:
            t = first_town_soup
        else:
            t = soup(turl)

        voters, envelopes, valid_votes = parse_voter_stats(t)

        votes_abs = parse_votes_absolute(t)
        votes_pct = parse_votes_percent(t)

        if len(votes_abs) < len(parties):
            votes_abs += [""] * (len(parties) - len(votes_abs))
        else:
            votes_abs = votes_abs[:len(parties)]

        if len(votes_pct) < len(parties):
            votes_pct += [""] * (len(parties) - len(votes_pct))
        else:
            votes_pct = votes_pct[:len(parties)]

        combined = []
        for abs_val, pct_val in zip(votes_abs, votes_pct):
            if pct_val and "%" not in pct_val:
                pct_val += " %"
            combined.extend([abs_val, pct_val])

        rows.append([tid, tname, voters, envelopes, valid_votes] + combined)
        time.sleep(0.2)

    # CSV - build header and write file:
    header = [
        "Town ID",
        "Town name",
        "Registered voters",
        "Issued envelopes",
        "Valid votes",
    ]
    for p in parties:
        header.append(f"{p} – Votes")
        header.append(f"{p} – %")

    print(f"💾 Writing CSV: {out_csv}")
    with open(out_csv, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"✅ Done. Saved to {out_csv}")

# ====================== Custom Argument Parser ======================

def parse_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("url", nargs="?")
    parser.add_argument("output", nargs="?")
    args = parser.parse_args()

    if not args.url or not args.output:
        print(
            "⚠️ There must be a web page link and a name of the CSV file in this order:\n"
            '   python main.py "web page link" file.csv\n'
        )
        sys.exit(1)
    return args

if __name__ == "__main__":
    args = parse_args()
    with Spinner():
        run(args.url, args.output)
