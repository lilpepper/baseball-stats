"""Pydantic models for data validation."""

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class Player(BaseModel):
    """Player biographical information."""

    player_id: str
    name_first: str
    name_last: str
    birth_date: Optional[date] = None
    debut: Optional[date] = None
    final_game: Optional[date] = None

    @property
    def full_name(self) -> str:
        return f"{self.name_first} {self.name_last}"


class BattingStats(BaseModel):
    """Single season batting statistics."""

    name: str
    season: int
    team: str
    games: int = Field(ge=0)
    pa: int = Field(ge=0, description="Plate appearances")
    ab: int = Field(ge=0, description="At bats")
    hits: int = Field(ge=0)
    hr: int = Field(ge=0, description="Home runs")
    rbi: int = Field(ge=0, description="Runs batted in")
    runs: int = Field(ge=0)
    sb: int = Field(ge=0, description="Stolen bases")
    bb: int = Field(ge=0, description="Walks")
    k: int = Field(ge=0, description="Strikeouts")
    avg: float = Field(ge=0, le=1, description="Batting average")
    obp: float = Field(ge=0, le=1, description="On-base percentage")
    slg: float = Field(ge=0, le=2, description="Slugging percentage")
    ops: float = Field(ge=0, le=3, description="On-base plus slugging")
    war: float = Field(description="Wins above replacement")
    wrc_plus: Optional[int] = Field(None, description="wRC+ (100 = league average)")
    woba: Optional[float] = Field(None, description="Weighted on-base average")
    iso: Optional[float] = Field(None, description="Isolated power")
    babip: Optional[float] = Field(None, description="Batting avg on balls in play")


class PitchingStats(BaseModel):
    """Single season pitching statistics."""

    name: str
    season: int
    team: str
    wins: int = Field(ge=0)
    losses: int = Field(ge=0)
    era: float = Field(ge=0, description="Earned run average")
    whip: float = Field(ge=0, description="Walks + hits per inning")
    games: int = Field(ge=0)
    games_started: int = Field(ge=0)
    ip: float = Field(ge=0, description="Innings pitched")
    k: int = Field(ge=0, description="Strikeouts")
    bb: int = Field(ge=0, description="Walks")
    hr: int = Field(ge=0, description="Home runs allowed")
    saves: int = Field(ge=0)
    war: float = Field(description="Wins above replacement")
    fip: Optional[float] = Field(None, description="Fielding independent pitching")
    xfip: Optional[float] = Field(None, description="Expected FIP")
    k_per_9: Optional[float] = Field(None, description="Strikeouts per 9 innings")
    bb_per_9: Optional[float] = Field(None, description="Walks per 9 innings")


class CustomFormula(BaseModel):
    """User-defined custom statistic formula."""

    name: str = Field(..., min_length=1, max_length=50)
    expression: str = Field(..., min_length=1)
    description: str = ""
    created_by: str = "user"
