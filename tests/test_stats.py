"""Tests for the custom statistics engine."""

import pytest
import pandas as pd

from baseball_stats.stats.validators import FormulaValidator, BATTING_STATS
from baseball_stats.stats.custom_stats import FormulaEngine, CustomFormula


class TestFormulaValidator:
    """Tests for FormulaValidator."""

    @pytest.fixture
    def validator(self):
        return FormulaValidator(BATTING_STATS)

    def test_valid_simple_expression(self, validator):
        result = validator.validate("obp + slg")
        assert result.is_valid
        assert "obp" in result.used_stats
        assert "slg" in result.used_stats

    def test_valid_complex_expression(self, validator):
        result = validator.validate("(obp * 1.8) + slg - (k_pct * 0.5)")
        assert result.is_valid

    def test_invalid_unknown_stat(self, validator):
        result = validator.validate("obp + xyz")
        assert not result.is_valid
        assert "Unknown" in result.error

    def test_invalid_dangerous_pattern(self, validator):
        result = validator.validate("import os; obp")
        assert not result.is_valid
        assert "disallowed" in result.error.lower()

    def test_invalid_syntax(self, validator):
        result = validator.validate("obp + + slg")
        assert not result.is_valid

    def test_empty_expression(self, validator):
        result = validator.validate("")
        assert not result.is_valid
        assert "empty" in result.error.lower()

    def test_functions_allowed(self, validator):
        result = validator.validate("abs(war) + sqrt(hr)")
        assert result.is_valid


class TestFormulaEngine:
    """Tests for FormulaEngine."""

    @pytest.fixture
    def engine(self):
        return FormulaEngine("batting")

    def test_create_valid_formula(self, engine):
        formula = engine.create_formula(
            name="test_formula",
            expression="obp + slg",
            description="Test formula",
        )
        assert formula.name == "test_formula"
        assert formula.expression == "obp + slg"

    def test_create_invalid_formula(self, engine):
        with pytest.raises(ValueError):
            engine.create_formula(
                name="bad_formula",
                expression="import os",
            )

    def test_compute_formula(self, engine, sample_batting_data):
        formula = CustomFormula(
            name="custom_ops",
            expression="obp + slg",
        )
        result = engine.compute(formula, sample_batting_data)

        # OPS should equal OBP + SLG
        expected = sample_batting_data["obp"] + sample_batting_data["slg"]
        pd.testing.assert_series_equal(result, expected, check_names=False)

    def test_compute_weighted(self, engine, sample_batting_data):
        stats = ["obp", "slg"]
        weights = [1.0, 1.0]
        result = engine.compute_weighted(stats, weights, sample_batting_data)

        assert len(result) == len(sample_batting_data)
        assert result.min() >= 0
        assert result.max() <= 2.0  # Normalized weights

    def test_builtin_formulas_exist(self, engine):
        formulas = engine.list_builtin_formulas()
        assert len(formulas) > 0
        assert any(f.name == "OPS_Plus_Custom" for f in formulas)

    def test_get_formula(self, engine):
        formula = engine.get_formula("OPS_Plus_Custom")
        assert formula is not None
        assert formula.name == "OPS_Plus_Custom"

    def test_delete_user_formula(self, engine):
        engine.create_formula("to_delete", "obp + slg")
        assert engine.get_formula("to_delete") is not None

        result = engine.delete_formula("to_delete")
        assert result is True
        assert engine.get_formula("to_delete") is None

    def test_cannot_delete_builtin(self, engine):
        with pytest.raises(ValueError):
            engine.delete_formula("OPS_Plus_Custom")
