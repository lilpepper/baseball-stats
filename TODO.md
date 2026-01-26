# Baseball Stats App - Prioritized TODO

## Bugs / Warnings to Fix
- [x] **LLM agent import error**: Update import from `langchain.agents.create_pandas_dataframe_agent` to `langchain_experimental.agents.create_pandas_dataframe_agent` ✅ Fixed
- [x] **FutureWarning in callbacks.py:125**: Wrap literal JSON string in `StringIO` when calling `pd.read_json()` ✅ Fixed

## Priority 1: Essential Setup
- [ ] **Install dependencies**: Run `pip install -e .` or `pip install -e ".[dev]"`
- [ ] **Download data**: Run `python scripts/download_data.py --start 2015 --end 2024`
- [ ] **Set API key**: Copy `.env.example` to `.env` and add your `ANTHROPIC_API_KEY`
- [ ] **Run the app**: Execute `python -m baseball_stats.app`

## Priority 2: Core Features to Complete
- [ ] **Add position filtering**: Currently position data needs to be mapped from pybaseball
- [x] **Implement player detail page**: Click on player in scatter plot to see full profile ✅ Player Card tab with click-to-navigate
- [x] **Add career totals view**: Aggregate stats across seasons for career comparison ✅ Career Totals tab
- [ ] **Implement data caching**: Add Redis or file-based cache for faster queries
- [ ] **Add dark mode toggle**: Theme switching for the dashboard

## Priority 3: Enhanced Visualizations
- [x] **Add radar/spider charts**: For multi-stat player comparisons ✅ Added to Compare and Career Totals
- [ ] **Implement heatmaps**: Correlation matrices between stats
- [ ] **Add histogram distributions**: See how stats are distributed across players
- [ ] **Create trend sparklines**: Small inline charts showing stat trends
- [x] **Add percentile rankings**: Show where a player ranks for each stat ✅ Player Card shows percentile bars

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

## Priority 6: Team & Season Analytics (New!)

Shift from individual players to team-level insights:

- [ ] **Team Season Dashboard**: Comprehensive single-team view showing W-L record, run differential, Pythagorean expected wins, team batting/pitching splits, and league rankings. Includes a "report card" grading offense, defense, rotation, and bullpen. *The foundation for all team analytics.*

- [ ] **Team WAR Allocation Map**: Visualize where a team's total WAR comes from—a treemap or stacked bar showing contribution by position (C, 1B, 2B...), role (starters vs. bench, rotation vs. bullpen), and individual players. Instantly reveals roster construction philosophy and where holes exist. *Answers "why did this team win/lose?"*

- [ ] **Cross-Era Team Comparison**: Compare any teams across history with era-adjusted stats. "2001 Mariners vs. 1998 Yankees vs. 1975 Reds"—normalize for run environments, show adjusted run differentials, and project head-to-head matchups. *Finally settle bar arguments with data.*

- [ ] **Franchise Timeline Explorer**: Interactive timeline of a franchise's entire history—season-by-season W-L, playoff appearances, championships, key player acquisitions/departures, and "dynasty" detection. Zoom from 100+ years to a single season. Click any year to drill into that team's roster. *Tells the story of a franchise through data.*

## Priority 7: Data Expansion
- [ ] **Add Statcast data**: Pitch-level metrics (exit velocity, launch angle, spin rate)
- [ ] **Include fielding stats**: UZR, DRS, OAA for defensive analysis
- [x] **Add team-level data**: Team standings, payroll, park factors *(Required for Priority 6)*
- [ ] **Include minor league data**: Prospect stats and development tracking
- [ ] **Add historical All-Star/MVP data**: Award voting and selections

## Priority 8: Performance & Polish
- [ ] **Implement lazy loading**: Load data on demand for large datasets
- [ ] **Add pagination**: Virtual scrolling for large tables
- [ ] **Optimize DuckDB queries**: Add indexes and query plans
- [ ] **Add loading skeletons**: Better UX during data fetches
- [ ] **Implement error boundaries**: Graceful error handling throughout

## Priority 9: Testing & Documentation
- [ ] **Add unit tests**: Test data ingestion, formula validation, callbacks
- [ ] **Add integration tests**: Test full app workflows
- [ ] **Create API documentation**: Document all modules and functions
- [ ] **Add user guide**: How to use each feature
- [ ] **Create demo video**: Showcase all features

## Priority 10: Deployment & DevOps
- [ ] **Create Dockerfile**: Containerize the application
- [ ] **Add docker-compose**: Full stack with Redis cache
- [ ] **Set up CI/CD**: Automated testing and deployment
- [ ] **Add health checks**: Monitoring endpoints
- [ ] **Configure logging**: Structured logging with log rotation

## Priority 11: Counter-Intuitive Insights

These features reveal hidden truths that contradict conventional baseball wisdom:

- [ ] **Era Time Machine**: Project how a player's stats would translate to a different era. "What would Babe Ruth hit in 2024?" or "How would Mike Trout fare in 1968?" Adjusts for run environment, pitching quality, and ballpark factors. *Counter-intuitive because we treat stats as absolute, but context changes everything.*

- [ ] **Career Trajectory Clustering**: Group players not by position or peak stats, but by the *shape* of their career arc—late bloomers, early peaks, steady performers, comeback stories, flash-in-the-pans. Find which pattern a current player is following. *Counter-intuitive because we obsess over peak performance while ignoring that career shapes predict future value.*

- [ ] **The "Replacement Reality" View**: For any player-season, show a side-by-side of what actually happened vs. what a freely-available replacement-level player would have contributed. Makes WAR tangible: "Without Mike Trout, the Angels would have scored 847 runs instead of 912." *Counter-intuitive because WAR is abstract; this makes the counterfactual concrete and emotionally resonant.*

- [ ] **Stat Contradiction Finder**: Automatically detect players whose stats defy conventional wisdom—high OBP but low runs scored (batting in wrong lineup spot?), high strikeouts but elite results (new swing philosophy?), great ERA but terrible FIP (lucky or good defense?). Surface the anomalies that suggest either hidden value or impending regression. *Counter-intuitive because we assume stats tell a coherent story, but contradictions reveal the real insights.*

## Priority 12: Quick Wins (New Suggestions)

Practical enhancements that build on existing functionality:

- [ ] **Season-over-Season Sparklines**: Add mini trend charts to the Player Card showing how each stat changed year-to-year. Green arrows for improvement, red for decline. Instantly see if a player is trending up or down without reading tables. *Builds on existing Player Card infrastructure.*

- [ ] **"Prime Years" Highlighter**: Automatically detect and highlight a player's peak performance window (typically ages 26-32). Show the stats from their prime vs. career average. Help users understand "peak Bonds" vs. "career Bonds". *Uses existing data, adds analytical insight.*

- [ ] **Head-to-Head Comparison Mode**: Enhanced Compare tab with side-by-side stat table showing who "wins" each category (highlighted in green). Add cumulative score like "Player A wins 7/10 categories". Makes comparisons more engaging and decisive. *Enhances existing Compare functionality.*

- [ ] **Era-Filtered Leaderboards**: Add decade filter to Explorer tab (1950s, 1960s, etc.) to see who dominated each era. "Top 10 HR hitters of the 1990s". Useful for historical context and settling debates. *Simple filter addition to existing leaderboard.*

## Priority 13: Future Features (Wishlist)
- [x] **Player similarity search**: "Find players similar to Mike Trout" ✅ Added to Player Card
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
