from datetime import date
from typing import Optional
from uuid import UUID, uuid4

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Field, SQLModel


class Teamstat(SQLModel, table=True):
    __tablename__ = "teamstat"

    id: Optional[UUID] = Field(
        sa_column=sa.Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            default=uuid4,
            server_default=sa.text("gen_random_uuid()"),
        ),
    )

    DAY_WITHIN_SEASON: Optional[int] = Field(nullable=False)
    GAME_DATE: Optional[date] = Field(nullable=False)
    TEAM_ID: Optional[int] = Field(nullable=False)

    lag08_GP: Optional[float] = Field(nullable=False)
    lag08_W_PCT: Optional[float] = Field(nullable=False)
    lag08_FG_PCT: Optional[float] = Field(nullable=False)
    lag08_FT_PCT: Optional[float] = Field(nullable=False)
    lag08_OREB: Optional[float] = Field(nullable=False)
    lag08_DREB: Optional[float] = Field(nullable=False)
    lag08_REB: Optional[float] = Field(nullable=False)
    lag08_AST: Optional[float] = Field(nullable=False)
    lag08_TOV: Optional[float] = Field(nullable=False)
    lag08_STL: Optional[float] = Field(nullable=False)
    lag08_BLK: Optional[float] = Field(nullable=False)
    lag08_PTS: Optional[float] = Field(nullable=False)
    lag08_PLUS_MINUS: Optional[float] = Field(nullable=False)
    lag08_W_PCT_RANK: Optional[float] = Field(nullable=False)
    lag08_PTS_RANK: Optional[float] = Field(nullable=False)
    lag08_PLUS_MINUS_RANK: Optional[float] = Field(nullable=False)

    lag16_GP: Optional[float] = Field(nullable=False)
    lag16_W_PCT: Optional[float] = Field(nullable=False)
    lag16_FG_PCT: Optional[float] = Field(nullable=False)
    lag16_FT_PCT: Optional[float] = Field(nullable=False)
    lag16_OREB: Optional[float] = Field(nullable=False)
    lag16_DREB: Optional[float] = Field(nullable=False)
    lag16_REB: Optional[float] = Field(nullable=False)
    lag16_AST: Optional[float] = Field(nullable=False)
    lag16_TOV: Optional[float] = Field(nullable=False)
    lag16_STL: Optional[float] = Field(nullable=False)
    lag16_BLK: Optional[float] = Field(nullable=False)
    lag16_PTS: Optional[float] = Field(nullable=False)
    lag16_PLUS_MINUS: Optional[float] = Field(nullable=False)
    lag16_W_PCT_RANK: Optional[float] = Field(nullable=False)
    lag16_PTS_RANK: Optional[float] = Field(nullable=False)
    lag16_PLUS_MINUS_RANK: Optional[float] = Field(nullable=False)

    lag32_GP: Optional[float] = Field(nullable=False)
    lag32_W_PCT: Optional[float] = Field(nullable=False)
    lag32_FG_PCT: Optional[float] = Field(nullable=False)
    lag32_FT_PCT: Optional[float] = Field(nullable=False)
    lag32_OREB: Optional[float] = Field(nullable=False)
    lag32_DREB: Optional[float] = Field(nullable=False)
    lag32_REB: Optional[float] = Field(nullable=False)
    lag32_AST: Optional[float] = Field(nullable=False)
    lag32_TOV: Optional[float] = Field(nullable=False)
    lag32_STL: Optional[float] = Field(nullable=False)
    lag32_BLK: Optional[float] = Field(nullable=False)
    lag32_PTS: Optional[float] = Field(nullable=False)
    lag32_PLUS_MINUS: Optional[float] = Field(nullable=False)
    lag32_W_PCT_RANK: Optional[float] = Field(nullable=False)
    lag32_PTS_RANK: Optional[float] = Field(nullable=False)
    lag32_PLUS_MINUS_RANK: Optional[float] = Field(nullable=False)

    lag64_GP: Optional[float] = Field(nullable=False)
    lag64_W_PCT: Optional[float] = Field(nullable=False)
    lag64_FG_PCT: Optional[float] = Field(nullable=False)
    lag64_FT_PCT: Optional[float] = Field(nullable=False)
    lag64_OREB: Optional[float] = Field(nullable=False)
    lag64_DREB: Optional[float] = Field(nullable=False)
    lag64_REB: Optional[float] = Field(nullable=False)
    lag64_AST: Optional[float] = Field(nullable=False)
    lag64_TOV: Optional[float] = Field(nullable=False)
    lag64_STL: Optional[float] = Field(nullable=False)
    lag64_BLK: Optional[float] = Field(nullable=False)
    lag64_PTS: Optional[float] = Field(nullable=False)
    lag64_PLUS_MINUS: Optional[float] = Field(nullable=False)
    lag64_W_PCT_RANK: Optional[float] = Field(nullable=False)
    lag64_PTS_RANK: Optional[float] = Field(nullable=False)
    lag64_PLUS_MINUS_RANK: Optional[float] = Field(nullable=False)

    lag180_GP: Optional[float] = Field(nullable=False)
    lag180_W_PCT: Optional[float] = Field(nullable=False)
    lag180_FG_PCT: Optional[float] = Field(nullable=False)
    lag180_FT_PCT: Optional[float] = Field(nullable=False)
    lag180_OREB: Optional[float] = Field(nullable=False)
    lag180_DREB: Optional[float] = Field(nullable=False)
    lag180_REB: Optional[float] = Field(nullable=False)
    lag180_AST: Optional[float] = Field(nullable=False)
    lag180_TOV: Optional[float] = Field(nullable=False)
    lag180_STL: Optional[float] = Field(nullable=False)
    lag180_BLK: Optional[float] = Field(nullable=False)
    lag180_PTS: Optional[float] = Field(nullable=False)
    lag180_PLUS_MINUS: Optional[float] = Field(nullable=False)
    lag180_W_PCT_RANK: Optional[float] = Field(nullable=False)
    lag180_PTS_RANK: Optional[float] = Field(nullable=False)
    lag180_PLUS_MINUS_RANK: Optional[float] = Field(nullable=False)
