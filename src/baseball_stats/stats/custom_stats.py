"""Custom statistics formula engine."""

import logging
from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd

from .validators import BATTING_STATS, PITCHING_STATS, FormulaValidator

logger = logging.getLogger(__name__)


@dataclass
class CustomFormula:
    """Represents a user-defined custom statistic."""

    name: str
    expression: str
    description: str = ""
    created_by: str = "user"


class FormulaEngine:
    """Engine for parsing and computing custom stat formulas."""

    # Built-in formulas
    BUILTIN_FORMULAS = [
        CustomFormula(
            name="OPS_Plus_Custom",
            expression="(obp * 1.8) + slg",
            description="OPS with higher OBP weighting (OBP valued 1.8x more)",
            created_by="system",
        ),
        CustomFormula(
            name="Power_Speed",
            expression="(hr * 2) + sb",
            description="Combined power and speed metric",
            created_by="system",
        ),
        CustomFormula(
            name="Plate_Discipline",
            expression="bb_pct - k_pct",
            description="Walk rate minus strikeout rate (higher = more disciplined)",
            created_by="system",
        ),
        CustomFormula(
            name="WAR_per_600PA",
            expression="(war / pa) * 600",
            description="WAR normalized to 600 plate appearances",
            created_by="system",
        ),
        CustomFormula(
            name="Contact_Quality",
            expression="(avg + babip) / 2 + iso",
            description="Combined contact and power quality metric",
            created_by="system",
        ),
        CustomFormula(
            name="Run_Production",
            expression="runs + rbi - hr",
            description="Total runs produced (avoiding double-counting HR)",
            created_by="system",
        ),
    ]

    def __init__(self, stat_type: str = "batting"):
        """
        Initialize the formula engine.

        Args:
            stat_type: 'batting' or 'pitching'
        """
        self.stat_type = stat_type
        available_stats = BATTING_STATS if stat_type == "batting" else PITCHING_STATS
        self.validator = FormulaValidator(available_stats)
        self._custom_formulas: dict[str, CustomFormula] = {}
        self._load_builtin_formulas()

    def _load_builtin_formulas(self):
        """Load built-in formulas."""
        for formula in self.BUILTIN_FORMULAS:
            self._custom_formulas[formula.name] = formula

    def create_formula(
        self,
        name: str,
        expression: str,
        description: str = "",
    ) -> CustomFormula:
        """
        Create and validate a new custom formula.

        Args:
            name: Unique name for the formula
            expression: Mathematical expression using stat names
            description: Human-readable description

        Returns:
            The created CustomFormula

        Raises:
            ValueError: If formula is invalid
        """
        # Validate expression
        validation = self.validator.validate(expression)
        if not validation.is_valid:
            raise ValueError(f"Invalid formula: {validation.error}")

        formula = CustomFormula(
            name=name,
            expression=expression,
            description=description,
            created_by="user",
        )
        self._custom_formulas[name] = formula
        logger.info(f"Created formula '{name}': {expression}")
        return formula

    def compute(self, formula: CustomFormula, data: pd.DataFrame) -> pd.Series:
        """
        Compute custom stat for a DataFrame.

        Args:
            formula: The formula to compute
            data: DataFrame with stat columns

        Returns:
            Series with computed values
        """
        # Prepare expression with DataFrame column references
        expr = formula.expression.lower()

        # Create a copy of data with lowercase columns for evaluation
        eval_data = data.copy()
        eval_data.columns = [c.lower() for c in eval_data.columns]

        try:
            # Use pandas eval for safe computation
            result = eval_data.eval(expr)
            return result
        except Exception as e:
            logger.error(f"Error computing formula '{formula.name}': {e}")
            return pd.Series(np.nan, index=data.index)

    def compute_by_name(self, formula_name: str, data: pd.DataFrame) -> pd.Series:
        """Compute a formula by its name."""
        formula = self.get_formula(formula_name)
        if formula is None:
            raise ValueError(f"Formula not found: {formula_name}")
        return self.compute(formula, data)

    def compute_weighted(
        self,
        stats: list[str],
        weights: list[float],
        data: pd.DataFrame,
        normalize: bool = True,
    ) -> pd.Series:
        """
        Compute weighted combination of stats.

        Args:
            stats: List of stat column names
            weights: Corresponding weights for each stat
            data: DataFrame with stat columns
            normalize: Whether to normalize stats to 0-1 range before weighting

        Returns:
            Series with weighted combination
        """
        if len(stats) != len(weights):
            raise ValueError("Number of stats must match number of weights")

        result = pd.Series(0.0, index=data.index)
        data_lower = data.copy()
        data_lower.columns = [c.lower() for c in data_lower.columns]

        for stat, weight in zip(stats, weights):
            stat_lower = stat.lower()
            if stat_lower in data_lower.columns:
                col = data_lower[stat_lower]
                if normalize and col.max() != col.min():
                    # Normalize to 0-1 range
                    col = (col - col.min()) / (col.max() - col.min())
                result += col * weight

        return result

    def get_formula(self, name: str) -> Optional[CustomFormula]:
        """Get a formula by name."""
        return self._custom_formulas.get(name)

    def list_formulas(self) -> list[CustomFormula]:
        """List all available formulas."""
        return list(self._custom_formulas.values())

    def list_builtin_formulas(self) -> list[CustomFormula]:
        """List only built-in formulas."""
        return [f for f in self._custom_formulas.values() if f.created_by == "system"]

    def list_user_formulas(self) -> list[CustomFormula]:
        """List only user-created formulas."""
        return [f for f in self._custom_formulas.values() if f.created_by == "user"]

    def delete_formula(self, name: str) -> bool:
        """Delete a user formula (cannot delete built-ins)."""
        formula = self._custom_formulas.get(name)
        if formula is None:
            return False
        if formula.created_by == "system":
            raise ValueError("Cannot delete built-in formulas")
        del self._custom_formulas[name]
        return True

    def get_available_stats(self) -> list[str]:
        """Get list of stats available for formulas."""
        return BATTING_STATS if self.stat_type == "batting" else PITCHING_STATS
