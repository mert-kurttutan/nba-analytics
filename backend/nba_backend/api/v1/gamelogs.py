"""REST API that provides speech transcription
in the form json response
There is no authorization as it is. If it is needed, please specify
"""
from datetime import date
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from nba_backend.api import deps
from nba_backend.gamelog_repository import GamelogRepository
from nba_backend.models import ApiClient
from nba_backend.schemas import protocol

router = APIRouter()


@router.get("/by_team_date", response_model=list[protocol.Gamelog])
def get_gamelog_team_date(
    api_client_id: Optional[UUID] = None,
    team1: str = "Cleveland Cavaliers",
    team2: str = "New York Knicks",
    date: date = "2016-10-26",
    max_count: int = Query(1, gt=0, le=10000),
    desc: bool = False,
    api_client: ApiClient = Depends(deps.get_api_client),
    db: Session = Depends(deps.get_db),
):
    gr = GamelogRepository(db, api_client)
    gamelogs = gr.query_gamelog_by_team_date(
        api_client_id=api_client_id,
        team1=team1,
        team2=team2,
        date=date,
        limit=max_count,
        desc=desc,
    )
    return [protocol.Gamelog(**glog.dict()) for glog in gamelogs]
