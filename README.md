# Friday 20 November 2026 — The World in One Day

One broadsheet front-page image summing up the world's news of Friday 20 November 2026: Russian missiles hit three Kyiv bridges, Cyclone Akvan comes ashore in eastern India, an AI sell-off sinks Asia's markets, and the UK and EU seal a "reset" deal — 35 stories in all, every one dated that day.

[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![Rank](https://make.fun/badge/news-image-20261120/Iruwae/news-image-20261120-entry/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![Reward](https://make.fun/badge/news-image-20261120/Iruwae/news-image-20261120-entry/reward.svg)](https://make.fun/bounty/news-image-20261120)

See the competition: [news-image-20261120 on make.fun](https://make.fun/bounty/news-image-20261120)

## How it is built

`draw.py` (Python + PIL, no network, no photos) draws the whole 1024×1024 front page — masthead, six-number stat strip, three big leads, ten small drawn stories, a pinned world map, 22 more briefs, and a DATE CHECK box that leaves out Thursday's news and anything not yet happened. `main.ts` copies the committed `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`.

## Verify

```sh
python3 draw.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
cmp entry.png out/entry.png
```
