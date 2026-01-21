"""Chat panel component for LLM interaction."""

from dash import dcc, html
import dash_bootstrap_components as dbc


def create_chat_panel():
    """
    Create the LLM chat interface for natural language queries.

    Returns:
        Dash Bootstrap Card component
    """
    return dbc.Card(
        [
            dbc.CardHeader(
                [
                    html.H5("Baseball AI Assistant", className="mb-0"),
                    html.Small(
                        "Ask questions about players, stats, and historical data",
                        className="text-muted",
                    ),
                ]
            ),
            dbc.CardBody(
                [
                    # Chat history display
                    html.Div(
                        id="chat-history",
                        style={
                            "height": "400px",
                            "overflowY": "auto",
                            "border": "1px solid #dee2e6",
                            "borderRadius": "4px",
                            "padding": "15px",
                            "marginBottom": "15px",
                            "backgroundColor": "#f8f9fa",
                        },
                        children=[
                            _create_message(
                                "assistant",
                                "Hello! I'm your baseball statistics assistant. "
                                "Ask me anything about players, stats, or historical data. "
                                "For example:\n\n"
                                "- Who had the highest WAR in 2023?\n"
                                "- Compare Mike Trout and Mookie Betts\n"
                                "- What does wRC+ mean?",
                            )
                        ],
                    ),
                    # Example questions accordion
                    dbc.Accordion(
                        [
                            dbc.AccordionItem(
                                [
                                    dbc.ListGroup(
                                        [
                                            dbc.ListGroupItem(
                                                q,
                                                action=True,
                                                id={"type": "example-question", "index": i},
                                                className="py-2",
                                            )
                                            for i, q in enumerate(EXAMPLE_QUESTIONS)
                                        ],
                                        flush=True,
                                    )
                                ],
                                title="Example Questions",
                            )
                        ],
                        start_collapsed=True,
                        className="mb-3",
                    ),
                    # Input area
                    dbc.InputGroup(
                        [
                            dbc.Textarea(
                                id="chat-input",
                                placeholder="Ask about baseball statistics...",
                                style={"height": "60px", "resize": "none"},
                                n_submit=0,
                            ),
                            dbc.Button(
                                "Send",
                                id="chat-send-btn",
                                color="primary",
                                className="ms-2",
                                style={"height": "60px"},
                            ),
                        ]
                    ),
                    # Loading indicator
                    dcc.Loading(
                        id="chat-loading",
                        type="dots",
                        children=[html.Div(id="chat-loading-output")],
                    ),
                ]
            ),
        ],
        className="mb-3",
    )


EXAMPLE_QUESTIONS = [
    "Who had the highest WAR in 2023?",
    "Compare Mike Trout and Mookie Betts over the last 5 years",
    "What players had 40+ home runs and 20+ stolen bases in the same season?",
    "Explain what wRC+ means",
    "Find pitchers with ERA under 3.00 and 200+ strikeouts",
    "Who are the top 10 players by career WAR?",
    "What was Shohei Ohtani's best season?",
    "Show me the most underrated players (high WAR, low recognition)",
]


def _create_message(role: str, content: str):
    """
    Create a chat message component.

    Args:
        role: 'user' or 'assistant'
        content: Message text

    Returns:
        Dash component for the message
    """
    is_user = role == "user"

    return html.Div(
        [
            html.Div(
                [
                    html.Strong("You" if is_user else "Assistant"),
                    html.Span(
                        content,
                        style={"whiteSpace": "pre-wrap"},
                        className="d-block mt-1",
                    ),
                ],
                className=f"p-2 rounded {'bg-primary text-white' if is_user else 'bg-white border'}",
                style={"maxWidth": "85%"},
            )
        ],
        className=f"d-flex {'justify-content-end' if is_user else 'justify-content-start'} mb-2",
    )


def create_chat_message(role: str, content: str):
    """Public function to create chat messages (used by callbacks)."""
    return _create_message(role, content)


def create_chat_config_panel():
    """
    Create configuration panel for chat settings.

    Returns:
        Dash component with chat settings
    """
    return dbc.Card(
        [
            dbc.CardHeader("Chat Settings"),
            dbc.CardBody(
                [
                    dbc.Label("Context"),
                    dbc.RadioItems(
                        id="chat-context-toggle",
                        options=[
                            {"label": "Batting Stats", "value": "batting"},
                            {"label": "Pitching Stats", "value": "pitching"},
                            {"label": "Both", "value": "both"},
                        ],
                        value="batting",
                        inline=True,
                        className="mb-3",
                    ),
                    dbc.Label("Response Style"),
                    dbc.RadioItems(
                        id="chat-style-toggle",
                        options=[
                            {"label": "Concise", "value": "concise"},
                            {"label": "Detailed", "value": "detailed"},
                        ],
                        value="concise",
                        inline=True,
                    ),
                ]
            ),
        ],
        className="mb-3",
    )
