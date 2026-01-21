"""Filter components for player/team selection."""

from dash import dcc, html
import dash_bootstrap_components as dbc


# Standard MLB positions
POSITIONS = ["C", "1B", "2B", "3B", "SS", "LF", "CF", "RF", "DH", "P"]


def create_team_filter(teams: list[str] = None):
    """
    Multi-select dropdown for team filtering.

    Args:
        teams: List of team abbreviations (populated dynamically if None)

    Returns:
        Dash Bootstrap Card component with dropdown
    """
    options = [{"label": t, "value": t} for t in (teams or [])]

    return dbc.Card(
        [
            dbc.CardHeader("Teams"),
            dbc.CardBody(
                [
                    dcc.Dropdown(
                        id="team-filter",
                        options=options,
                        multi=True,
                        placeholder="All teams",
                        className="mb-2",
                    )
                ]
            ),
        ],
        className="mb-3",
    )


def create_position_filter(positions: list[str] = None):
    """
    Checkbox group for position filtering.

    Args:
        positions: List of position abbreviations

    Returns:
        Dash Bootstrap Card component with checkboxes
    """
    positions = positions or POSITIONS

    return dbc.Card(
        [
            dbc.CardHeader("Positions"),
            dbc.CardBody(
                [
                    dbc.Checklist(
                        id="position-filter",
                        options=[{"label": p, "value": p} for p in positions],
                        value=positions,  # All selected by default
                        inline=True,
                        className="flex-wrap",
                    )
                ]
            ),
        ],
        className="mb-3",
    )


def create_player_search():
    """
    Typeahead search for player names.

    Returns:
        Dash Bootstrap Card component with searchable dropdown
    """
    return dbc.Card(
        [
            dbc.CardHeader("Search Player"),
            dbc.CardBody(
                [
                    dcc.Dropdown(
                        id="player-search",
                        options=[],  # Populated dynamically via callback
                        placeholder="Type player name...",
                        searchable=True,
                        clearable=True,
                        className="mb-2",
                    )
                ]
            ),
        ],
        className="mb-3",
    )


def create_stat_type_toggle():
    """
    Toggle between batting and pitching stats.

    Returns:
        Dash Bootstrap RadioItems component
    """
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.RadioItems(
                        id="stat-type-toggle",
                        options=[
                            {"label": "Batting", "value": "batting"},
                            {"label": "Pitching", "value": "pitching"},
                        ],
                        value="batting",
                        inline=True,
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                    )
                ]
            )
        ],
        className="mb-3",
    )


def create_stat_dropdown(stat_type: str = "batting", axis: str = "x"):
    """
    Dropdown for selecting which stat to display.

    Args:
        stat_type: 'batting' or 'pitching'
        axis: 'x' or 'y' for scatter plot axes

    Returns:
        Dropdown component
    """
    batting_stats = [
        {"label": "WAR", "value": "war"},
        {"label": "AVG", "value": "avg"},
        {"label": "OBP", "value": "obp"},
        {"label": "SLG", "value": "slg"},
        {"label": "OPS", "value": "ops"},
        {"label": "wRC+", "value": "wrc_plus"},
        {"label": "HR", "value": "hr"},
        {"label": "RBI", "value": "rbi"},
        {"label": "Runs", "value": "runs"},
        {"label": "SB", "value": "sb"},
        {"label": "ISO", "value": "iso"},
        {"label": "BABIP", "value": "babip"},
    ]

    pitching_stats = [
        {"label": "WAR", "value": "war"},
        {"label": "ERA", "value": "era"},
        {"label": "WHIP", "value": "whip"},
        {"label": "FIP", "value": "fip"},
        {"label": "K/9", "value": "k_per_9"},
        {"label": "BB/9", "value": "bb_per_9"},
        {"label": "Wins", "value": "wins"},
        {"label": "Saves", "value": "saves"},
        {"label": "IP", "value": "ip"},
        {"label": "K", "value": "k"},
    ]

    options = batting_stats if stat_type == "batting" else pitching_stats
    default = "war" if axis == "y" else ("obp" if stat_type == "batting" else "era")

    return dcc.Dropdown(
        id=f"{axis}-stat-dropdown",
        options=options,
        value=default,
        clearable=False,
        className="mb-2",
    )


def create_filter_panel(teams: list[str] = None):
    """
    Complete filter panel combining all filters.

    Args:
        teams: List of team abbreviations

    Returns:
        Dash component with all filters
    """
    return html.Div(
        [
            create_stat_type_toggle(),
            create_player_search(),
            create_team_filter(teams),
        ]
    )


def create_axis_selectors():
    """
    X and Y axis stat selectors for scatter plot.

    Returns:
        Card component with axis dropdowns
    """
    return dbc.Card(
        [
            dbc.CardHeader("Chart Axes"),
            dbc.CardBody(
                [
                    html.Label("X-Axis", className="small text-muted"),
                    dcc.Dropdown(
                        id="x-stat-dropdown",
                        options=[
                            {"label": "OBP", "value": "obp"},
                            {"label": "SLG", "value": "slg"},
                            {"label": "AVG", "value": "avg"},
                            {"label": "WAR", "value": "war"},
                            {"label": "wRC+", "value": "wrc_plus"},
                            {"label": "HR", "value": "hr"},
                            {"label": "ISO", "value": "iso"},
                        ],
                        value="obp",
                        clearable=False,
                        className="mb-2",
                    ),
                    html.Label("Y-Axis", className="small text-muted"),
                    dcc.Dropdown(
                        id="y-stat-dropdown",
                        options=[
                            {"label": "WAR", "value": "war"},
                            {"label": "SLG", "value": "slg"},
                            {"label": "OPS", "value": "ops"},
                            {"label": "wRC+", "value": "wrc_plus"},
                            {"label": "HR", "value": "hr"},
                            {"label": "RBI", "value": "rbi"},
                        ],
                        value="war",
                        clearable=False,
                    ),
                ]
            ),
        ],
        className="mb-3",
    )
