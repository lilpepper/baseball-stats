"""Player similarity calculations based on statistical profiles."""

import pandas as pd
import numpy as np
from typing import Optional


def calculate_similarity_score(
    player_stats: dict,
    comparison_stats: dict,
    stat_weights: dict,
) -> float:
    """
    Calculate similarity score between two players using weighted Euclidean distance.

    Args:
        player_stats: Dict of normalized stats for the target player
        comparison_stats: Dict of normalized stats for comparison player
        stat_weights: Dict of weights for each stat

    Returns:
        Similarity score (0-100, higher = more similar)
    """
    total_weight = 0
    weighted_distance = 0

    for stat, weight in stat_weights.items():
        if stat in player_stats and stat in comparison_stats:
            p1 = player_stats[stat]
            p2 = comparison_stats[stat]
            if not pd.isna(p1) and not pd.isna(p2):
                weighted_distance += weight * ((p1 - p2) ** 2)
                total_weight += weight

    if total_weight == 0:
        return 0

    # Convert distance to similarity (0-100 scale)
    distance = np.sqrt(weighted_distance / total_weight)
    # Assuming normalized stats are 0-1, max distance is ~1
    similarity = max(0, 100 * (1 - distance))
    return round(similarity, 1)


def normalize_stats(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Normalize stats to 0-1 scale using min-max normalization.

    Args:
        df: DataFrame with stats
        columns: List of columns to normalize

    Returns:
        DataFrame with normalized columns (suffixed with _norm)
    """
    result = df.copy()
    for col in columns:
        if col in result.columns:
            min_val = result[col].min()
            max_val = result[col].max()
            if max_val > min_val:
                result[f"{col}_norm"] = (result[col] - min_val) / (max_val - min_val)
            else:
                result[f"{col}_norm"] = 0.5
    return result


def find_similar_players(
    player_id: str,
    all_players_df: pd.DataFrame,
    stat_type: str = "batting",
    top_n: int = 5,
    same_era: bool = False,
) -> list[dict]:
    """
    Find players with similar statistical profiles.

    Args:
        player_id: IDfg of the target player (handles duplicate names)
        all_players_df: DataFrame with all player stats (must have IDfg column)
        stat_type: 'batting' or 'pitching'
        top_n: Number of similar players to return
        same_era: If True, only compare players from similar eras

    Returns:
        List of dicts with similar player info and similarity scores
    """
    # Ensure IDfg column exists and convert to string for comparison
    if "IDfg" not in all_players_df.columns:
        return []

    # Get target player's career stats using IDfg
    player_df = all_players_df[all_players_df["IDfg"].astype(str) == str(player_id)]
    if player_df.empty:
        return []

    player_name = player_df["name"].iloc[0]

    # Define stats to use for similarity
    if stat_type == "batting":
        stats_to_compare = ["war", "avg", "obp", "slg", "hr", "sb", "rbi"]
        stat_weights = {
            "war": 2.0,      # WAR is most important
            "avg": 1.0,
            "obp": 1.5,
            "slg": 1.5,
            "hr": 1.0,
            "sb": 0.5,
            "rbi": 0.5,
        }
    else:
        stats_to_compare = ["war", "era", "whip", "k_per_9", "wins"]
        stat_weights = {
            "war": 2.0,
            "era": 1.5,
            "whip": 1.5,
            "k_per_9": 1.0,
            "wins": 0.5,
        }

    # Calculate career averages for the target player
    player_career = {}
    for stat in stats_to_compare:
        if stat in player_df.columns:
            if stat in ["hr", "rbi", "sb", "wins"]:
                # Per-season average for counting stats
                player_career[stat] = player_df[stat].mean()
            else:
                player_career[stat] = player_df[stat].mean()

    player_seasons = player_df["season"].tolist()
    player_era_start = min(player_seasons) if player_seasons else 1900
    player_era_end = max(player_seasons) if player_seasons else 2024

    # Calculate career averages for all other players (exclude by IDfg, not name)
    other_players = all_players_df[all_players_df["IDfg"].astype(str) != str(player_id)]

    # Filter by era if requested
    if same_era:
        # Include players whose careers overlap or are within 20 years
        era_range = 20
        other_players = other_players.groupby("IDfg").filter(
            lambda x: (x["season"].min() <= player_era_end + era_range) and
                      (x["season"].max() >= player_era_start - era_range)
        )

    # Aggregate other players' careers by IDfg (handles duplicate names correctly)
    agg_dict = {stat: "mean" for stat in stats_to_compare if stat in other_players.columns}
    agg_dict["name"] = "first"  # Keep player name for display
    career_stats = other_players.groupby("IDfg").agg(agg_dict).reset_index()

    if career_stats.empty:
        return []

    # Normalize all stats including player's
    all_career_stats = pd.concat([
        career_stats,
        pd.DataFrame([{"IDfg": player_id, "name": player_name, **player_career}])
    ], ignore_index=True)

    normalized_df = normalize_stats(all_career_stats, stats_to_compare)

    # Get normalized player stats
    player_norm = normalized_df[normalized_df["IDfg"].astype(str) == str(player_id)].iloc[0].to_dict()
    player_norm_stats = {f"{s}_norm": player_norm.get(f"{s}_norm", 0.5) for s in stats_to_compare}

    # Calculate similarity for each other player
    similarities = []
    for _, row in normalized_df[normalized_df["IDfg"].astype(str) != str(player_id)].iterrows():
        other_norm_stats = {f"{s}_norm": row.get(f"{s}_norm", 0.5) for s in stats_to_compare}
        score = calculate_similarity_score(
            {k: player_norm_stats.get(k, 0.5) for k in [f"{s}_norm" for s in stats_to_compare]},
            {k: other_norm_stats.get(k, 0.5) for k in [f"{s}_norm" for s in stats_to_compare]},
            {f"{s}_norm": stat_weights.get(s, 1.0) for s in stats_to_compare}
        )

        # Get original stats for display
        original_stats = career_stats[career_stats["IDfg"].astype(str) == str(row["IDfg"])]
        if not original_stats.empty:
            orig = original_stats.iloc[0].to_dict()
            similarities.append({
                "name": row["name"],
                "similarity": score,
                "war": round(orig.get("war", 0), 1),
                "avg": round(orig.get("avg", 0), 3) if stat_type == "batting" else None,
                "era": round(orig.get("era", 0), 2) if stat_type == "pitching" else None,
            })

    # Sort by similarity and return top N
    similarities.sort(key=lambda x: x["similarity"], reverse=True)
    return similarities[:top_n]
