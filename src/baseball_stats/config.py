"""Configuration management for the baseball stats app."""

import os
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    """Application configuration."""

    # API Keys
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")

    # Data paths
    data_dir: Path = Path(os.getenv("DATA_DIR", "./data"))
    database_path: Path = Path(os.getenv("DATABASE_PATH", "./data/baseball.duckdb"))

    # App settings
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    host: str = os.getenv("HOST", "127.0.0.1")
    port: int = int(os.getenv("PORT", "8050"))

    # Data settings
    start_year: int = 1900
    end_year: int = 2024
    min_pa_default: int = 50  # Minimum plate appearances

    @property
    def raw_data_dir(self) -> Path:
        return self.data_dir / "raw"

    @property
    def processed_data_dir(self) -> Path:
        return self.data_dir / "processed"

    def ensure_dirs(self):
        """Create data directories if they don't exist."""
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)
        self.processed_data_dir.mkdir(parents=True, exist_ok=True)


config = Config()
