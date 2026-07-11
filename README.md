# Snap Dossier

A static, single-page Marvel Snap collection dossier for GitHub Pages. It reads
your local `CollectionState.json` in the browser, renders booster history, your
infinity-split roster, dormant cards, a sortable collection grid, and
**per-series completion** — all without a server and without uploading anything.

Your collection lives only in your browser (`localStorage`). The only thing in
this repo is the public card list (`cards.json`), which carries no personal data.

## What's here

    index.html                     the whole app (HTML + CSS + JS, no build step)
    cards.json                     slim card list; refreshed by the Action
    scripts/refresh_cards.py       fetches + slims the MarvelSnapZone card data
    .github/workflows/refresh-cards.yml   weekly + on-demand refresh of cards.json

## Deploy (about 3 minutes)

1. **Create a repo** and push these files to `main`.
2. **Enable Pages:** Settings → Pages → Build and deployment → *Deploy from a
   branch* → Branch `main`, folder `/ (root)` → Save. Your site appears at
   `https://<you>.github.io/<repo>/` within a minute or two.
3. **Populate the card data:** Actions tab → *Refresh card data* → *Run
   workflow*. This fetches ~500 cards from MarvelSnapZone, slims them, and
   commits `cards.json`. (It also runs automatically every Monday.)
4. **Open the page and click Sync.** Pick your `CollectionState.json` at:

       %USERPROFILE%\AppData\LocalLow\Second Dinner\SNAP\Standalone\States\nvprod\CollectionState.json

   It parses in the browser, renders, and saves to `localStorage` so a reload
   restores it. On Chromium (Edge/Chrome) the file handle is remembered, so
   future syncs are one click.

## How syncing works

A hosted page can't read your disk on its own — you pick the file once. On
Chromium the File System Access API remembers the handle (via IndexedDB), so
after the first grant, **Sync re-reads the same file in one click** — play a
match, hit Sync, watch the numbers move. Firefox falls back to a file picker
each time. Note: `CollectionState.json` is only rewritten by the game after you
finish a match, so freshly-earned cards appear after your next game.

## Series completion

Completion needs the full card universe, which the page loads from its own
`cards.json` (same-origin — no CORS issues). The **Refresh card data** workflow
keeps that file current through monthly Series Drops. Run it manually anytime
after a drop, or wait for the weekly schedule. Ownership is matched on raw
`CardDefId`, so it's exact rather than fuzzy name-matching; tokens, created
cards, and unreleased cards are excluded from the denominators.

## Refreshing card data locally

    python scripts/refresh_cards.py          # fetch live, write cards.json

The script refuses to overwrite `cards.json` with a suspiciously short list, so
a transient endpoint failure won't blow away good data.

## Notes

- No build, no dependencies, no framework. Just static files.
- Card data © their respective owners; sourced from MarvelSnapZone's public
  endpoint. This project stores no personal collection data server-side.
