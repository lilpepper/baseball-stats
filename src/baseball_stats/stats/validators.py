"""Formula validation for custom statistics."""

import ast
import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ValidationResult:
    """Result of formula validation."""

    is_valid: bool
    error: Optional[str] = None
    used_stats: list[str] = field(default_factory=list)


class FormulaValidator:
    """Validates custom formula expressions for safety and correctness."""

    # Allowed mathematical operators and functions
    ALLOWED_OPERATORS = {"+", "-", "*", "/", "(", ")", ".", ","}
    ALLOWED_FUNCTIONS = {"abs", "sqrt", "log", "min", "max", "pow", "round"}

    # Patterns that could indicate code injection attempts
    DANGEROUS_PATTERNS = [
        "import",
        "__",
        "eval",
        "exec",
        "open",
        "file",
        "os.",
        "sys.",
        "subprocess",
        "lambda",
        "def ",
        "class ",
        "global",
        "locals",
        "globals",
    ]

    def __init__(self, available_stats: list[str]):
        """
        Initialize validator with available stat names.

        Args:
            available_stats: List of valid statistic column names
        """
        self.available_stats = set(s.lower() for s in available_stats)

    def validate(self, expression: str) -> ValidationResult:
        """
        Validate a formula expression.

        Args:
            expression: The formula expression to validate

        Returns:
            ValidationResult with is_valid flag and any errors
        """
        if not expression or not expression.strip():
            return ValidationResult(is_valid=False, error="Expression cannot be empty")

        # Check for dangerous patterns
        if self._has_dangerous_patterns(expression):
            return ValidationResult(
                is_valid=False,
                error="Expression contains disallowed patterns",
            )

        # Extract stat references
        stats_used = self._extract_stats(expression)

        # Check all stats exist (case-insensitive)
        stats_lower = {s.lower() for s in stats_used}
        unknown_stats = stats_lower - self.available_stats - set(
            f.lower() for f in self.ALLOWED_FUNCTIONS
        )

        if unknown_stats:
            return ValidationResult(
                is_valid=False,
                error=f"Unknown statistics: {', '.join(unknown_stats)}",
            )

        # Try to parse expression
        if not self._is_syntactically_valid(expression):
            return ValidationResult(
                is_valid=False,
                error="Invalid syntax - check parentheses and operators",
            )

        return ValidationResult(
            is_valid=True,
            used_stats=list(stats_used),
        )

    def _has_dangerous_patterns(self, expr: str) -> bool:
        """Check for code injection patterns."""
        expr_lower = expr.lower()
        return any(pattern in expr_lower for pattern in self.DANGEROUS_PATTERNS)

    def _extract_stats(self, expr: str) -> set[str]:
        """Extract stat variable names from expression."""
        # Match word characters that could be stat names
        tokens = re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*\b", expr)
        # Filter out numeric literals and functions
        return {
            t for t in tokens if t.lower() not in {f.lower() for f in self.ALLOWED_FUNCTIONS}
        }

    def _is_syntactically_valid(self, expr: str) -> bool:
        """Check if expression is syntactically valid Python."""
        try:
            # Replace stat names with dummy numeric values for parsing
            test_expr = re.sub(r"\b[A-Za-z_][A-Za-z0-9_]*\b", "1.0", expr)
            ast.parse(test_expr, mode="eval")
            return True
        except SyntaxError:
            return False


# Common batting stats for formula building
BATTING_STATS = [
    "avg",
    "obp",
    "slg",
    "ops",
    "woba",
    "wrc_plus",
    "war",
    "iso",
    "babip",
    "hr",
    "rbi",
    "runs",
    "sb",
    "bb",
    "k",
    "hits",
    "ab",
    "pa",
    "games",
    "bb_pct",
    "k_pct",
]

# Common pitching stats for formula building
PITCHING_STATS = [
    "era",
    "whip",
    "fip",
    "xfip",
    "war",
    "k_per_9",
    "bb_per_9",
    "hr_per_9",
    "k_pct",
    "bb_pct",
    "wins",
    "losses",
    "saves",
    "ip",
    "k",
    "bb",
    "hr",
    "games",
    "games_started",
]
