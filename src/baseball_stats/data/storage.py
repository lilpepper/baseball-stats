"""Storage layer using DuckDB and Parquet files."""

import logging
from pathlib import Path
from typing import Optional

import duckdb
import pandas as pd

logger = logging.getLogger(__name__)


class BaseballDatabase:
    """DuckDB-based storage for baseball statistics."""

    def __init__(self, db_path: Path, data_dir: Path):
        """
        Initialize the database connection.

        Args:
            db_path: Path to DuckDB database file
            data_dir: Directory containing Parquet files
        """
        self.db_path = Path(db_path)
        self.data_dir = Path(data_dir)
        self.conn = duckdb.connect(str(db_path))
        self._setup_database()

    def _setup_database(self):
        """Set up database tables and views."""
        # Create user formulas table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS custom_formulas (
                id INTEGER PRIMARY KEY,
                name VARCHAR UNIQUE NOT NULL,
                expression VARCHAR NOT NULL,
                description VARCHAR,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Register Parquet files as views if they exist
        self._register_parquet_views()

    def _register_parquet_views(self):
        """Register Parquet files as queryable views."""
        parquet_files = {
            "batting": self.data_dir / "batting.parquet",
            "pitching": self.data_dir / "pitching.parquet",
            "players": self.data_dir / "players.parquet",
        }

        for name, path in parquet_files.items():
            if path.exists():
                logger.info(f"Registering {name} view from {path}")
                self.conn.execute(f"""
                    CREATE OR REPLACE VIEW {name} AS
                    SELECT * FROM read_parquet('{path}')
                """)

    def save_dataframe(self, df: pd.DataFrame, name: str):
        """
        Save DataFrame as Parquet file.

        Args:
            df: DataFrame to save
            name: Name for the Parquet file (without extension)
        """
        path = self.data_dir / f"{name}.parquet"
        path.parent.mkdir(parents=True, exist_ok=True)

        df.to_parquet(path, index=False)
        logger.info(f"Saved {len(df)} records to {path}")

        # Re-register the view
        self.conn.execute(f"""
            CREATE OR REPLACE VIEW {name} AS
            SELECT * FROM read_parquet('{path}')
        """)

    def query(self, sql: str) -> pd.DataFrame:
        """
        Execute SQL query and return DataFrame.

        Args:
            sql: SQL query string

        Returns:
            Query results as DataFrame
        """
        return self.conn.execute(sql).fetchdf()

    def get_batting_stats(
        self,
        player_names: Optional[list[str]] = None,
        teams: Optional[list[str]] = None,
        years: Optional[tuple[int, int]] = None,
        min_pa: int = 0,
    ) -> pd.DataFrame:
        """
        Retrieve batting statistics with filters.

        Args:
            player_names: Filter by player names
            teams: Filter by team abbreviations
            years: Filter by year range (start, end)
            min_pa: Minimum plate appearances

        Returns:
            Filtered batting statistics DataFrame
        """
        conditions = ["1=1"]
        params = []

        if player_names:
            placeholders = ", ".join(["?" for _ in player_names])
            conditions.append(f"name IN ({placeholders})")
            params.extend(player_names)

        if teams:
            placeholders = ", ".join(["?" for _ in teams])
            conditions.append(f"team IN ({placeholders})")
            params.extend(teams)

        if years:
            conditions.append("season >= ? AND season <= ?")
            params.extend(years)

        if min_pa > 0:
            conditions.append("pa >= ?")
            params.append(min_pa)

        where_clause = " AND ".join(conditions)
        sql = f"SELECT * FROM batting WHERE {where_clause} ORDER BY season DESC, war DESC"

        return self.conn.execute(sql, params).fetchdf()

    def get_pitching_stats(
        self,
        player_names: Optional[list[str]] = None,
        teams: Optional[list[str]] = None,
        years: Optional[tuple[int, int]] = None,
        min_ip: float = 0,
    ) -> pd.DataFrame:
        """
        Retrieve pitching statistics with filters.

        Args:
            player_names: Filter by player names
            teams: Filter by team abbreviations
            years: Filter by year range (start, end)
            min_ip: Minimum innings pitched

        Returns:
            Filtered pitching statistics DataFrame
        """
        conditions = ["1=1"]
        params = []

        if player_names:
            placeholders = ", ".join(["?" for _ in player_names])
            conditions.append(f"name IN ({placeholders})")
            params.extend(player_names)

        if teams:
            placeholders = ", ".join(["?" for _ in teams])
            conditions.append(f"team IN ({placeholders})")
            params.extend(teams)

        if years:
            conditions.append("season >= ? AND season <= ?")
            params.extend(years)

        if min_ip > 0:
            conditions.append("ip >= ?")
            params.append(min_ip)

        where_clause = " AND ".join(conditions)
        sql = f"SELECT * FROM pitching WHERE {where_clause} ORDER BY season DESC, war DESC"

        return self.conn.execute(sql, params).fetchdf()

    def get_available_columns(self, table: str = "batting") -> list[str]:
        """Get list of available columns in a table."""
        try:
            df = self.conn.execute(f"SELECT * FROM {table} LIMIT 1").fetchdf()
            return list(df.columns)
        except Exception:
            return []

    def get_unique_teams(self, table: str = "batting") -> list[str]:
        """Get list of unique team abbreviations."""
        try:
            df = self.conn.execute(
                f"SELECT DISTINCT team FROM {table} ORDER BY team"
            ).fetchdf()
            return df["team"].tolist()
        except Exception:
            return []

    def get_year_range(self, table: str = "batting") -> tuple[int, int]:
        """Get the range of years available in the data."""
        try:
            result = self.conn.execute(
                f"SELECT MIN(season), MAX(season) FROM {table}"
            ).fetchone()
            return (result[0], result[1])
        except Exception:
            return (1900, 2024)

    def get_war_leaders(
        self,
        year: int,
        stat_type: str = "batting",
        limit: int = 10,
    ) -> pd.DataFrame:
        """Get WAR leaders for a specific year."""
        table = stat_type
        return self.query(f"""
            SELECT name, team, war, season
            FROM {table}
            WHERE season = {year}
            ORDER BY war DESC
            LIMIT {limit}
        """)

    def search_players(self, search_term: str, table: str = "batting") -> list[str]:
        """Search for player names matching a term."""
        try:
            df = self.conn.execute(f"""
                SELECT DISTINCT name
                FROM {table}
                WHERE LOWER(name) LIKE LOWER('%{search_term}%')
                ORDER BY name
                LIMIT 50
            """).fetchdf()
            return df["name"].tolist()
        except Exception:
            return []

    def save_custom_formula(self, name: str, expression: str, description: str = ""):
        """Save a custom formula to the database."""
        self.conn.execute("""
            INSERT OR REPLACE INTO custom_formulas (name, expression, description)
            VALUES (?, ?, ?)
        """, [name, expression, description])

    def get_custom_formulas(self) -> pd.DataFrame:
        """Get all saved custom formulas."""
        return self.query("SELECT * FROM custom_formulas ORDER BY name")

    def close(self):
        """Close the database connection."""
        self.conn.close()
