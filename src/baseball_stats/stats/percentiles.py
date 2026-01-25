"""Percentile calculations for player statistics."""

import pandas as pd
import numpy as np
from typing import Optional


def calculate_percentile(value: float, series: pd.Series) -> int:
    """
    Calculate the percentile rank of a value within a series.

    Args:
        value: The value to rank
        series: The series of values to compare against

    Returns:
        Percentile rank (0-100)
    """
    if pd.isna(value) or series.empty:
        return 0
    return int(round((series < value).sum() / len(series) * 100))


def get_season_percentiles(
    player_stats: dict,
    all_players_df: pd.DataFrame,
    season: int,
    stat_type: str = "batting"
) -> dict:
    """
    Calculate percentile rankings for a player's stats within their season.

    Args:
        player_stats: Dict of player's stats for the season
        all_players_df: DataFrame with all players' stats
        season: The season to compare within
        stat_type: 'batting' or 'pitching'

    Returns:
        Dict mapping stat names to percentile ranks
    """
    # Filter to same season
    season_df = all_players_df[all_players_df["season"] == season]

    if season_df.empty:
        return {}

    if stat_type == "batting":
        stats_to_rank = ["war", "avg", "obp", "slg", "ops", "hr", "rbi", "runs", "sb", "wrc_plus"]
    else:
        # For pitching, lower is better for ERA, WHIP
        stats_to_rank = ["war", "era", "whip", "fip", "k", "wins", "saves", "k_per_9"]

    percentiles = {}
    for stat in stats_to_rank:
        if stat not in player_stats or stat not in season_df.columns:
            continue

        value = player_stats.get(stat)
        if pd.isna(value):
            continue

        series = season_df[stat].dropna()

        # For stats where lower is better, invert the percentile
        if stat in ["era", "whip", "fip"]:
            # Lower is better: count how many are HIGHER
            percentiles[stat] = int(round((series > value).sum() / len(series) * 100))
        else:
            percentiles[stat] = calculate_percentile(value, series)

    return percentiles


def get_career_percentiles(
    career_stats: dict,
    all_players_df: pd.DataFrame,
    stat_type: str = "batting"
) -> dict:
    """
    Calculate percentile rankings for career stats compared to all players.

    Args:
        career_stats: Dict of player's career totals
        all_players_df: DataFrame with all players' season stats
        stat_type: 'batting' or 'pitching'

    Returns:
        Dict mapping stat names to percentile ranks
    """
    # Aggregate all players' careers
    if stat_type == "batting":
        agg_funcs = {
            "war": "sum",
            "hr": "sum",
            "rbi": "sum",
            "runs": "sum",
            "sb": "sum",
            "hits": "sum",
            "games": "sum",
        }
        stats_to_rank = ["war", "hr", "rbi", "runs", "sb", "hits", "games"]
    else:
        agg_funcs = {
            "war": "sum",
            "wins": "sum",
            "k": "sum",
            "saves": "sum",
            "ip": "sum",
            "games": "sum",
        }
        stats_to_rank = ["war", "wins", "k", "saves", "ip", "games"]

    # Only aggregate columns that exist
    agg_funcs = {k: v for k, v in agg_funcs.items() if k in all_players_df.columns}

    if not agg_funcs:
        return {}

    # Use IDfg for grouping to handle duplicate names correctly
    if "IDfg" in all_players_df.columns:
        career_totals = all_players_df.groupby("IDfg").agg(agg_funcs).reset_index()
    else:
        # Fallback to name if IDfg not available
        career_totals = all_players_df.groupby("name").agg(agg_funcs).reset_index()

    percentiles = {}
    for stat in stats_to_rank:
        if stat not in career_stats or stat not in career_totals.columns:
            continue

        value = career_stats.get(stat)
        if pd.isna(value):
            continue

        series = career_totals[stat].dropna()
        percentiles[stat] = calculate_percentile(value, series)

    return percentiles


def get_percentile_color(percentile: int) -> str:
    """
    Get a color based on percentile rank.

    Args:
        percentile: 0-100 percentile rank

    Returns:
        CSS color string
    """
    if percentile >= 90:
        return "#28a745"  # Green - elite
    elif percentile >= 75:
        return "#20c997"  # Teal - excellent
    elif percentile >= 50:
        return "#6c757d"  # Gray - average
    elif percentile >= 25:
        return "#fd7e14"  # Orange - below average
    else:
        return "#dc3545"  # Red - poor


def get_percentile_label(percentile: int) -> str:
    """
    Get a descriptive label for a percentile rank.

    Args:
        percentile: 0-100 percentile rank

    Returns:
        Descriptive label
    """
    if percentile >= 95:
        return "Elite"
    elif percentile >= 90:
        return "Excellent"
    elif percentile >= 75:
        return "Great"
    elif percentile >= 50:
        return "Above Avg"
    elif percentile >= 25:
        return "Below Avg"
    else:
        return "Poor"
