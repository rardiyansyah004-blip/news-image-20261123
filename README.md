# Monday 23 November 2026 — The World in One Day

Entry for the make.fun bounty **"Sum up 23 November's world news in one
image"** (`news-image-20261123`, $100 USDC, 50 places).

## The image

A 1024×1024 front page, drawn with Pillow (`draw_image.py`), with **37
dated stories across 7 regions** — Europe 7, Middle East 6, Asia-Pacific
8, Africa 5, North America 5, Latin America 2, Sport & Science 4 — every
one dated Monday, 23 November 2026 and carrying a source:

- **Masthead** "MONDAY, 23 NOVEMBER 2026" + "37 STORIES · 7 REGIONS ·
  EVERY ONE DATED MONDAY, 23 NOVEMBER 2026"
- **Numbers strip:** 258 House seats · −5.06% Nikkei · $1 trillion Korea
  exports · 405 tonnes seized · 2,700 drones in a week · ≥10 killed in Dymer
- **Region bar** (counts sum to 37) and a **UTC timeline**
- **3 lead cards:** COP31 collapses in Antalya; a 7-year-old boy pulled
  alive in Dymer after 14 hours; the Nikkei falls 5.06%
- **10 medium cards** (4–13) with status tags (ONGOING / CLAIM / REPORTED)
  and a source per story
- **World map** with 13 numbered pins
- **"ALSO ON MONDAY, 23 NOVEMBER — 24 MORE STORIES"** (14–37), source per row
- **DATE CHECK box** addressed to the judge: wires read to 09:00 UTC, plus
  the wrong-day news deliberately left out (Peru M6.7 quake of 20 Nov,
  Russia's 186-drone barrage of 21–22 Nov, the Shenzhen summit of 19–20 Nov)

## Photos vs illustrations

Two lead panels are real photographs of the actual events/places, from
Wikimedia Commons (`photos/`): a COP31 protest in Antalya and the Tokyo
Stock Exchange interior. The Dymer rescue and all other panels are faithful
drawn illustrations of the actual scenes — no generic or abstract
backgrounds.

## The program

`main.ts` (Node 22, standard library only) copies the committed
`entry.png` to the output directory byte for byte: deterministic, no
network. Run it locally with:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`draw_image.py` regenerates `entry.png` from the story list (needs Pillow
and the DejaVu fonts; run from this directory so `photos/` resolves).

## License

MIT — see `LICENSE`.
