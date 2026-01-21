#!/usr/bin/env python3
"""
Download baseball data and save to Parquet files.

Usage:
    python scripts/download_data.py [--start YEAR] [--end YEAR] [--qual MIN_PA]

Example:
    python scripts/download_data.py --start 2000 --end 2024 --qual 100
"""

import argparse
import logging
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from baseball_stats.config import config
from baseball_stats.data.ingestion import BaseballDataIngester, DataIngestionConfig
from baseball_stats.data.storage import BaseballDatabase

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Download baseball statistics data")
    parser.add_argument(
        "--start",
        type=int,
        default=2000,
        help="Start year (default: 2000)",
    )
    parser.add_argument(
        "--end",
        type=int,
        default=2024,
        help="End year (default: 2024)",
    )
    parser.add_argument(
        "--qual",
        type=int,
        default=50,
        help="Minimum plate appearances / innings (default: 50)",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Download full historical data from 1900",
    )
    args = parser.parse_args()

    # Use full range if requested
    start_year = 1900 if args.full else args.start
    end_year = args.end

    logger.info(f"Downloading data from {start_year} to {end_year}")
    logger.info(f"Minimum PA/IP qualification: {args.qual}")

    # Ensure data directories exist
    config.ensure_dirs()

    # Create ingester
    ingestion_config = DataIngestionConfig(
        start_year=start_year,
        end_year=end_year,
        qual=args.qual,
        cache_enabled=True,
    )
    ingester = BaseballDataIngester(ingestion_config)

    # Create database
    db = BaseballDatabase(config.database_path, config.processed_data_dir)

    try:
        # Fetch and save batting stats
        logger.info("Fetching batting statistics...")
        batting_df = ingester.fetch_batting_stats()
        db.save_dataframe(batting_df, "batting")
        logger.info(f"Saved {len(batting_df)} batting records")

        # Fetch and save pitching stats
        logger.info("Fetching pitching statistics...")
        pitching_df = ingester.fetch_pitching_stats()
        db.save_dataframe(pitching_df, "pitching")
        logger.info(f"Saved {len(pitching_df)} pitching records")

        # Fetch player info
        logger.info("Fetching player information...")
        try:
            players_df = ingester.fetch_player_info()
            db.save_dataframe(players_df, "players")
            logger.info(f"Saved {len(players_df)} player records")
        except Exception as e:
            logger.warning(f"Could not fetch player info: {e}")

        logger.info("Data download complete!")
        logger.info(f"Data saved to: {config.processed_data_dir}")
        logger.info(f"Database: {config.database_path}")

        # Print summary
        print("\n" + "=" * 50)
        print("DOWNLOAD SUMMARY")
        print("=" * 50)
        print(f"Batting records:  {len(batting_df):,}")
        print(f"Pitching records: {len(pitching_df):,}")
        print(f"Year range:       {start_year} - {end_year}")
        print(f"Data directory:   {config.processed_data_dir}")
        print("=" * 50)

    except Exception as e:
        logger.error(f"Error during download: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
