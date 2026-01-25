# Baseball Statistics Explorer

Interactive baseball statistics dashboard with sliders, dials, custom stat builder, and AI-powered natural language queries.

## Features

- **Interactive Visualizations**: Scatter plots, leaderboard tables, and gauges with real-time filtering
- **Sliders & Dials**: Year range sliders, stat threshold sliders, WAR gauges, and weight knobs
- **Custom Stats Engine**: Create your own statistics with weighted combinations or custom formulas
- **AI Assistant**: Ask questions in natural language (powered by Claude)
- **Player Comparison**: Side-by-side analysis of any two players
- **Historical Data**: Access to 100+ years of MLB batting and pitching statistics

## Quick Start

### 1. Install dependencies

```bash
pip install -e .
# Or with development tools:
pip install -e ".[dev]"
```

### 2. Download baseball data

```bash
# Recent years (faster, recommended for first run)
python scripts/download_data.py --start 2015 --end 2024

# Full historical data (slower)
python scripts/download_data.py --full
```

### 3. Set up environment (optional, for AI features)

```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 4. Run the app

```bash
python -m baseball_stats.app
```

Open http://127.0.0.1:8050 in your browser.

## Screenshots

The dashboard includes:
- **Explorer Tab**: Filter and visualize player statistics
- **Compare Tab**: Head-to-head player comparison
- **Custom Stats Tab**: Build novel statistics with knobs and formulas
- **AI Assistant Tab**: Chat with an AI about baseball data

## Project Structure

```
baseball-stats/
├── src/baseball_stats/
│   ├── app.py              # Main Dash application
│   ├── config.py           # Configuration management
│   ├── data/               # Data ingestion and storage
│   ├── stats/              # Custom statistics engine
│   ├── llm/                # LLM integration
│   └── dashboard/          # UI components and callbacks
├── scripts/
│   └── download_data.py    # Data download script
├── data/                   # Data files (gitignored)
└── tests/                  # Test suite
```

## Technology Stack

- **Frontend**: Dash + Dash Bootstrap Components + Dash DAQ
- **Database**: DuckDB + Parquet
- **Data Source**: pybaseball (FanGraphs, Baseball-Reference)
- **LLM**: Claude API via LangChain
- **Visualization**: Plotly

## Custom Stats Examples

**Quick Mode** - Adjust knobs for weighted combinations:
- OBP weight: 1.8x, SLG weight: 1.0x → Custom OPS

**Advanced Mode** - Write formulas:
```
(obp * 1.8) + slg                    # Custom OPS
(hr * 2) + sb                        # Power-Speed
bb_pct - k_pct                       # Plate Discipline
war / pa * 600                       # WAR per 600 PA
```

## AI Assistant Examples

Ask questions like:
- "Who had the highest WAR in 2023?"
- "Compare Mike Trout and Mookie Betts"
- "Find players with 40+ HR and 20+ SB"
- "Explain what wRC+ means"

## License

MIT
