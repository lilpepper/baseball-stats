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
    )

    # Update layout for better appearance
    fig.update_layout(
        hovermode="closest",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    # Add trend line
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
