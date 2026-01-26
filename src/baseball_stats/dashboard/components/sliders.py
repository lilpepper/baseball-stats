"""Slider and dial components for data exploration."""

from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_daq as daq


def create_year_range_slider(min_year: int = 1900, max_year: int = 2024):
    """
    Dual-handle slider for year range selection.

    Args:
        min_year: Minimum year value
        max_year: Maximum year value

    Returns:
        Dash Bootstrap Card component with range slider
    """
    # Create marks at decade intervals
    marks = {y: str(y) for y in range(min_year, max_year + 1, 10)}
    marks[max_year] = str(max_year)  # Ensure max year is marked

    return dbc.Card(
        [
            dbc.CardHeader("Year Range"),
            dbc.CardBody(
                [
                    dcc.RangeSlider(
                        id="year-range-slider",
                        min=min_year,
                        max=max_year,
                        value=[1950, max_year],  # Default to 1950-present
                        marks=marks,
                        tooltip={"placement": "bottom", "always_visible": True},
                        allowCross=False,
                        step=1,
                    )
                ]
            ),
        ],
        className="mb-3",
    )


def create_stat_threshold_slider(
    stat_name: str,
    stat_id: str,
    min_val: float,
    max_val: float,
    default_val: float = None,
    step: float = None,
):
    """
    Slider for filtering by statistical threshold.

    Args:
        stat_name: Display name for the stat
        stat_id: ID suffix for the slider
        min_val: Minimum value
        max_val: Maximum value
        default_val: Default value (defaults to min_val)
        step: Step increment

    Returns:
        Dash Bootstrap Card component with slider
    """
    default_val = default_val if default_val is not None else min_val
    step = step if step is not None else (max_val - min_val) / 20

    return dbc.Card(
        [
            dbc.CardHeader(f"Min {stat_name}"),
            dbc.CardBody(
                [
                    dcc.Slider(
                        id=f"{stat_id}-threshold-slider",
                        min=min_val,
                        max=max_val,
                        value=default_val,
                        step=step,
                        marks={
                            min_val: f"{min_val:.1f}",
                            max_val: f"{max_val:.1f}",
                        },
                        tooltip={"placement": "bottom", "always_visible": True},
                    )
                ]
            ),
        ],
        className="mb-3",
    )


def create_war_gauge(value: float = 0, label: str = "WAR"):
    """
    Circular gauge for WAR display.

    WAR color ranges:
    - Red: Below 0 (replacement level)
    - Yellow: 0-2 (role player)
    - Green: 2-6 (solid starter to star)
    - Blue: 6+ (MVP caliber)

    Args:
        value: Current WAR value to display
        label: Label text

    Returns:
        Dash DAQ Gauge component
    """
    return daq.Gauge(
        id="war-gauge",
        label=label,
        value=value,
        min=-2,
        max=12,
        showCurrentValue=True,
        units="WAR",
        color={
            "gradient": True,
            "ranges": {
                "#FF4136": [-2, 0],  # Red: below replacement
                "#FFDC00": [0, 2],  # Yellow: replacement to average
                "#2ECC40": [2, 6],  # Green: above average to star
                "#0074D9": [6, 12],  # Blue: superstar
            },
        },
        style={"margin": "auto"},
    )


def create_stat_weight_knob(
    stat_name: str,
    stat_id: str,
    default_value: float = 1.0,
    min_val: float = 0,
    max_val: float = 3,
):
    """
    Rotary knob for adjusting stat weights in formulas.

    Args:
        stat_name: Display name for the stat
        stat_id: ID suffix for the knob
        default_value: Default weight value
        min_val: Minimum weight
        max_val: Maximum weight

    Returns:
        Dash component with knob and label
    """
    return html.Div(
        [
            html.Label(stat_name, className="text-center d-block mb-1"),
            daq.Knob(
                id=f"{stat_id}-weight-knob",
                label="",
                value=default_value,
                min=min_val,
                max=max_val,
                scale={"interval": 0.5, "labelInterval": 1},
                color={"gradient": True, "ranges": {"blue": [0, 3]}},
                size=80,
            ),
            html.Div(
                id=f"{stat_id}-weight-display",
                className="text-center small text-muted",
            ),
        ],
        className="text-center",
    )


def create_games_played_slider(max_games: int = 162):
    """
    Slider for minimum games played filter.

    Args:
        max_games: Maximum games (162 for full MLB season)

    Returns:
        Dash Bootstrap Card component with slider
    """
    return dbc.Card(
        [
            dbc.CardHeader("Minimum Games"),
            dbc.CardBody(
                [
                    dcc.Slider(
                        id="min-games-slider",
                        min=0,
                        max=max_games,
                        step=10,
                        value=50,
                        marks={
                            0: "0",
                            50: "50",
                            100: "100",
                            max_games: str(max_games),
                        },
                        tooltip={"placement": "bottom", "always_visible": True},
                    )
                ]
            ),
        ],
        className="mb-3",
    )


def create_pa_slider(max_pa: int = 700):
    """
    Slider for minimum plate appearances filter.

    Args:
        max_pa: Maximum plate appearances

    Returns:
        Dash Bootstrap Card component with slider
    """
    return dbc.Card(
        [
            dbc.CardHeader("Minimum PA"),
            dbc.CardBody(
                [
                    dcc.Slider(
                        id="min-pa-slider",
                        min=0,
                        max=max_pa,
                        step=25,
                        value=100,
                        marks={
                            0: "0",
                            200: "200",
                            400: "400",
                            max_pa: str(max_pa),
                        },
                        tooltip={"placement": "bottom", "always_visible": True},
                    )
                ]
            ),
        ],
        className="mb-3",
    )


def create_stat_dial_panel():
    """
    Panel with multiple stat dials for quick weight adjustment.

    Returns:
        Dash Bootstrap Card with stat knobs
    """
    return dbc.Card(
        [
            dbc.CardHeader("Stat Weights"),
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                create_stat_weight_knob("OBP", "obp"),
                                width=3,
                            ),
                            dbc.Col(
                                create_stat_weight_knob("SLG", "slg"),
                                width=3,
                            ),
                            dbc.Col(
                                create_stat_weight_knob("WAR", "war"),
                                width=3,
                            ),
                            dbc.Col(
                                create_stat_weight_knob("ISO", "iso"),
                                width=3,
                            ),
                        ],
                        className="g-2",
                    ),
                ]
            ),
        ],
        className="mb-3",
    )
