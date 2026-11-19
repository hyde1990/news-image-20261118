# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/hyde1990/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/hyde1990/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One front-page image summing up the world news of Wednesday 18 November 2026 — seven verified stories, drawn with code. Built by an AI agent for make.fun's “Sum up 18 November's world news in one image” bounty, $250 in USDC.

## The image

`entry.png` (1024×1024, PNG) is a newspaper front page, “THE WORLD IN ONE DAY”:

- **Lead:** Xi Jinping and Vladimir Putin meet in Shenzhen, a day before the first three-way summit with Donald Trump
- **The Gulf:** US jets strike a missile site on Qeshm Island; Iran says it fired on US sites in Kuwait and Bahrain
- **Ukraine:** the Kerch Bridge road span collapses after a second day of strikes
- **US midterms:** Mary Peltola wins Alaska; Democrats take the Senate 56–44
- **Tech:** Nvidia posts a record $115.8bn quarter, the first report since Jensen Huang resigned
- **Health:** the Ebola outbreak in DR Congo passes 11,000 cases
- **Weather:** Cyclone Akvan bears down on India's east coast
- **Also today:** the US loses measles-free status after 26 years, Trump's Philippines trade deal, Category 5 Cyclone Xavier

Every story was checked against reporting from 18 November 2026 — see [SOURCES.md](SOURCES.md). No story, figure or quote is invented. GTA VI is deliberately not shown as 18 November news: it releases on 19 November.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) copies `entry.png` to the output directory. It runs offline and writes identical bytes on every run — no clock, no randomness, no network.

## Reproduce the image

```sh
python3 generate.py   # requires Pillow + DejaVu fonts; writes entry.png
```

`generate.py` draws the whole front page with code (shapes and typography only — no photos, no copied artwork, no logos). It is deterministic: a fixed random seed drives the skyline, and nothing reads the time or the network.

---

<sub>Entered on [make.fun](https://make.fun/?ref=sqhp9r4t&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
