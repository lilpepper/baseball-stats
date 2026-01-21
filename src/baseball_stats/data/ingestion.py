"""Data ingestion module using pybaseball library."""

import logging
from dataclasses import dataclass
from typing import Optional

import pandas as pd
from pybaseball import batting_stats, pitching_stats, cache
from pybaseball.lahman import download_lahman, batting, pitching, people

logger = logging.getLogger(__name__)


@dataclass
class DataIngestionConfig:
    """Configuration for data ingestion."""

    start_year: int = 1900
    end_year: int = 2024
    cache_enabled: bool = True
    qual: int = 50  # Minimum plate appearances (batting) or innings (pitching)


class BaseballDataIngester:
    """Handles all data fetching from pybaseball sources."""

    def __init__(self, config: Optional[DataIngestionConfig] = None):
        self.config = config or DataIngestionConfig()
        if self.config.cache_enabled:
            cache.enable()

    def fetch_batting_stats(
        self, start: Optional[int] = None, end: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Fetch season-level batting statistics including WAR.

        Returns DataFrame with 300+ columns including:
        - WAR, wRC+, OBP, SLG, OPS, wOBA
        - HR, RBI, R, SB, BB, K
        - ISO, BABIP, BB%, K%
        """
        start = start or self.config.start_year
        end = end or self.config.end_year

        logger.info(f"Fetching batting stats from {start} to {end}...")

        # FanGraphs batting stats include WAR and advanced metrics
        df = batting_stats(start, end, qual=self.config.qual)

        # Standardize column names
        df = self._standardize_batting_columns(df)

        logger.info(f"Fetched {len(df)} batting records")
        return df

    def fetch_pitching_stats(
        self, start: Optional[int] = None, end: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Fetch season-level pitching statistics including WAR.

        Returns DataFrame with columns including:
        - WAR, ERA, WHIP, FIP, xFIP
        - W, L, SV, IP, K, BB
        - K/9, BB/9, HR/9
        """
        start = start or self.config.start_year
        end = end or self.config.end_year

        logger.info(f"Fetching pitching stats from {start} to {end}...")

        # FanGraphs pitching stats include WAR and advanced metrics
        df = pitching_stats(start, end, qual=self.config.qual)

        # Standardize column names
        df = self._standardize_pitching_columns(df)

        logger.info(f"Fetched {len(df)} pitching records")
        return df

    def fetch_lahman_data(self) -> dict[str, pd.DataFrame]:
        """
        Fetch complete Lahman database for historical coverage.

        Returns dict with keys: 'batting', 'pitching', 'people', etc.
        """
        logger.info("Downloading Lahman database...")

        # Download if not cached
        download_lahman()

        data = {
            "batting": batting(),
            "pitching": pitching(),
            "people": people(),
        }

        logger.info(
            f"Fetched Lahman data: {len(data['batting'])} batting, "
            f"{len(data['pitching'])} pitching, {len(data['people'])} players"
        )
        return data

    def fetch_player_info(self) -> pd.DataFrame:
        """Fetch player biographical information."""
        logger.info("Fetching player info...")
        df = people()
        return df

    def run_full_ingestion(self) -> dict[str, pd.DataFrame]:
        """
        Execute complete data ingestion pipeline.

        Returns dict with all fetched DataFrames.
        """
        logger.info("Starting full data ingestion...")

        result = {
            "batting": self.fetch_batting_stats(),
            "pitching": self.fetch_pitching_stats(),
        }

        # Try to get Lahman for historical coverage
        try:
            lahman = self.fetch_lahman_data()
            result["players"] = lahman["people"]
        except Exception as e:
            logger.warning(f"Could not fetch Lahman data: {e}")

        logger.info("Full ingestion complete")
        return result

    def _standardize_batting_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize batting column names for consistency."""
        # Map common column variations
        column_map = {
            "Name": "name",
            "Team": "team",
            "Season": "season",
            "G": "games",
            "PA": "pa",
            "AB": "ab",
            "H": "hits",
            "HR": "hr",
            "RBI": "rbi",
            "R": "runs",
            "SB": "sb",
            "BB": "bb",
            "SO": "k",
            "AVG": "avg",
            "OBP": "obp",
            "SLG": "slg",
            "OPS": "ops",
            "WAR": "war",
            "wRC+": "wrc_plus",
            "wOBA": "woba",
            "ISO": "iso",
            "BABIP": "babip",
            "BB%": "bb_pct",
            "K%": "k_pct",
        }

        # Only rename columns that exist
        existing_renames = {k: v for k, v in column_map.items() if k in df.columns}
        df = df.rename(columns=existing_renames)

        return df

    def _standardize_pitching_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize pitching column names for consistency."""
        column_map = {
            "Name": "name",
            "Team": "team",
            "Season": "season",
            "W": "wins",
            "L": "losses",
            "ERA": "era",
            "WHIP": "whip",
            "G": "games",
            "GS": "games_started",
            "IP": "ip",
            "SO": "k",
            "BB": "bb",
            "HR": "hr",
            "WAR": "war",
            "FIP": "fip",
            "xFIP": "xfip",
            "K/9": "k_per_9",
            "BB/9": "bb_per_9",
            "HR/9": "hr_per_9",
            "K%": "k_pct",
            "BB%": "bb_pct",
            "SV": "saves",
        }

        existing_renames = {k: v for k, v in column_map.items() if k in df.columns}
        df = df.rename(columns=existing_renames)

        return df
