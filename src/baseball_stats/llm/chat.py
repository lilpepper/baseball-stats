"""Chat session management for LLM interaction."""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class ChatMessage:
    """Represents a single chat message."""

    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)


class ChatSession:
    """Manages a chat session with the LLM assistant."""

    # Keywords that indicate pitching context
    PITCHING_KEYWORDS = [
        "pitcher",
        "pitching",
        "era",
        "whip",
        "strikeout",
        "wins",
        "losses",
        "saves",
        "innings",
        "fip",
        "xfip",
        "k/9",
        "bb/9",
        "starter",
        "reliever",
        "closer",
    ]

    def __init__(self, agent: "BaseballLLMAgent"):
        """
        Initialize a chat session.

        Args:
            agent: BaseballLLMAgent instance
        """
        self.agent = agent
        self.history: list[ChatMessage] = []
        self.context: dict = {}

    def send_message(self, content: str) -> ChatMessage:
        """
        Send a message and get a response.

        Args:
            content: User message text

        Returns:
            Assistant's response as ChatMessage
        """
        # Add user message to history
        user_msg = ChatMessage(role="user", content=content)
        self.history.append(user_msg)

        # Detect stat type from context
        stat_type = self._detect_stat_type(content)

        # Get response from agent
        try:
            response_text = self.agent.query(content, stat_type)
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            response_text = f"I'm sorry, I encountered an error: {str(e)}"

        # Add assistant message to history
        assistant_msg = ChatMessage(
            role="assistant",
            content=response_text,
            metadata={"stat_type": stat_type},
        )
        self.history.append(assistant_msg)

        return assistant_msg

    def _detect_stat_type(self, query: str) -> str:
        """
        Detect if query is about batting or pitching.

        Args:
            query: User's question

        Returns:
            'batting' or 'pitching'
        """
        query_lower = query.lower()

        for keyword in self.PITCHING_KEYWORDS:
            if keyword in query_lower:
                return "pitching"

        return "batting"

    def get_history(self) -> list[ChatMessage]:
        """Get full chat history."""
        return self.history

    def get_last_n_messages(self, n: int) -> list[ChatMessage]:
        """Get the last n messages."""
        return self.history[-n:] if len(self.history) >= n else self.history

    def clear_history(self):
        """Clear chat history."""
        self.history = []
        logger.info("Chat history cleared")

    def export_history(self) -> list[dict]:
        """Export history as list of dicts for serialization."""
        return [
            {
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
                "metadata": msg.metadata,
            }
            for msg in self.history
        ]


def create_welcome_message() -> str:
    """Create a welcome message for new chat sessions."""
    return """Hello! I'm your baseball statistics assistant. I can help you with:

**Questions I can answer:**
- "Who had the highest WAR in 2023?"
- "Compare Mike Trout and Mookie Betts"
- "What players hit 40+ home runs last year?"
- "Explain what wRC+ means"
- "Find pitchers with ERA under 3.00"

**Tips:**
- I'll automatically detect if you're asking about batting or pitching
- For best results, be specific about years or time periods
- Ask me to explain any stats you're unfamiliar with

What would you like to know about baseball?"""
