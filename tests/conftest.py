"""Pytest fixtures for baseball-stats tests."""

import pytest
import pandas as pd


@pytest.fixture
def sample_batting_data():
    """Sample batting data for testing."""
    return pd.DataFrame({
        "name": ["Mike Trout", "Mookie Betts", "Shohei Ohtani", "Ronald Acuna Jr."],
        "team": ["LAA", "LAD", "LAA", "ATL"],
        "season": [2023, 2023, 2023, 2023],
        "games": [82, 152, 135, 159],
        "pa": [352, 693, 599, 735],
        "ab": [307, 584, 497, 643],
        "hits": [79, 179, 151, 217],
        "hr": [18, 39, 44, 41],
        "rbi": [44, 107, 95, 106],
        "runs": [52, 126, 102, 149],
        "sb": [1, 14, 20, 73],
        "bb": [40, 96, 91, 80],
        "k": [82, 125, 143, 104],
        "avg": [0.257, 0.307, 0.304, 0.337],
        "obp": [0.367, 0.408, 0.412, 0.416],
        "slg": [0.490, 0.579, 0.654, 0.596],
        "ops": [0.857, 0.987, 1.066, 1.012],
        "war": [3.5, 8.4, 10.0, 8.2],
        "wrc_plus": [140, 167, 191, 174],
        "woba": [0.370, 0.410, 0.430, 0.410],
        "iso": [0.233, 0.272, 0.350, 0.259],
        "babip": [0.310, 0.340, 0.340, 0.380],
        "bb_pct": [11.4, 13.9, 15.2, 10.9],
        "k_pct": [23.3, 18.0, 23.9, 14.1],
    })


@pytest.fixture
def sample_pitching_data():
    """Sample pitching data for testing."""
    return pd.DataFrame({
        "name": ["Gerrit Cole", "Spencer Strider", "Kevin Gausman", "Zack Wheeler"],
        "team": ["NYY", "ATL", "TOR", "PHI"],
        "season": [2023, 2023, 2023, 2023],
        "wins": [15, 20, 12, 13],
        "losses": [4, 5, 9, 6],
        "era": [2.63, 3.86, 3.16, 3.61],
        "whip": [0.98, 1.05, 1.07, 1.13],
        "games": [33, 32, 31, 32],
        "games_started": [33, 32, 31, 32],
        "ip": [209.0, 186.2, 185.1, 192.0],
        "k": [222, 281, 237, 212],
        "bb": [48, 51, 42, 47],
        "hr": [23, 25, 22, 28],
        "saves": [0, 0, 0, 0],
        "war": [5.5, 6.0, 4.8, 4.5],
        "fip": [3.12, 3.00, 2.90, 3.45],
        "xfip": [3.20, 3.10, 3.00, 3.50],
        "k_per_9": [9.6, 13.5, 11.5, 9.9],
        "bb_per_9": [2.1, 2.5, 2.0, 2.2],
        "hr_per_9": [1.0, 1.2, 1.1, 1.3],
        "k_pct": [28.0, 35.0, 30.0, 27.0],
        "bb_pct": [6.0, 7.0, 5.5, 6.0],
    })
