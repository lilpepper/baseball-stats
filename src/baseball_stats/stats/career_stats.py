"""Career statistics aggregation with proper weighted calculations."""

import pandas as pd
from typing import Optional


def calculate_career_batting_stats(df: pd.DataFrame) -> dict:
    """
    Calculate career batting statistics with proper aggregation.

    - Counting stats (HR, RBI, etc.) are summed
    - Rate stats (AVG, OBP, SLG) use weighted calculations
    - WAR is summed

    Args:
        df: DataFrame with season-by-season batting stats for a player

    Returns:
        Dictionary of career statistics
    """
    if df.empty:
        return {}

    # Summed counting stats
    career = {
        "seasons": len(df),
        "games": int(df["games"].sum()) if "games" in df.columns else 0,
        "pa": int(df["pa"].sum()) if "pa" in df.columns else 0,
        "ab": int(df["ab"].sum()) if "ab" in df.columns else 0,
        "hits": int(df["hits"].sum()) if "hits" in df.columns else 0,
        "hr": int(df["hr"].sum()) if "hr" in df.columns else 0,
        "rbi": int(df["rbi"].sum()) if "rbi" in df.columns else 0,
        "runs": int(df["runs"].sum()) if "runs" in df.columns else 0,
        "sb": int(df["sb"].sum()) if "sb" in df.columns else 0,
        "bb": int(df["bb"].sum()) if "bb" in df.columns else 0,
        "k": int(df["k"].sum()) if "k" in df.columns else 0,
        "war": round(df["war"].sum(), 1) if "war" in df.columns else 0,
    }

    # Weighted rate stats
    total_ab = career["ab"]
    total_pa = career["pa"]
    total_hits = career["hits"]
    total_bb = career["bb"]

    # AVG = H / AB
    if total_ab > 0:
        career["avg"] = round(total_hits / total_ab, 3)
    else:
        career["avg"] = 0.0

    # OBP approximation = (H + BB) / PA (simplified, ignores HBP/SF)
    if total_pa > 0:
        career["obp"] = round((total_hits + total_bb) / total_pa, 3)
    else:
        career["obp"] = 0.0

    # SLG - need total bases, approximate from existing SLG * AB per season
    if total_ab > 0 and "slg" in df.columns:
        total_bases = (df["slg"] * df["ab"]).sum()
        career["slg"] = round(total_bases / total_ab, 3)
    else:
        career["slg"] = 0.0

    # OPS = OBP + SLG
    career["ops"] = round(career["obp"] + career["slg"], 3)

    # ISO = SLG - AVG
    career["iso"] = round(career["slg"] - career["avg"], 3)

    # wRC+ weighted by PA
    if "wrc_plus" in df.columns and total_pa > 0:
        career["wrc_plus"] = round((df["wrc_plus"] * df["pa"]).sum() / total_pa, 0)

    return career


def calculate_career_pitching_stats(df: pd.DataFrame) -> dict:
    """
    Calculate career pitching statistics with proper aggregation.

    - Counting stats (W, K, etc.) are summed
    - Rate stats (ERA, WHIP) use weighted calculations by IP
    - WAR is summed

    Args:
        df: DataFrame with season-by-season pitching stats for a player

    Returns:
        Dictionary of career statistics
    """
    if df.empty:
        return {}

    # Summed counting stats
    career = {
        "seasons": len(df),
        "games": int(df["games"].sum()) if "games" in df.columns else 0,
        "games_started": int(df["games_started"].sum()) if "games_started" in df.columns else 0,
        "wins": int(df["wins"].sum()) if "wins" in df.columns else 0,
        "losses": int(df["losses"].sum()) if "losses" in df.columns else 0,
        "saves": int(df["saves"].sum()) if "saves" in df.columns else 0,
        "ip": round(df["ip"].sum(), 1) if "ip" in df.columns else 0,
        "k": int(df["k"].sum()) if "k" in df.columns else 0,
        "bb": int(df["bb"].sum()) if "bb" in df.columns else 0,
        "hr": int(df["hr"].sum()) if "hr" in df.columns else 0,
        "war": round(df["war"].sum(), 1) if "war" in df.columns else 0,
    }

    total_ip = career["ip"]

    # ERA = (ER * 9) / IP - calculate from ERA * IP / 9 per season
    if total_ip > 0 and "era" in df.columns:
        total_earned_runs = (df["era"] * df["ip"] / 9).sum()
        career["era"] = round((total_earned_runs * 9) / total_ip, 2)
    else:
        career["era"] = 0.0

    # WHIP = (BB + H) / IP - calculate from WHIP * IP per season
    if total_ip > 0 and "whip" in df.columns:
        total_baserunners = (df["whip"] * df["ip"]).sum()
        career["whip"] = round(total_baserunners / total_ip, 2)
    else:
        career["whip"] = 0.0

    # FIP weighted by IP
    if total_ip > 0 and "fip" in df.columns:
        weighted_fip = (df["fip"] * df["ip"]).sum()
        career["fip"] = round(weighted_fip / total_ip, 2)
    else:
        career["fip"] = 0.0

    # K/9
    if total_ip > 0:
        career["k_per_9"] = round((career["k"] * 9) / total_ip, 1)
    else:
        career["k_per_9"] = 0.0

    # BB/9
    if total_ip > 0:
        career["bb_per_9"] = round((career["bb"] * 9) / total_ip, 1)
    else:
        career["bb_per_9"] = 0.0

    return career


def get_career_comparison_df(
    players_data: dict[str, pd.DataFrame],
    stat_type: str = "batting"
) -> pd.DataFrame:
    """
    Create a comparison DataFrame for multiple players' career stats.

    Args:
        players_data: Dict mapping player names to their season DataFrames
        stat_type: 'batting' or 'pitching'

    Returns:
        DataFrame with players as columns and stats as rows
    """
    if not players_data:
        return pd.DataFrame()

    calc_func = calculate_career_batting_stats if stat_type == "batting" else calculate_career_pitching_stats

    career_stats = {}
    for player_name, df in players_data.items():
        career_stats[player_name] = calc_func(df)

    # Convert to DataFrame with stats as index
    comparison_df = pd.DataFrame(career_stats)

    return comparison_df
