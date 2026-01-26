"""Chart and visualization components."""

from dash import dash_table, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def create_scatter_plot(
    data: pd.DataFrame = None,
    x_col: str = "obp",
    y_col: str = "war",
    color_col: str = None,
    size_col: str = None,
    hover_name: str = "name",
    title: str = "Player Statistics",
    highlighted_players: list = None,
):
    """
    Create an interactive scatter plot.

    Args:
        data: DataFrame with player statistics
        x_col: Column for x-axis
        y_col: Column for y-axis
        color_col: Column for color encoding
        size_col: Column for size encoding
        hover_name: Column for hover labels
        title: Chart title
        highlighted_players: List of player IDfg values to highlight on the chart

    Returns:
        Plotly figure
    """
    if data is None or len(data) == 0:
        # Return empty figure with message
        fig = go.Figure()
        fig.add_annotation(
            text="No data to display. Adjust filters to see results.",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16),
        )
        fig.update_layout(
            title=title,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
        )
        return fig

    # Bright, saturated colors for highlighted players (high contrast)
    highlight_colors = [
        "#FF0000",  # Bright Red
        "#00FF00",  # Bright Green
        "#FF00FF",  # Magenta
        "#FFD700",  # Gold
        "#00FFFF",  # Cyan
        "#FF6B00",  # Bright Orange
        "#0080FF",  # Bright Blue
        "#FF1493",  # Deep Pink
    ]

    # If players are highlighted, add a column for coloring
    # Use IDfg for matching (handles duplicate names), fall back to name
    if highlighted_players and "IDfg" in data.columns:
        data = data.copy()
        # Convert IDfg to string for comparison
        highlighted_ids = [str(p) for p in highlighted_players]

        def get_highlight_group(row):
            if str(row["IDfg"]) in highlighted_ids:
                return row["name"]  # Use player name for legend display
            return "Other Players"

        data["_highlight"] = data.apply(get_highlight_group, axis=1)
        color_col = "_highlight"

        # Build color map - map player names to colors
        color_map = {"Other Players": "#d0d0d0"}  # Light gray for others
        # Get unique highlighted player names for color assignment
        highlighted_names = data[data["_highlight"] != "Other Players"]["_highlight"].unique()
        for i, player_name in enumerate(highlighted_names):
            color_map[player_name] = highlight_colors[i % len(highlight_colors)]
    elif highlighted_players and "name" in data.columns:
        # Fallback to name-based matching if no IDfg
        data = data.copy()

        def get_highlight_group(name):
            if name in highlighted_players:
                return name
            return "Other Players"

        data["_highlight"] = data["name"].apply(get_highlight_group)
        color_col = "_highlight"

        color_map = {"Other Players": "#d0d0d0"}
        for i, player in enumerate(highlighted_players):
            color_map[player] = highlight_colors[i % len(highlight_colors)]
    else:
        color_map = None

    # Build scatter plot
    fig = px.scatter(
        data,
        x=x_col,
        y=y_col,
        color=color_col,
        size=size_col,
        hover_name=hover_name,
        hover_data=["team", "season", "war"],
        custom_data=["name"],  # Include player name for click events
        title=title,
        template="plotly_white",
        color_discrete_map=color_map,
    )

    # Update layout for better appearance
    fig.update_layout(
        hovermode="closest",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    # If players are highlighted, make their points much larger and more visible
    if highlighted_players and color_map:
        for trace in fig.data:
            # Trace names are player names (from _highlight column), not IDfg
            # Check if trace is a highlighted player (not "Other Players")
            if trace.name != "Other Players" and trace.name in color_map:
                trace.marker.size = 22  # Much bigger
                trace.marker.opacity = 1.0
                trace.marker.line = dict(width=3, color="black")  # Thicker outline
                trace.marker.symbol = "circle"
            else:
                trace.marker.opacity = 0.15  # Very faded
                trace.marker.size = 5  # Smaller
                trace.marker.line = dict(width=0)  # No outline
    else:
        fig.update_traces(marker=dict(opacity=0.7, line=dict(width=1, color="DarkSlateGrey")))

    return fig


def create_leaderboard_table(
    data: pd.DataFrame = None,
    columns: list[str] = None,
    page_size: int = 15,
):
    """
    Create a sortable leaderboard table.

    Args:
        data: DataFrame with player statistics
        columns: List of columns to display
        page_size: Number of rows per page

    Returns:
        Dash DataTable component
    """
    if columns is None:
        columns = ["name", "team", "season", "war", "avg", "obp", "slg", "hr", "rbi"]

    # Filter to existing columns
    if data is not None:
        columns = [c for c in columns if c in data.columns]
        display_data = data[columns].to_dict("records")
    else:
        display_data = []

    # Column display names
    column_names = {
        "name": "Player",
        "team": "Team",
        "season": "Year",
        "war": "WAR",
        "avg": "AVG",
        "obp": "OBP",
        "slg": "SLG",
        "ops": "OPS",
        "hr": "HR",
        "rbi": "RBI",
        "runs": "R",
        "sb": "SB",
        "wrc_plus": "wRC+",
        "era": "ERA",
        "whip": "WHIP",
        "fip": "FIP",
        "wins": "W",
        "saves": "SV",
        "k": "K",
        "ip": "IP",
    }

    return dash_table.DataTable(
        id="stats-table",
        columns=[{"name": column_names.get(c, c.upper()), "id": c} for c in columns],
        data=display_data,
        page_size=page_size,
        sort_action="native",
        sort_mode="multi",
        filter_action="native",
        style_table={"overflowX": "auto"},
        style_cell={
            "textAlign": "left",
            "padding": "8px",
            "minWidth": "60px",
        },
        style_header={
            "backgroundColor": "#f8f9fa",
            "fontWeight": "bold",
            "borderBottom": "2px solid #dee2e6",
        },
        style_data_conditional=[
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "#f8f9fa",
            },
            {
                "if": {"column_id": "war"},
                "fontWeight": "bold",
            },
        ],
    )


def create_bar_chart(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str = "Statistics",
    orientation: str = "v",
    color: str = "#0074D9",
):
    """
    Create a bar chart.

    Args:
        data: DataFrame with data
        x_col: Column for categories
        y_col: Column for values
        title: Chart title
        orientation: 'v' for vertical, 'h' for horizontal
        color: Bar color

    Returns:
        Plotly figure
    """
    fig = px.bar(
        data,
        x=x_col if orientation == "v" else y_col,
        y=y_col if orientation == "v" else x_col,
        orientation=orientation,
        title=title,
        template="plotly_white",
        color_discrete_sequence=[color],
    )

    fig.update_layout(
        xaxis_title=x_col.upper() if orientation == "v" else y_col.upper(),
        yaxis_title=y_col.upper() if orientation == "v" else x_col.upper(),
    )

    return fig


def create_line_chart(
    data: pd.DataFrame,
    x_col: str = "season",
    y_col: str = "war",
    color_col: str = "name",
    title: str = "Stat Trend Over Time",
):
    """
    Create a line chart for trend analysis.

    Args:
        data: DataFrame with data
        x_col: Column for x-axis (typically season/year)
        y_col: Column for y-axis
        color_col: Column for line colors
        title: Chart title

    Returns:
        Plotly figure
    """
    fig = px.line(
        data,
        x=x_col,
        y=y_col,
        color=color_col,
        title=title,
        template="plotly_white",
        markers=True,
    )

    fig.update_layout(
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )

    return fig


def create_radar_chart(
    players_stats: dict[str, dict],
    stat_type: str = "batting",
    title: str = "Player Comparison",
):
    """
    Create a radar/spider chart comparing multiple players across stats.

    Args:
        players_stats: Dict mapping player names to their stat dicts
                      e.g., {"Player A": {"war": 5, "avg": 0.300, ...}, ...}
        stat_type: 'batting' or 'pitching' to determine which stats to show
        title: Chart title

    Returns:
        Plotly figure with radar chart
    """
    if not players_stats:
        fig = go.Figure()
        fig.add_annotation(
            text="No data to display",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False, font=dict(size=16)
        )
        return fig

    # Define stats to include in radar chart (normalized to 0-100 scale)
    if stat_type == "batting":
        # Stats where higher is better, with typical max values for normalization
        stats_config = {
            "war": {"label": "WAR", "max": 10, "invert": False},
            "avg": {"label": "AVG", "max": 0.350, "invert": False},
            "obp": {"label": "OBP", "max": 0.450, "invert": False},
            "slg": {"label": "SLG", "max": 0.600, "invert": False},
            "hr": {"label": "HR", "max": 50, "invert": False},
            "sb": {"label": "SB", "max": 50, "invert": False},
        }
    else:
        # Pitching stats - some are inverted (lower is better)
        stats_config = {
            "war": {"label": "WAR", "max": 8, "invert": False},
            "era": {"label": "ERA", "max": 5.0, "invert": True},  # Lower is better
            "whip": {"label": "WHIP", "max": 1.5, "invert": True},  # Lower is better
            "k_per_9": {"label": "K/9", "max": 12, "invert": False},
            "wins": {"label": "W", "max": 20, "invert": False},
            "saves": {"label": "SV", "max": 40, "invert": False},
        }

    categories = [cfg["label"] for cfg in stats_config.values()]
    stat_keys = list(stats_config.keys())

    fig = go.Figure()

    colors = px.colors.qualitative.Set2

    for i, (player_name, stats) in enumerate(players_stats.items()):
        values = []
        for key in stat_keys:
            cfg = stats_config[key]
            raw_value = stats.get(key, 0) or 0

            # Normalize to 0-100 scale
            if cfg["invert"]:
                # For stats where lower is better (ERA, WHIP)
                # A value of 0 should be 100, a value of max should be 0
                normalized = max(0, min(100, (1 - raw_value / cfg["max"]) * 100))
            else:
                normalized = max(0, min(100, (raw_value / cfg["max"]) * 100))

            values.append(normalized)

        # Close the radar chart by repeating first value
        values.append(values[0])
        cats = categories + [categories[0]]

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=cats,
            fill='toself',
            name=player_name,
            line=dict(color=colors[i % len(colors)]),
            fillcolor=colors[i % len(colors)],
            opacity=0.6,
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                ticksuffix="",
            )
        ),
        showlegend=True,
        title=title,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
    )

    return fig


def create_chart_container():
    """
    Create the main chart container component.

    Returns:
        Dash component with loading wrapper and chart
    """
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    dcc.Loading(
                        id="chart-loading",
                        type="circle",
                        children=[
                            dcc.Graph(
                                id="main-scatter-plot",
                                config={
                                    "displayModeBar": True,
                                    "modeBarButtonsToRemove": ["lasso2d", "select2d"],
                                },
                                style={"height": "500px"},
                            )
                        ],
                    )
                ]
            )
        ],
        className="mb-3",
    )


def create_table_container():
    """
    Create the leaderboard table container.

    Returns:
        Dash component with table
    """
    return dbc.Card(
        [
            dbc.CardHeader("Leaderboard"),
            dbc.CardBody(
                [
                    dcc.Loading(
                        id="table-loading",
                        type="circle",
                        children=[html.Div(id="table-container")],
                    )
                ]
            ),
        ],
        className="mb-3",
    )
