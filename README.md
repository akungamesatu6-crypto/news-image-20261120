# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/akungamesatu6-crypto/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/akungamesatu6-crypto/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image summing up the world's news of Friday 20 November 2026: the World Court rules Myanmar committed genocide against the Rohingya; Trump, Xi and Putin meet in Shenzhen and sign a joint peace declaration; Russian strikes kill 8 in Kyiv; a Houthi missile hits Riyadh's finance tower; markets slide while Anthropic's IPO pops 17%; and Kenya declares Ebola over.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (Python 3.13, standard library only) copies `entry.png` beside it to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png`). Deterministic: the same bytes out on every run. No network, no dependencies.

## How the image was built

`entry.png` (1024×1024 JPEG, 268 KiB) is a front page composed by `compose.py` from four AI-illustrated panels in `panels/` (no text in the artwork; all headlines and captions are drawn crisply by the script) plus a markets band and a footer line. The news was researched on 21 November 2026 from the day's wire reporting (`NEWS.md`).

---

<sub>Entered on [make.fun](https://make.fun/?ref=w6dq43eh&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
