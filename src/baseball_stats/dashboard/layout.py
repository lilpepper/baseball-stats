"""Main dashboard layout using Dash Bootstrap Components."""

from dash import dcc, html
import dash_bootstrap_components as dbc

from .components.sliders import (
    create_year_range_slider,
    create_games_played_slider,
    create_pa_slider,
    create_war_gauge,
)
from .components.filters import (
    create_filter_panel,
    create_axis_selectors,
)
from .components.charts import create_chart_container, create_table_container
from .components.formula_builder import create_formula_builder, create_builtin_formulas_list
from .components.chat_panel import create_chat_panel


def create_layout():
    """
    Create the main application layout.

    Returns:
        Dash Bootstrap Container with full app layout
    """
    return dbc.Container(
        [
            # Data stores
            dcc.Store(id="filtered-data-store"),
            dcc.Store(id="batting-data-store"),
            dcc.Store(id="pitching-data-store"),
            # Header
            _create_header(),
            # Main content
            dbc.Row(
                [
                    # Left sidebar - Filters and Controls
                    dbc.Col(
                        _create_sidebar(),
                        width=3,
                        className="bg-light border-end",
                        style={"minHeight": "calc(100vh - 80px)"},
                    ),
                    # Main content area
                    dbc.Col(
                        _create_main_content(),
                        width=9,
                    ),
                ],
                className="g-0",
            ),
        ],
        fluid=True,
        className="px-0",
    )


def _create_header():
    """Create the app header."""
    return dbc.Navbar(
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H4(
                                    "Baseball Statistics Explorer",
                                    className="text-white mb-0",
                                ),
                                html.Small(
                                    "Interactive analysis with AI assistance",
                                    className="text-light",
                                ),
                            ]
                        ),
                    ],
                    align="center",
                    className="g-0",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Button(
                                "Download Data",
                                id="refresh-data-btn",
                                color="light",
                                size="sm",
                                outline=True,
                            ),
                            width="auto",
                        ),
                    ],
                    align="center",
                ),
            ],
            fluid=True,
        ),
        color="primary",
        dark=True,
        className="mb-0",
    )


def _create_sidebar():
    """Create the sidebar with filters and sliders."""
    return html.Div(
        [
            html.Div(
                [
                    html.H6("Filters", className="text-uppercase text-muted mb-3"),
                    create_filter_panel(),
                    html.Hr(),
                    html.H6("Time Range", className="text-uppercase text-muted mb-3"),
                    create_year_range_slider(1900, 2024),
                    html.Hr(),
                    html.H6("Qualifiers", className="text-uppercase text-muted mb-3"),
                    create_pa_slider(),
                    create_games_played_slider(),
                    html.Hr(),
                    html.H6("Chart Settings", className="text-uppercase text-muted mb-3"),
                    create_axis_selectors(),
                ],
                className="p-3",
            )
        ],
        style={"overflowY": "auto", "height": "calc(100vh - 80px)"},
    )


def _create_main_content():
    """Create the main content area with tabs."""
    return html.Div(
        [
            dbc.Tabs(
                [
                    dbc.Tab(
                        _create_explorer_tab(),
                        label="Explorer",
                        tab_id="explorer",
                    ),
                    dbc.Tab(
                        _create_player_card_tab(),
                        label="Player Card",
                        tab_id="player-card",
                    ),
                    dbc.Tab(
                        _create_compare_tab(),
                        label="Compare",
                        tab_id="compare",
                    ),
                    dbc.Tab(
                        _create_custom_stats_tab(),
                        label="Custom Stats",
                        tab_id="custom-stats",
                    ),
                    dbc.Tab(
                        _create_chat_tab(),
                        label="AI Assistant",
                        tab_id="chat",
                    ),
                ],
                id="main-tabs",
                active_tab="explorer",
                className="mb-3",
            ),
        ],
        className="p-3",
    )


def _create_explorer_tab():
    """Create the main data explorer tab."""
    return html.Div(
        [
            # Summary stats row
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H6("Players", className="text-muted"),
                                        html.H3(id="total-players-count", children="0"),
                                    ]
                                )
                            ]
                        ),
                        width=3,
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H6("Avg WAR", className="text-muted"),
                                        html.H3(id="avg-war-display", children="0.0"),
                                    ]
                                )
                            ]
                        ),
                        width=3,
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H6("Top WAR", className="text-muted"),
                                        html.H3(id="top-war-display", children="0.0"),
                                    ]
                                )
                            ]
                        ),
                        width=3,
                    ),
                    dbc.Col(
                        create_war_gauge(),
                        width=3,
                    ),
                ],
                className="mb-4",
            ),
            # Chart
            create_chart_container(),
            # Table
            create_table_container(),
        ]
    )


def _create_player_card_tab():
    """Create the individual player stat card tab."""
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Label("Search Player"),
                            dcc.Dropdown(
                                id="player-card-search",
                                placeholder="Type player name...",
                                searchable=True,
                                clearable=True,
                            ),
                        ],
                        width=6,
                    ),
                    dbc.Col(
                        [
                            dbc.Label("Season (optional)"),
                            dcc.Dropdown(
                                id="player-card-season",
                                placeholder="All seasons",
                                clearable=True,
                            ),
                        ],
                        width=3,
                    ),
                ],
                className="mb-4",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Loading(
                            id="player-card-loading",
                            children=[html.Div(id="player-card-content")],
                        ),
                        width=12,
                    ),
                ]
            ),
        ]
    )


def _create_compare_tab():
    """Create the player comparison tab."""
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Label("Player 1"),
                            dcc.Dropdown(
                                id="compare-player-1",
                                placeholder="Select first player...",
                                searchable=True,
                            ),
                        ],
                        width=6,
                    ),
                    dbc.Col(
                        [
                            dbc.Label("Player 2"),
                            dcc.Dropdown(
                                id="compare-player-2",
                                placeholder="Select second player...",
                                searchable=True,
                            ),
                        ],
                        width=6,
                    ),
                ],
                className="mb-4",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Loading(
                            id="comparison-loading",
                            children=[
                                dcc.Graph(
                                    id="comparison-chart",
                                    style={"height": "400px"},
                                )
                            ],
                        ),
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(id="comparison-table"),
                        className="mt-3",
                    )
                ]
            ),
        ]
    )


def _create_custom_stats_tab():
    """Create the custom statistics builder tab."""
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        create_formula_builder(),
                        width=8,
                    ),
                    dbc.Col(
                        create_builtin_formulas_list(),
                        width=4,
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader("Custom Stat Leaderboard"),
                                    dbc.CardBody(
                                        [
                                            dcc.Loading(
                                                children=[
                                                    html.Div(id="custom-stat-leaderboard")
                                                ]
                                            )
                                        ]
                                    ),
                                ]
                            )
                        ]
                    )
                ],
                className="mt-3",
            ),
        ]
    )


def _create_chat_tab():
    """Create the AI chat assistant tab."""
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        create_chat_panel(),
                        width=12,
                    ),
                ]
            )
        ]
    )
