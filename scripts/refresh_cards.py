#!/usr/bin/env python3
"""Fetch the MarvelSnapZone card list and write a slim cards.json for the site.

Run by the "Refresh card data" GitHub Action. Keeps only the fields the site
needs (carddefid, name, source, source_slug, status, type, art, cost, power) so
the committed cards.json stays small. Refuses to overwrite with a short list.

Usage:
  python scripts/refresh_cards.py                # fetch live
  python scripts/refresh_cards.py sample.json    # slim a local payload (testing)
"""
import json
import sys
import urllib.request

URL = "https://marvelsnapzone.com/getinfo/?searchtype=cards&searchcardstype=true"
FIELDS = ("carddefid", "name", "source", "source_slug", "status", "type", "art", "ability", "flavor")
NUM_FIELDS = ("cost", "power")  # integers; kept as-is (0 is valid, not "missing")
MIN_CARDS = 100  # guard against committing a broken/empty pull


def as_int(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, int):
        return v
    if isinstance(v, str) and v.strip().lstrip("-").isdigit():
        return int(v)
    return None


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "snap-dossier/1.0 (+github-pages)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8-sig"))


def slim(payload):
    cards = (payload.get("success") or {}).get("cards") or []
    out = []
    for c in cards:
        cid = c.get("carddefid")
        if not cid:
            continue
        rec = {k: (c.get(k) or "") for k in FIELDS}
        for k in NUM_FIELDS:
            rec[k] = as_int(c.get(k))
        out.append(rec)
    return out


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else URL
    is_local = not src.startswith("http")
    payload = json.load(open(src, encoding="utf-8")) if is_local else fetch(src)
    cards = slim(payload)
    if len(cards) < MIN_CARDS and not is_local:
        print(f"refusing to write: only {len(cards)} cards (endpoint may be broken)", file=sys.stderr)
        sys.exit(1)
    with open("cards.json", "w", encoding="utf-8") as f:
        json.dump(cards, f, separators=(",", ":"), ensure_ascii=False)
    print(f"wrote cards.json with {len(cards)} cards")


if __name__ == "__main__":
    main()
