"""Main Dash application entry point."""

import logging
from pathlib import Path

import dash
import dash_bootstrap_components as dbc
from dash import html

from .config import config
from .data.storage import BaseballDatabase
from .dashboard.layout import create_layout
from .dashboard.callbacks import register_callbacks

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_app() -> dash.Dash:
    """
    Create and configure the Dash application.

    Returns:
        Configured Dash app instance
    """
    # Initialize Dash app with Bootstrap theme
    app = dash.Dash(
        __name__,
        external_stylesheets=[
            dbc.themes.BOOTSTRAP,
            dbc.icons.FONT_AWESOME,
        ],
        title="Baseball Statistics Explorer",
        suppress_callback_exceptions=True,
    )

    # Set layout
    app.layout = create_layout()

    # Initialize database
    config.ensure_dirs()
    db = BaseballDatabase(config.database_path, config.processed_data_dir)

    # Initialize LLM agent if API key is available
    llm_agent = None
    if config.anthropic_api_key:
        try:
            from .llm.agent import BaseballLLMAgent

            # Load data for LLM agent
            batting_df = db.get_batting_stats()
            pitching_df = db.get_pitching_stats()

            if len(batting_df) > 0:
                llm_agent = BaseballLLMAgent(
                    api_key=config.anthropic_api_key,
                    batting_df=batting_df,
                    pitching_df=pitching_df,
                )
                logger.info("LLM agent initialized successfully")
            else:
                logger.warning("No data available for LLM agent")
        except Exception as e:
            logger.warning(f"Could not initialize LLM agent: {e}")
    else:
        logger.info("No ANTHROPIC_API_KEY found - LLM features disabled")

    # Register callbacks
    register_callbacks(app, db, llm_agent)

    return app


def main():
    """Run the application."""
    app = create_app()

    logger.info(f"Starting Baseball Statistics Explorer at http://{config.host}:{config.port}")

    # Check if data exists
    if not (config.processed_data_dir / "batting.parquet").exists():
        logger.warning(
            "No data found! Run 'python scripts/download_data.py' to download baseball data."
        )

    app.run(
        host=config.host,
        port=config.port,
        debug=config.debug,
    )


if __name__ == "__main__":
    main()
