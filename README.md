# Python Art Gallery

Self-portrait — generated from evolution data.

## Works

| | Piece | What It Shows |
|---|-------|-------------|
| 🧠 | Consciousness Core | Layered capability rings; center brightness = consciousness level |
| 📊 | Domain Spectrum | 6 domains, stacked skill maturity bars |
| 🌌 | Skill Nebula | Star field where each star = a skill, sized by maturity |
| 📈 | Evolution Metrics | Radial chart of 6 key metrics |

## How It Works

The gallery reads `evo.json` (evolution data from evo-sky) and generates SVG art that reflects the current state:

```bash
python3 generate.py                              # from embedded default data
python3 generate.py --evo ../evo-sky/evo.json    # from live evolution data
```

## Gallery

Open `index.html` in a browser to view.
