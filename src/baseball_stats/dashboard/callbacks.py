"""Dash callback definitions for dashboard interactivity."""

import json
import logging
from io import StringIO
from typing import Optional

import pandas as pd
import plotly.express as px
from dash import Input, Output, State, callback, html, no_update
from dash.exceptions import PreventUpdate

from .components.charts import create_scatter_plot, create_leaderboard_table
from .components.chat_panel import create_chat_message

logger = logging.getLogger(__name__)


def register_callbacks(app, db, llm_agent=None):
    """
    Register all dashboard callbacks.

    Args:
        app: Dash application instance
        db: BaseballDatabase instance
        llm_agent: Optional BaseballLLMAgent instance
    """

    @app.callback(
        Output("batting-data-store", "data"),
        Output("pitching-data-store", "data"),
        Input("refresh-data-btn", "n_clicks"),
    )
    def load_initial_data(n_clicks):
        """Load initial data into stores."""
        try:
            batting = db.get_batting_stats()
            pitching = db.get_pitching_stats()
            return batting.to_json(orient="split"), pitching.to_json(orient="split")
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return None, None

    @app.callback(
        Output("team-filter", "options"),
        Input("stat-type-toggle", "value"),
    )
    def update_team_options(stat_type):
        """Update team dropdown options based on stat type."""
        try:
            teams = db.get_unique_teams(stat_type)
            return [{"label": t, "value": t} for t in teams]
        except Exception:
            return []

    @app.callback(
        Output("player-search", "options"),
        Input("player-search", "search_value"),
        Input("stat-type-toggle", "value"),
    )
    def update_player_options(search_value, stat_type):
        """Update player search dropdown based on search term."""
        if not search_value or len(search_value) < 2:
            return []
        try:
            players = db.search_players(search_value, stat_type)
            return [{"label": p, "value": p} for p in players]
        except Exception:
            return []

    @app.callback(
        Output("filtered-data-store", "data"),
        Input("year-range-slider", "value"),
        Input("team-filter", "value"),
        Input("min-pa-slider", "value"),
        Input("min-games-slider", "value"),
        Input("stat-type-toggle", "value"),
        Input("player-search", "value"),
    )
    def filter_data(year_range, teams, min_pa, min_games, stat_type, selected_player):
        """Filter data based on all filter inputs."""
        try:
            if stat_type == "batting":
                df = db.get_batting_stats(
                    player_names=[selected_player] if selected_player else None,
                    teams=teams if teams else None,
                    years=tuple(year_range) if year_range else None,
                    min_pa=min_pa or 0,
                )
            else:
                df = db.get_pitching_stats(
                    player_names=[selected_player] if selected_player else None,
                    teams=teams if teams else None,
                    years=tuple(year_range) if year_range else None,
                    min_ip=min_pa or 0,  # Reuse PA slider for IP
                )

            # Additional games filter
            if min_games and "games" in df.columns:
                df = df[df["games"] >= min_games]

            return df.to_json(orient="split")
        except Exception as e:
            logger.error(f"Error filtering data: {e}")
            return None

    @app.callback(
        Output("main-scatter-plot", "figure"),
        Output("table-container", "children"),
        Output("total-players-count", "children"),
        Output("avg-war-display", "children"),
        Output("top-war-display", "children"),
        Output("war-gauge", "value"),
        Input("filtered-data-store", "data"),
        Input("x-stat-dropdown", "value"),
        Input("y-stat-dropdown", "value"),
    )
    def update_main_view(filtered_data, x_stat, y_stat):
        """Update main visualization based on filtered data."""
        if not filtered_data:
            empty_fig = create_scatter_plot(None, x_stat, y_stat)
            empty_table = create_leaderboard_table(None)
            return empty_fig, empty_table, "0", "0.0", "0.0", 0

        try:
            df = pd.read_json(StringIO(filtered_data), orient="split")

            # Create scatter plot
            fig = create_scatter_plot(
                df,
                x_col=x_stat,
                y_col=y_stat,
                hover_name="name",
                title=f"{y_stat.upper()} vs {x_stat.upper()}",
            )

            # Create table
            table = create_leaderboard_table(df)

            # Calculate summary stats
            total_players = len(df)
            avg_war = df["war"].mean() if "war" in df.columns else 0
            top_war = df["war"].max() if "war" in df.columns else 0

            return (
                fig,
                table,
                f"{total_players:,}",
                f"{avg_war:.2f}",
                f"{top_war:.2f}",
                float(top_war) if top_war else 0,
            )
        except Exception as e:
            logger.error(f"Error updating view: {e}")
            empty_fig = create_scatter_plot(None, x_stat, y_stat)
            empty_table = create_leaderboard_table(None)
            return empty_fig, empty_table, "0", "0.0", "0.0", 0

    @app.callback(
        Output("player-card-search", "value", allow_duplicate=True),
        Output("main-tabs", "active_tab"),
        Input("main-scatter-plot", "clickData"),
        prevent_initial_call=True,
    )
    def handle_scatter_click(click_data):
        """Navigate to player card when clicking a point in scatter plot."""
        if not click_data or not click_data.get("points"):
            raise PreventUpdate

        # Extract player name from customdata
        point = click_data["points"][0]
        player_name = point.get("customdata", [None])[0]

        if not player_name:
            raise PreventUpdate

        return player_name, "player-card"

    @app.callback(
        Output("compare-player-1", "options"),
        Input("compare-player-1", "search_value"),
        Input("stat-type-toggle", "value"),
    )
    def update_compare_player1_options(search_value, stat_type):
        """Update comparison player 1 dropdown based on search."""
        if not search_value or len(search_value) < 2:
            raise PreventUpdate
        try:
            players = db.search_players(search_value, stat_type)
            return [{"label": p, "value": p} for p in players]
        except Exception:
            raise PreventUpdate

    @app.callback(
        Output("compare-player-2", "options"),
        Input("compare-player-2", "search_value"),
        Input("stat-type-toggle", "value"),
    )
    def update_compare_player2_options(search_value, stat_type):
        """Update comparison player 2 dropdown based on search."""
        if not search_value or len(search_value) < 2:
            raise PreventUpdate
        try:
            players = db.search_players(search_value, stat_type)
            return [{"label": p, "value": p} for p in players]
        except Exception:
            raise PreventUpdate

    @app.callback(
        Output("comparison-chart", "figure"),
        Output("comparison-radar-chart", "figure"),
        Output("comparison-table", "children"),
        Input("compare-player-1", "value"),
        Input("compare-player-2", "value"),
        Input("stat-type-toggle", "value"),
    )
    def update_comparison(player1, player2, stat_type):
        """Update player comparison view."""
        from .components.charts import create_radar_chart

        empty_radar = create_radar_chart({}, stat_type)

        if not player1 or not player2:
            return {}, empty_radar, html.Div("Select two players to compare")

        try:
            if stat_type == "batting":
                df1 = db.get_batting_stats(player_names=[player1])
                df2 = db.get_batting_stats(player_names=[player2])
                compare_cols = ["war", "avg", "obp", "slg", "hr", "rbi"]
            else:
                df1 = db.get_pitching_stats(player_names=[player1])
                df2 = db.get_pitching_stats(player_names=[player2])
                compare_cols = ["war", "era", "whip", "k", "wins", "ip"]

            # Combine for comparison
            df1["player"] = player1
            df2["player"] = player2
            combined = pd.concat([df1, df2])

            # Create comparison line chart by season
            fig = px.line(
                combined,
                x="season",
                y="war",
                color="player",
                markers=True,
                title=f"WAR Comparison: {player1} vs {player2}",
            )

            # Create comparison table
            stats1 = df1[compare_cols].mean().round(2)
            stats2 = df2[compare_cols].mean().round(2)

            # Create radar chart with career averages
            if stat_type == "batting":
                radar_stats = {
                    player1: {
                        "war": df1["war"].mean() if "war" in df1.columns else 0,
                        "avg": df1["avg"].mean() if "avg" in df1.columns else 0,
                        "obp": df1["obp"].mean() if "obp" in df1.columns else 0,
                        "slg": df1["slg"].mean() if "slg" in df1.columns else 0,
                        "hr": df1["hr"].mean() if "hr" in df1.columns else 0,
                        "sb": df1["sb"].mean() if "sb" in df1.columns else 0,
                    },
                    player2: {
                        "war": df2["war"].mean() if "war" in df2.columns else 0,
                        "avg": df2["avg"].mean() if "avg" in df2.columns else 0,
                        "obp": df2["obp"].mean() if "obp" in df2.columns else 0,
                        "slg": df2["slg"].mean() if "slg" in df2.columns else 0,
                        "hr": df2["hr"].mean() if "hr" in df2.columns else 0,
                        "sb": df2["sb"].mean() if "sb" in df2.columns else 0,
                    },
                }
            else:
                radar_stats = {
                    player1: {
                        "war": df1["war"].mean() if "war" in df1.columns else 0,
                        "era": df1["era"].mean() if "era" in df1.columns else 0,
                        "whip": df1["whip"].mean() if "whip" in df1.columns else 0,
                        "k_per_9": df1["k_per_9"].mean() if "k_per_9" in df1.columns else 0,
                        "wins": df1["wins"].mean() if "wins" in df1.columns else 0,
                        "saves": df1["saves"].mean() if "saves" in df1.columns else 0,
                    },
                    player2: {
                        "war": df2["war"].mean() if "war" in df2.columns else 0,
                        "era": df2["era"].mean() if "era" in df2.columns else 0,
                        "whip": df2["whip"].mean() if "whip" in df2.columns else 0,
                        "k_per_9": df2["k_per_9"].mean() if "k_per_9" in df2.columns else 0,
                        "wins": df2["wins"].mean() if "wins" in df2.columns else 0,
                        "saves": df2["saves"].mean() if "saves" in df2.columns else 0,
                    },
                }

            radar_fig = create_radar_chart(radar_stats, stat_type, "Stat Profile Comparison")

            table_data = []
            for col in compare_cols:
                table_data.append({
                    "Stat": col.upper(),
                    player1: stats1.get(col, "N/A"),
                    player2: stats2.get(col, "N/A"),
                })

            table = html.Table(
                [
                    html.Thead(
                        html.Tr([html.Th("Stat"), html.Th(player1), html.Th(player2)])
                    ),
                    html.Tbody([
                        html.Tr([
                            html.Td(row["Stat"]),
                            html.Td(str(row[player1])),
                            html.Td(str(row[player2])),
                        ])
                        for row in table_data
                    ]),
                ],
                className="table table-striped",
            )

            return fig, radar_fig, table
        except Exception as e:
            logger.error(f"Error in comparison: {e}")
            return {}, empty_radar, html.Div(f"Error: {str(e)}")

    # Player Card callbacks
    @app.callback(
        Output("player-card-search", "options"),
        Input("player-card-search", "search_value"),
        Input("stat-type-toggle", "value"),
    )
    def update_player_card_search(search_value, stat_type):
        """Update player card search dropdown."""
        if not search_value or len(search_value) < 2:
            # Don't clear options when search is empty (preserves selection)
            raise PreventUpdate
        try:
            players = db.search_players(search_value, stat_type)
            return [{"label": p, "value": p} for p in players]
        except Exception:
            raise PreventUpdate

    @app.callback(
        Output("player-card-season", "options"),
        Input("player-card-search", "value"),
        Input("stat-type-toggle", "value"),
    )
    def update_player_card_seasons(player_name, stat_type):
        """Update available seasons for selected player."""
        if not player_name:
            return []
        try:
            if stat_type == "batting":
                df = db.get_batting_stats(player_names=[player_name])
            else:
                df = db.get_pitching_stats(player_names=[player_name])
            seasons = sorted(df["season"].unique().tolist(), reverse=True)
            return [{"label": str(s), "value": s} for s in seasons]
        except Exception:
            return []

    @app.callback(
        Output("player-card-content", "children"),
        Input("player-card-search", "value"),
        Input("player-card-season", "value"),
        Input("stat-type-toggle", "value"),
    )
    def update_player_card(player_name, season, stat_type):
        """Generate player stat card."""
        if not player_name:
            return html.Div(
                "Search for a player to view their stat card",
                className="text-muted text-center py-5",
            )

        try:
            import dash_bootstrap_components as dbc
            import plotly.express as px
            from dash import dcc

            # Get player data
            if stat_type == "batting":
                df = db.get_batting_stats(player_names=[player_name])
                key_stats = ["war", "avg", "obp", "slg", "ops", "hr", "rbi", "runs", "sb", "hits"]
                stat_labels = {
                    "war": "WAR", "avg": "AVG", "obp": "OBP", "slg": "SLG",
                    "ops": "OPS", "hr": "HR", "rbi": "RBI", "runs": "R",
                    "sb": "SB", "hits": "H"
                }
            else:
                df = db.get_pitching_stats(player_names=[player_name])
                key_stats = ["war", "era", "whip", "fip", "wins", "losses", "saves", "k", "ip"]
                stat_labels = {
                    "war": "WAR", "era": "ERA", "whip": "WHIP", "fip": "FIP",
                    "wins": "W", "losses": "L", "saves": "SV", "k": "K", "ip": "IP"
                }

            if df.empty:
                return html.Div("No data found for this player", className="text-warning")

            # Filter by season if specified
            if season:
                season_df = df[df["season"] == season]
                if season_df.empty:
                    return html.Div(f"No data for {season}", className="text-warning")
            else:
                season_df = df

            # Career summary
            career_seasons = f"{df['season'].min()} - {df['season'].max()}"
            teams = ", ".join(df["team"].unique())

            # Calculate career totals/averages
            if stat_type == "batting":
                career_war = df["war"].sum()
                career_avg = df["avg"].mean()
                career_hr = int(df["hr"].sum())
                career_rbi = int(df["rbi"].sum())
                highlight_stats = [
                    ("Career WAR", f"{career_war:.1f}"),
                    ("Career AVG", f"{career_avg:.3f}"),
                    ("Career HR", f"{career_hr:,}"),
                    ("Career RBI", f"{career_rbi:,}"),
                ]
            else:
                career_war = df["war"].sum()
                career_era = df["era"].mean()
                career_wins = int(df["wins"].sum())
                career_k = int(df["k"].sum())
                highlight_stats = [
                    ("Career WAR", f"{career_war:.1f}"),
                    ("Career ERA", f"{career_era:.2f}"),
                    ("Career W", f"{career_wins:,}"),
                    ("Career K", f"{career_k:,}"),
                ]

            # Build stat cards for highlights
            highlight_cards = dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody([
                                html.H6(label, className="text-muted mb-1"),
                                html.H3(value, className="mb-0"),
                            ]),
                            className="text-center",
                        ),
                        width=3,
                    )
                    for label, value in highlight_stats
                ],
                className="mb-4",
            )

            # Season-by-season table
            display_cols = ["season", "team"] + [c for c in key_stats if c in df.columns]
            table_df = df[display_cols].copy()
            table_df.columns = ["Season", "Team"] + [stat_labels.get(c, c.upper()) for c in key_stats if c in df.columns]

            season_table = html.Div([
                html.H5("Season-by-Season Stats"),
                html.Table(
                    [
                        html.Thead(html.Tr([html.Th(c) for c in table_df.columns])),
                        html.Tbody([
                            html.Tr([html.Td(f"{v:.3f}" if isinstance(v, float) else str(v)) for v in row])
                            for row in table_df.values
                        ]),
                    ],
                    className="table table-striped table-sm",
                ),
            ])

            # WAR over time chart
            war_fig = px.bar(
                df.sort_values("season"),
                x="season",
                y="war",
                title=f"WAR by Season",
                labels={"season": "Season", "war": "WAR"},
            )
            war_fig.update_layout(height=300)

            return html.Div([
                # Player header
                dbc.Card(
                    dbc.CardBody([
                        html.H2(player_name, className="mb-1"),
                        html.P(f"{career_seasons} | {teams}", className="text-muted mb-0"),
                    ]),
                    className="mb-4",
                ),
                # Highlight stats
                highlight_cards,
                # WAR chart
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(figure=war_fig, config={"displayModeBar": False}),
                    ])
                ], className="mb-4"),
                # Season table
                dbc.Card([
                    dbc.CardBody(season_table),
                ]),
            ])

        except Exception as e:
            logger.error(f"Error generating player card: {e}")
            return html.Div(f"Error: {str(e)}", className="text-danger")

    # Career Totals callbacks
    @app.callback(
        Output("career-player-select", "options"),
        Input("career-player-select", "search_value"),
        Input("stat-type-toggle", "value"),
    )
    def update_career_player_options(search_value, stat_type):
        """Update career player search dropdown."""
        if not search_value or len(search_value) < 2:
            raise PreventUpdate
        try:
            players = db.search_players(search_value, stat_type)
            return [{"label": p, "value": p} for p in players]
        except Exception:
            raise PreventUpdate

    @app.callback(
        Output("career-summary-cards", "children"),
        Output("career-comparison-table", "children"),
        Output("career-war-chart", "figure"),
        Output("career-radar-chart", "figure"),
        Input("career-player-select", "value"),
        Input("stat-type-toggle", "value"),
    )
    def update_career_comparison(selected_players, stat_type):
        """Update career totals comparison view."""
        import dash_bootstrap_components as dbc
        import plotly.graph_objects as go
        from baseball_stats.stats.career_stats import (
            calculate_career_batting_stats,
            calculate_career_pitching_stats,
        )
        from .components.charts import create_radar_chart

        empty_fig = go.Figure()
        empty_fig.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            annotations=[dict(
                text="Select players to compare career totals",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False, font=dict(size=16)
            )]
        )
        empty_radar = create_radar_chart({}, stat_type)

        if not selected_players:
            return [], html.Div("Select players above to compare their career statistics", className="text-muted"), empty_fig, empty_radar

        # Limit to 5 players
        selected_players = selected_players[:5]

        try:
            # Get data for each player
            players_data = {}
            for player in selected_players:
                if stat_type == "batting":
                    df = db.get_batting_stats(player_names=[player])
                else:
                    df = db.get_pitching_stats(player_names=[player])
                if not df.empty:
                    players_data[player] = df

            if not players_data:
                return [], html.Div("No data found for selected players", className="text-warning"), empty_fig, empty_radar

            # Calculate career stats
            calc_func = calculate_career_batting_stats if stat_type == "batting" else calculate_career_pitching_stats
            career_stats = {name: calc_func(df) for name, df in players_data.items()}

            # Build summary cards (one per player with key stats)
            summary_cards = []
            for player, stats in career_stats.items():
                if stat_type == "batting":
                    card_stats = [
                        ("WAR", stats.get("war", 0)),
                        ("AVG", f"{stats.get('avg', 0):.3f}"),
                        ("HR", stats.get("hr", 0)),
                        ("RBI", stats.get("rbi", 0)),
                    ]
                else:
                    card_stats = [
                        ("WAR", stats.get("war", 0)),
                        ("ERA", f"{stats.get('era', 0):.2f}"),
                        ("W", stats.get("wins", 0)),
                        ("K", stats.get("k", 0)),
                    ]

                card = dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(player, className="fw-bold"),
                        dbc.CardBody([
                            html.Div([
                                html.Span(f"{label}: ", className="text-muted"),
                                html.Span(f"{value}", className="fw-bold"),
                            ], className="mb-1")
                            for label, value in card_stats
                        ]),
                    ]),
                    width=12 // min(len(career_stats), 4),
                    className="mb-2",
                )
                summary_cards.append(card)

            # Build comparison table
            if stat_type == "batting":
                stat_order = ["seasons", "games", "pa", "ab", "hits", "hr", "rbi", "runs", "sb", "bb", "k", "avg", "obp", "slg", "ops", "war"]
                stat_labels = {
                    "seasons": "Seasons", "games": "G", "pa": "PA", "ab": "AB",
                    "hits": "H", "hr": "HR", "rbi": "RBI", "runs": "R",
                    "sb": "SB", "bb": "BB", "k": "K", "avg": "AVG",
                    "obp": "OBP", "slg": "SLG", "ops": "OPS", "war": "WAR"
                }
            else:
                stat_order = ["seasons", "games", "games_started", "wins", "losses", "saves", "ip", "k", "bb", "hr", "era", "whip", "fip", "k_per_9", "war"]
                stat_labels = {
                    "seasons": "Seasons", "games": "G", "games_started": "GS",
                    "wins": "W", "losses": "L", "saves": "SV", "ip": "IP",
                    "k": "K", "bb": "BB", "hr": "HR", "era": "ERA",
                    "whip": "WHIP", "fip": "FIP", "k_per_9": "K/9", "war": "WAR"
                }

            # Build table rows
            table_rows = []
            for stat in stat_order:
                if stat not in stat_labels:
                    continue
                row_data = [html.Td(stat_labels[stat], className="fw-bold")]
                for player in career_stats:
                    value = career_stats[player].get(stat, "-")
                    if isinstance(value, float):
                        value = f"{value:.3f}" if stat in ["avg", "obp", "slg", "ops"] else f"{value:.2f}" if stat in ["era", "whip", "fip"] else f"{value:.1f}"
                    row_data.append(html.Td(str(value)))
                table_rows.append(html.Tr(row_data))

            comparison_table = html.Table(
                [
                    html.Thead(html.Tr([html.Th("Stat")] + [html.Th(p) for p in career_stats.keys()])),
                    html.Tbody(table_rows),
                ],
                className="table table-striped table-hover",
            )

            # Build WAR comparison bar chart
            war_fig = go.Figure()
            players = list(career_stats.keys())
            wars = [career_stats[p].get("war", 0) for p in players]
            war_fig.add_trace(go.Bar(
                x=players,
                y=wars,
                text=[f"{w:.1f}" for w in wars],
                textposition="auto",
                marker_color=px.colors.qualitative.Set2[:len(players)],
            ))
            war_fig.update_layout(
                title="Career WAR Comparison",
                xaxis_title="Player",
                yaxis_title="Career WAR",
                showlegend=False,
                height=350,
            )

            # Build radar chart for career stats
            radar_fig = create_radar_chart(career_stats, stat_type, "Career Stats Profile")

            return summary_cards, comparison_table, war_fig, radar_fig

        except Exception as e:
            logger.error(f"Error in career comparison: {e}")
            return [], html.Div(f"Error: {str(e)}", className="text-danger"), empty_fig, empty_radar

    @app.callback(
        Output("formula-preview", "children"),
        Input("preview-formula-btn", "n_clicks"),
        Input("formula-mode-tabs", "active_tab"),
        State("formula-input", "value"),
        State("obp-weight-knob", "value"),
        State("slg-weight-knob", "value"),
        State("war-weight-knob", "value"),
        State("iso-weight-knob", "value"),
        State("normalize-checkbox", "value"),
        State("filtered-data-store", "data"),
    )
    def preview_formula(
        n_clicks, mode, formula_text, obp_w, slg_w, war_w, iso_w, normalize, data
    ):
        """Preview custom formula results."""
        if not data:
            return "Load data first to preview formula"

        try:
            df = pd.read_json(StringIO(data), orient="split")

            if mode == "quick-mode":
                # Weighted combination
                from baseball_stats.stats.custom_stats import FormulaEngine

                engine = FormulaEngine("batting")
                stats = ["obp", "slg", "war", "iso"]
                weights = [obp_w or 0, slg_w or 0, war_w or 0, iso_w or 0]
                result = engine.compute_weighted(stats, weights, df, normalize=normalize)
                df["custom_stat"] = result
            else:
                # Custom formula
                if not formula_text:
                    return "Enter a formula to preview"

                from baseball_stats.stats.custom_stats import FormulaEngine, CustomFormula

                engine = FormulaEngine("batting")
                formula = CustomFormula(name="preview", expression=formula_text)
                df["custom_stat"] = engine.compute(formula, df)

            # Show top 10 by custom stat
            top_10 = df.nlargest(10, "custom_stat")[["name", "team", "season", "custom_stat"]]
            top_10["custom_stat"] = top_10["custom_stat"].round(3)

            return html.Div([
                html.H6("Top 10 Players by Custom Stat"),
                html.Table(
                    [
                        html.Thead(html.Tr([html.Th(c) for c in top_10.columns])),
                        html.Tbody([
                            html.Tr([html.Td(str(v)) for v in row])
                            for row in top_10.values
                        ]),
                    ],
                    className="table table-sm",
                ),
            ])
        except Exception as e:
            return html.Div(f"Error: {str(e)}", className="text-danger")

    @app.callback(
        Output("formula-save-feedback", "children"),
        Input("save-formula-btn", "n_clicks"),
        State("formula-name-input", "value"),
        State("formula-description-input", "value"),
        State("formula-input", "value"),
        prevent_initial_call=True,
    )
    def save_formula(n_clicks, name, description, expression):
        """Save a custom formula."""
        if not name or not expression:
            return html.Div("Please provide a name and formula", className="text-warning")

        try:
            db.save_custom_formula(name, expression, description or "")
            return html.Div(f"Formula '{name}' saved successfully!", className="text-success")
        except Exception as e:
            return html.Div(f"Error saving: {str(e)}", className="text-danger")

    # Chat callbacks (only register if LLM agent is available)
    if llm_agent:
        @app.callback(
            Output("chat-history", "children"),
            Input("chat-send-btn", "n_clicks"),
            Input("chat-input", "n_submit"),
            State("chat-input", "value"),
            State("chat-history", "children"),
            State("stat-type-toggle", "value"),
            prevent_initial_call=True,
        )
        def handle_chat(n_clicks, n_submit, message, history, stat_type):
            """Handle chat messages."""
            if not message:
                raise PreventUpdate

            # Add user message to history
            history = history or []
            history.append(create_chat_message("user", message))

            try:
                # Get response from LLM
                response = llm_agent.query(message, stat_type)
                history.append(create_chat_message("assistant", response))
            except Exception as e:
                history.append(
                    create_chat_message("assistant", f"Sorry, I encountered an error: {str(e)}")
                )

            return history

        @app.callback(
            Output("chat-input", "value"),
            Input("chat-send-btn", "n_clicks"),
            Input("chat-input", "n_submit"),
            prevent_initial_call=True,
        )
        def clear_chat_input(n_clicks, n_submit):
            """Clear chat input after sending."""
            return ""
