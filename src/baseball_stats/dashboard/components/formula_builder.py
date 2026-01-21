"""Visual formula builder component for custom statistics."""

from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_daq as daq


def create_formula_builder():
    """
    Create the visual formula builder interface.

    Provides two modes:
    1. Quick Mode: Adjust knobs for weighted combination of stats
    2. Advanced Mode: Write custom formula expressions

    Returns:
        Dash Bootstrap Card component
    """
    return dbc.Card(
        [
            dbc.CardHeader(
                [
                    html.H5("Custom Stat Builder", className="mb-0"),
                ]
            ),
            dbc.CardBody(
                [
                    # Formula name input
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.Label("Formula Name"),
                                    dbc.Input(
                                        id="formula-name-input",
                                        placeholder="My Custom Stat",
                                        type="text",
                                    ),
                                ],
                                width=6,
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Description"),
                                    dbc.Input(
                                        id="formula-description-input",
                                        placeholder="What this stat measures...",
                                        type="text",
                                    ),
                                ],
                                width=6,
                            ),
                        ],
                        className="mb-4",
                    ),
                    # Mode tabs
                    dbc.Tabs(
                        [
                            dbc.Tab(
                                _create_quick_mode(),
                                label="Quick Mode",
                                tab_id="quick-mode",
                            ),
                            dbc.Tab(
                                _create_advanced_mode(),
                                label="Advanced Mode",
                                tab_id="advanced-mode",
                            ),
                        ],
                        id="formula-mode-tabs",
                        active_tab="quick-mode",
                    ),
                    html.Hr(),
                    # Preview area
                    html.H6("Preview"),
                    dcc.Loading(
                        id="formula-preview-loading",
                        children=[
                            html.Div(
                                id="formula-preview",
                                className="p-3 bg-light rounded",
                            )
                        ],
                    ),
                    html.Hr(),
                    # Action buttons
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Button(
                                    "Preview",
                                    id="preview-formula-btn",
                                    color="secondary",
                                    className="me-2",
                                ),
                                width="auto",
                            ),
                            dbc.Col(
                                dbc.Button(
                                    "Save Formula",
                                    id="save-formula-btn",
                                    color="primary",
                                ),
                                width="auto",
                            ),
                        ],
                        justify="end",
                    ),
                    # Feedback message
                    html.Div(id="formula-save-feedback", className="mt-2"),
                ]
            ),
        ],
        className="mb-3",
    )


def _create_quick_mode():
    """Create quick mode content with weight knobs."""
    return html.Div(
        [
            html.P(
                "Adjust weights for each stat. Higher weight = more influence on final score.",
                className="text-muted small mb-3",
            ),
            dbc.Row(
                [
                    dbc.Col(_create_weight_knob("OBP", "obp", 1.0), width=3),
                    dbc.Col(_create_weight_knob("SLG", "slg", 1.0), width=3),
                    dbc.Col(_create_weight_knob("WAR", "war", 0.5), width=3),
                    dbc.Col(_create_weight_knob("ISO", "iso", 0.5), width=3),
                ],
                className="mb-3",
            ),
            dbc.Row(
                [
                    dbc.Col(_create_weight_knob("AVG", "avg", 0.0), width=3),
                    dbc.Col(_create_weight_knob("wRC+", "wrc", 0.0), width=3),
                    dbc.Col(_create_weight_knob("HR", "hr", 0.0), width=3),
                    dbc.Col(_create_weight_knob("SB", "sb", 0.0), width=3),
                ],
            ),
            # Normalize option
            dbc.Checkbox(
                id="normalize-checkbox",
                label="Normalize stats to 0-1 range before weighting",
                value=True,
                className="mt-3",
            ),
        ],
        className="p-3",
    )


def _create_weight_knob(label: str, stat_id: str, default: float = 1.0):
    """Create a single weight knob with label."""
    return html.Div(
        [
            html.Label(label, className="text-center d-block mb-1 fw-bold"),
            daq.Knob(
                id=f"{stat_id}-weight-knob",
                value=default,
                min=0,
                max=3,
                scale={"interval": 0.5, "labelInterval": 1},
                color={"gradient": True, "ranges": {"#0074D9": [0, 3]}},
                size=70,
            ),
            html.Div(
                f"{default:.1f}x",
                id=f"{stat_id}-weight-value",
                className="text-center small text-muted",
            ),
        ],
        className="text-center",
    )


def _create_advanced_mode():
    """Create advanced mode content with formula input."""
    return html.Div(
        [
            html.P(
                "Write a custom formula using stat names and math operators.",
                className="text-muted small mb-3",
            ),
            dbc.Textarea(
                id="formula-input",
                placeholder="e.g., (obp * 1.8) + slg - (k_pct * 0.5)",
                style={"fontFamily": "monospace", "height": "100px"},
                className="mb-3",
            ),
            # Available stats reference
            dbc.Accordion(
                [
                    dbc.AccordionItem(
                        [
                            html.P(
                                [
                                    html.Strong("Batting: "),
                                    "avg, obp, slg, ops, woba, war, iso, babip, hr, rbi, "
                                    "runs, sb, bb, k, hits, ab, pa, games, bb_pct, k_pct, wrc_plus",
                                ],
                                className="mb-2",
                            ),
                            html.P(
                                [
                                    html.Strong("Pitching: "),
                                    "era, whip, fip, xfip, war, k_per_9, bb_per_9, hr_per_9, "
                                    "k_pct, bb_pct, wins, losses, saves, ip, k, bb, hr",
                                ],
                                className="mb-2",
                            ),
                            html.P(
                                [
                                    html.Strong("Functions: "),
                                    "abs(), sqrt(), log(), min(), max(), pow(), round()",
                                ],
                                className="mb-0",
                            ),
                        ],
                        title="Available Stats & Functions",
                    ),
                    dbc.AccordionItem(
                        [
                            html.Code("(obp * 1.8) + slg", className="d-block mb-1"),
                            html.Small(
                                "OPS with higher OBP weight", className="text-muted"
                            ),
                            html.Br(),
                            html.Code("(hr * 2) + sb", className="d-block mb-1 mt-2"),
                            html.Small("Power-Speed number", className="text-muted"),
                            html.Br(),
                            html.Code(
                                "war / pa * 600", className="d-block mb-1 mt-2"
                            ),
                            html.Small(
                                "WAR per 600 plate appearances", className="text-muted"
                            ),
                        ],
                        title="Example Formulas",
                    ),
                ],
                start_collapsed=True,
                className="mb-3",
            ),
        ],
        className="p-3",
    )


def create_saved_formulas_list():
    """
    Create a list of saved custom formulas.

    Returns:
        Dash component showing saved formulas
    """
    return dbc.Card(
        [
            dbc.CardHeader("Saved Formulas"),
            dbc.CardBody(
                [
                    dcc.Loading(
                        id="saved-formulas-loading",
                        children=[html.Div(id="saved-formulas-list")],
                    )
                ]
            ),
        ],
        className="mb-3",
    )


def create_builtin_formulas_list():
    """
    Create a list of built-in formulas users can apply.

    Returns:
        Dash component with built-in formula buttons
    """
    builtin_formulas = [
        ("OPS+ Custom", "OPS with 1.8x OBP weight"),
        ("Power-Speed", "HR * 2 + SB"),
        ("Plate Discipline", "BB% - K%"),
        ("WAR/600PA", "WAR normalized to 600 PA"),
    ]

    return dbc.Card(
        [
            dbc.CardHeader("Built-in Formulas"),
            dbc.CardBody(
                [
                    dbc.ListGroup(
                        [
                            dbc.ListGroupItem(
                                [
                                    html.Div(name, className="fw-bold"),
                                    html.Small(desc, className="text-muted"),
                                ],
                                action=True,
                                id={"type": "builtin-formula", "index": i},
                            )
                            for i, (name, desc) in enumerate(builtin_formulas)
                        ],
                        flush=True,
                    )
                ]
            ),
        ],
        className="mb-3",
    )
