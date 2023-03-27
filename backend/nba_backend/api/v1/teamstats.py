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
from nba_backend.models import ApiClient
from nba_backend.schemas import protocol
from nba_backend.teamstat_repository import TeamstatRepository

router = APIRouter()


@router.get("/by_team_date", response_model=list[protocol.Teamstat])
def get_teamstat_team_date(
    api_client_id: Optional[UUID] = None,
    team_name: str = "Cleveland Cavaliers",
    date: date = "2016-10-26",
    max_count: int = Query(1, gt=0, le=10000),
    desc: bool = False,
    api_client: ApiClient = Depends(deps.get_api_client),
    db: Session = Depends(deps.get_db),
):
    tsr = TeamstatRepository(db, api_client)
    teamstats = tsr.query_teamstat_by_date_team(
        api_client_id=api_client_id,
        team_name=team_name,
        date=date,
        limit=max_count,
        desc=desc,
    )
    return [protocol.Teamstat(**glog.dict()) for glog in teamstats]
