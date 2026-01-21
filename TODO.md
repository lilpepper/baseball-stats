# Baseball Stats App - Prioritized TODO

## Bugs / Warnings to Fix
- [ ] **LLM agent import error**: Update import from `langchain.agents.create_pandas_dataframe_agent` to `langchain_experimental.agents.create_pandas_dataframe_agent`
- [ ] **FutureWarning in callbacks.py:125**: Wrap literal JSON string in `StringIO` when calling `pd.read_json()`

## Priority 1: Essential Setup
- [ ] **Install dependencies**: Run `pip install -e .` or `pip install -e ".[dev]"`
- [ ] **Download data**: Run `python scripts/download_data.py --start 2015 --end 2024`
- [ ] **Set API key**: Copy `.env.example` to `.env` and add your `ANTHROPIC_API_KEY`
- [ ] **Run the app**: Execute `python -m baseball_stats.app`

## Priority 2: Core Features to Complete
- [ ] **Add position filtering**: Currently position data needs to be mapped from pybaseball
- [ ] **Implement player detail page**: Click on player in scatter plot to see full profile
- [ ] **Add career totals view**: Aggregate stats across seasons for career comparison
- [ ] **Implement data caching**: Add Redis or file-based cache for faster queries
- [ ] **Add dark mode toggle**: Theme switching for the dashboard

## Priority 3: Enhanced Visualizations
- [ ] **Add radar/spider charts**: For multi-stat player comparisons
- [ ] **Implement heatmaps**: Correlation matrices between stats
- [ ] **Add histogram distributions**: See how stats are distributed across players
- [ ] **Create trend sparklines**: Small inline charts showing stat trends
- [ ] **Add percentile rankings**: Show where a player ranks for each stat

## Priority 4: Advanced Custom Stats
- [ ] **Save formulas to database**: Persist user formulas across sessions
- [ ] **Add formula sharing**: Export/import custom formulas
- [ ] **Implement rolling averages**: Create formulas with window functions
- [ ] **Add z-score normalization**: Option for standardized stat combinations
- [ ] **Create formula templates**: Pre-built templates for common use cases

## Priority 5: LLM Enhancements
- [ ] **Add conversation memory**: Remember context across multiple questions
- [ ] **Implement query caching**: Cache LLM responses for repeated questions
- [ ] **Add source citations**: Show which data rows support the answer
- [ ] **Create visualization suggestions**: LLM suggests charts based on questions
- [ ] **Add natural language formula creation**: "Create a stat that values power and speed equally"

## Priority 6: Data Expansion
- [ ] **Add Statcast data**: Pitch-level metrics (exit velocity, launch angle, spin rate)
- [ ] **Include fielding stats**: UZR, DRS, OAA for defensive analysis
- [ ] **Add team-level data**: Team standings, payroll, park factors
- [ ] **Include minor league data**: Prospect stats and development tracking
- [ ] **Add historical All-Star/MVP data**: Award voting and selections

## Priority 7: Performance & Polish
- [ ] **Implement lazy loading**: Load data on demand for large datasets
- [ ] **Add pagination**: Virtual scrolling for large tables
- [ ] **Optimize DuckDB queries**: Add indexes and query plans
- [ ] **Add loading skeletons**: Better UX during data fetches
- [ ] **Implement error boundaries**: Graceful error handling throughout

## Priority 8: Testing & Documentation
- [ ] **Add unit tests**: Test data ingestion, formula validation, callbacks
- [ ] **Add integration tests**: Test full app workflows
- [ ] **Create API documentation**: Document all modules and functions
- [ ] **Add user guide**: How to use each feature
- [ ] **Create demo video**: Showcase all features

## Priority 9: Deployment & DevOps
- [ ] **Create Dockerfile**: Containerize the application
- [ ] **Add docker-compose**: Full stack with Redis cache
- [ ] **Set up CI/CD**: Automated testing and deployment
- [ ] **Add health checks**: Monitoring endpoints
- [ ] **Configure logging**: Structured logging with log rotation

## Priority 10: Future Features (Wishlist)
- [ ] **Player similarity search**: "Find players similar to Mike Trout"
- [ ] **Projection system**: Simple projection model for future performance
- [ ] **Trade analyzer**: Compare packages of players
- [ ] **Draft board**: Rank players by custom criteria
- [ ] **Fantasy integration**: Fantasy points calculations
- [ ] **Mobile responsive**: Optimize for tablet/phone
- [ ] **Export to CSV/Excel**: Download filtered data
- [ ] **Shareable URLs**: Deep links to specific views
- [ ] **User accounts**: Save preferences and formulas per user
- [ ] **Real-time updates**: WebSocket for live game data during season

---

## Quick Start Commands

```bash
# Install
pip install -e ".[dev]"

# Download data (recent years, faster)
python scripts/download_data.py --start 2015 --end 2024

# Download full historical data (slower, ~100k+ records)
python scripts/download_data.py --full

# Run the app
python -m baseball_stats.app

# Run tests
pytest tests/

# Type check
mypy src/

# Lint
ruff check src/
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | API key for Claude LLM | (required for AI chat) |
| `DATA_DIR` | Directory for data files | `./data` |
| `DATABASE_PATH` | DuckDB database path | `./data/baseball.duckdb` |
| `DEBUG` | Enable debug mode | `false` |
| `HOST` | Server host | `127.0.0.1` |
| `PORT` | Server port | `8050` |
