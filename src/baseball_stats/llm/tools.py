"""Custom LangChain tools for baseball-specific operations."""

from typing import Optional

from langchain.tools import tool


STAT_EXPLANATIONS = {
    "war": """**WAR (Wins Above Replacement)**
WAR measures a player's total value compared to a replacement-level player (a freely available minor leaguer or AAAA player).

**How it's calculated:**
WAR combines batting runs, baserunning runs, fielding runs, and positional adjustment, then compares to replacement level.

**Interpretation:**
- 0-1: Replacement level
- 1-2: Bench player
- 2-3: Solid starter
- 3-5: Good player
- 5-7: All-Star
- 7+: MVP caliber

**Example:** A player with 6 WAR contributed approximately 6 more wins than a replacement player would have.""",

    "wrc_plus": """**wRC+ (Weighted Runs Created Plus)**
wRC+ measures offensive value adjusted for park and league, scaled to 100.

**How it's calculated:**
Based on wRC (Weighted Runs Created) but adjusted for ballpark and league, then scaled.

**Interpretation:**
- 100: League average
- 120: 20% better than average
- 80: 20% worse than average
- 150+: Elite offense
- <70: Very poor offense

**Example:** A player with 125 wRC+ created 25% more runs than a league-average hitter.""",

    "fip": """**FIP (Fielding Independent Pitching)**
FIP measures pitcher performance based only on outcomes the pitcher directly controls: strikeouts, walks, HBP, and home runs.

**How it's calculated:**
FIP = ((13*HR) + (3*(BB+HBP)) - (2*K)) / IP + constant

**Interpretation:**
- Uses ERA scale (lower is better)
- 3.00: Excellent
- 3.50: Good
- 4.00: Average
- 4.50: Below average
- 5.00+: Poor

**Why use it:**
FIP removes defense and luck, showing true pitching skill better than ERA.""",

    "ops": """**OPS (On-base Plus Slugging)**
OPS is a simple measure of offensive production: OBP + SLG.

**How it's calculated:**
OPS = On-Base Percentage + Slugging Percentage

**Interpretation:**
- .900+: Elite
- .800-.900: Very good
- .700-.800: Average
- .600-.700: Below average
- <.600: Poor

**Limitation:** OPS weights OBP and SLG equally, but OBP is actually more valuable.""",

    "babip": """**BABIP (Batting Average on Balls In Play)**
BABIP measures how often batted balls (excluding HR) fall for hits.

**How it's calculated:**
BABIP = (H - HR) / (AB - K - HR + SF)

**Interpretation:**
- League average: ~.300
- Higher than .300: May indicate luck or skill
- Lower than .300: May indicate bad luck or poor contact

**Uses:**
- Identify players who may regress
- Evaluate true hitting skill
- Understand ERA fluctuations for pitchers"""
}


@tool
def explain_stat(stat_name: str) -> str:
    """
    Explain what a baseball statistic means and how to interpret it.

    Args:
        stat_name: The name of the statistic to explain (e.g., 'WAR', 'wRC+', 'FIP')

    Returns:
        Detailed explanation of the statistic
    """
    stat_lower = stat_name.lower().replace(" ", "_").replace("+", "_plus")

    if stat_lower in STAT_EXPLANATIONS:
        return STAT_EXPLANATIONS[stat_lower]

    return f"I don't have a detailed explanation for '{stat_name}'. Common stats I can explain include: WAR, wRC+, FIP, OPS, BABIP."


@tool
def get_league_average(stat_name: str, year: Optional[int] = None) -> str:
    """
    Get the league average for a statistic.

    Args:
        stat_name: The statistic name
        year: Optional year (defaults to recent average)

    Returns:
        League average value and context
    """
    # Approximate league averages (these are typical modern values)
    averages = {
        "avg": ".250",
        "obp": ".320",
        "slg": ".400",
        "ops": ".720",
        "war": "2.0 (per full season for starters)",
        "wrc_plus": "100 (by definition)",
        "era": "4.00",
        "whip": "1.30",
        "fip": "4.00",
        "k_pct": "23%",
        "bb_pct": "8.5%",
        "hr": "20-25 (per full season)",
    }

    stat_lower = stat_name.lower()
    if stat_lower in averages:
        return f"League average {stat_name.upper()}: {averages[stat_lower]}"

    return f"I don't have league average data for '{stat_name}'."


@tool
def classify_player_value(war: float) -> str:
    """
    Classify a player's value based on their WAR.

    Args:
        war: The player's WAR value

    Returns:
        Classification of player value
    """
    if war >= 8:
        return "MVP caliber - among the best players in baseball"
    elif war >= 6:
        return "All-Star level - elite player"
    elif war >= 4:
        return "Very good player - solid starter with above-average value"
    elif war >= 2:
        return "Starter quality - average regular"
    elif war >= 1:
        return "Bench player - useful depth piece"
    elif war >= 0:
        return "Replacement level - minimal value above freely available players"
    else:
        return "Below replacement - actively hurting the team compared to alternatives"
