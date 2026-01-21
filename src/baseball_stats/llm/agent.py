"""LangChain agent for natural language baseball queries."""

import logging
from typing import Optional

import pandas as pd
from langchain.agents import AgentType, create_pandas_dataframe_agent
from langchain_anthropic import ChatAnthropic

logger = logging.getLogger(__name__)


class BaseballLLMAgent:
    """LLM agent for natural language interaction with baseball data."""

    BATTING_PREFIX = """You are a baseball statistics expert assistant.
You have access to a DataFrame containing batting statistics for MLB players.

Key columns include:
- name: Player name
- team: Team abbreviation
- season: Year
- war: Wins Above Replacement (the best overall measure of player value)
- avg: Batting average
- obp: On-base percentage
- slg: Slugging percentage
- ops: On-base plus slugging
- wrc_plus: Weighted Runs Created Plus (100 = league average, higher is better)
- hr: Home runs
- rbi: Runs batted in
- runs: Runs scored
- sb: Stolen bases
- bb: Walks
- k: Strikeouts
- iso: Isolated power (SLG - AVG)
- babip: Batting average on balls in play

When answering questions:
1. Use WAR as the primary measure of overall player value
2. If the user doesn't specify a time period, use the most recent data available
3. Explain any advanced metrics in simple terms
4. Provide context when relevant (league averages, historical comparisons)
5. Be concise but informative
"""

    PITCHING_PREFIX = """You are a baseball statistics expert assistant.
You have access to a DataFrame containing pitching statistics for MLB players.

Key columns include:
- name: Player name
- team: Team abbreviation
- season: Year
- war: Wins Above Replacement
- era: Earned Run Average (lower is better)
- whip: Walks + Hits per Inning Pitched (lower is better)
- fip: Fielding Independent Pitching (ERA estimator based on K, BB, HR)
- xfip: Expected FIP (normalizes HR rate)
- wins: Wins
- losses: Losses
- saves: Saves
- ip: Innings pitched
- k: Strikeouts
- bb: Walks
- k_per_9: Strikeouts per 9 innings
- bb_per_9: Walks per 9 innings

When answering questions:
1. Use WAR as the primary measure of overall pitcher value
2. Distinguish between ERA (results-based) and FIP (skill-based) when discussing pitcher quality
3. Consider workload (IP) when comparing pitchers
4. Be concise but informative
"""

    def __init__(
        self,
        api_key: str,
        batting_df: pd.DataFrame,
        pitching_df: pd.DataFrame,
        model: str = "claude-sonnet-4-20250514",
    ):
        """
        Initialize the baseball LLM agent.

        Args:
            api_key: Anthropic API key
            batting_df: DataFrame with batting statistics
            pitching_df: DataFrame with pitching statistics
            model: Claude model to use
        """
        self.llm = ChatAnthropic(
            api_key=api_key,
            model=model,
            temperature=0,
            max_tokens=1024,
        )
        self.batting_df = batting_df
        self.pitching_df = pitching_df

        # Create agents for batting and pitching
        self.batting_agent = self._create_agent(batting_df, self.BATTING_PREFIX)
        self.pitching_agent = self._create_agent(pitching_df, self.PITCHING_PREFIX)

        logger.info(
            f"LLM agent initialized with {len(batting_df)} batting records "
            f"and {len(pitching_df)} pitching records"
        )

    def _create_agent(self, df: pd.DataFrame, prefix: str):
        """Create a pandas DataFrame agent."""
        return create_pandas_dataframe_agent(
            self.llm,
            df,
            agent_type=AgentType.OPENAI_FUNCTIONS,  # Works with Claude too
            prefix=prefix,
            verbose=False,
            allow_dangerous_code=True,  # Required for DataFrame operations
            max_iterations=5,
        )

    def query(self, question: str, stat_type: str = "batting") -> str:
        """
        Execute a natural language query against the data.

        Args:
            question: Natural language question about baseball statistics
            stat_type: 'batting' or 'pitching'

        Returns:
            String response from the LLM
        """
        agent = self.batting_agent if stat_type == "batting" else self.pitching_agent

        try:
            response = agent.invoke({"input": question})
            return response.get("output", "I couldn't find an answer to that question.")
        except Exception as e:
            logger.error(f"Error in LLM query: {e}")
            return f"I encountered an error processing your question: {str(e)}"

    def get_war_leaders(self, year: int, stat_type: str = "batting", limit: int = 10) -> str:
        """Get WAR leaders for a specific year."""
        question = f"Who were the top {limit} players by WAR in {year}? List their names, teams, and WAR values."
        return self.query(question, stat_type)

    def compare_players(
        self,
        player1: str,
        player2: str,
        stats: Optional[list[str]] = None,
    ) -> str:
        """Compare two players."""
        stats_str = ", ".join(stats) if stats else "WAR, batting average, OBP, SLG, and home runs"
        question = f"Compare {player1} and {player2} across their careers. Focus on {stats_str}. Which player has been more valuable overall?"
        return self.query(question, "batting")

    def explain_stat(self, stat_name: str) -> str:
        """Explain what a statistic means."""
        question = f"Explain what {stat_name} means in baseball, how it's calculated, and what values are considered good/average/poor."
        return self.query(question, "batting")
