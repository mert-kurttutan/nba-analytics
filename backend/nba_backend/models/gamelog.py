from datetime import date
from typing import Optional
from uuid import UUID, uuid4

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Field, SQLModel


def get_teamstat_type(column_name):
    if column_name == "GAME_DATE":
        return str
    elif column_name == "GAME_ID":
        return int
    else:
        return float


def is_primary_key_teamstat(x):
    return x == "GAME_ID"


class Gamelog(SQLModel, table=True):
    __tablename__ = "gamelog"

    id: Optional[UUID] = Field(
        sa_column=sa.Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            default=uuid4,
            server_default=sa.text("gen_random_uuid()"),
        ),
    )

    DAY_WITHIN_SEASON: Optional[int] = Field(nullable=False)
    GAME_DATE: Optional[date] = Field(sa_column=sa.Date(), nullable=False)
    GAME_ID: Optional[int] = Field(nullable=False)

    T1_IS_HOME: Optional[bool] = Field(nullable=False)
    T1_PLUS_MINUS: Optional[float] = Field(nullable=False)
    T1_PTS: Optional[float] = Field(nullable=False)
    T1_TEAM_ID: Optional[int] = Field(nullable=False)
    T1_TEAM_NAME: Optional[str] = Field(nullable=False)
    T1_W: Optional[float] = Field(nullable=False)
    T1_W_cum: Optional[float] = Field(nullable=False)

    T2_IS_HOME: Optional[bool] = Field(nullable=False)
    T2_PLUS_MINUS: Optional[float] = Field(nullable=False)
    T2_PTS: Optional[float] = Field(nullable=False)
    T2_TEAM_ID: Optional[int] = Field(nullable=False)
    T2_TEAM_NAME: Optional[str] = Field(nullable=False)
    T2_W: Optional[float] = Field(nullable=False)
    T2_W_cum: Optional[float] = Field(nullable=False)
