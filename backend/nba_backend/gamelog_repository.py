from datetime import date
from typing import Optional
from uuid import UUID

from sqlmodel import Session, and_
from starlette.status import HTTP_403_FORBIDDEN

from nba_backend.exceptions import NBAError, NBAErrorCode
from nba_backend.models import ApiClient, Gamelog

name_to_id = {
    "Cleveland Cavaliers": 1610612739,
    "Portland Trail Blazers": 1610612757,
    "Golden State Warriors": 1610612744,
    "Miami Heat": 1610612748,
    "Dallas Mavericks": 1610612742,
    "Boston Celtics": 1610612738,
    "Toronto Raptors": 1610612761,
    "Milwaukee Bucks": 1610612749,
    "Minnesota Timberwolves": 1610612750,
    "New Orleans Pelicans": 1610612740,
    "Philadelphia 76ers": 1610612755,
    "Phoenix Suns": 1610612756,
    "Houston Rockets": 1610612745,
    "Atlanta Hawks": 1610612737,
    "Sacramento Kings": 1610612758,
    "LA Clippers": 1610612746,
    "Brooklyn Nets": 1610612751,
    "Orlando Magic": 1610612753,
    "Los Angeles Lakers": 1610612747,
    "New York Knicks": 1610612752,
    "Chicago Bulls": 1610612741,
    "Denver Nuggets": 1610612743,
    "Memphis Grizzlies": 1610612763,
    "San Antonio Spurs": 1610612759,
    "Indiana Pacers": 1610612754,
    "Utah Jazz": 1610612762,
    "Oklahoma City Thunder": 1610612760,
    "Detroit Pistons": 1610612765,
    "Washington Wizards": 1610612764,
}


class GamelogRepository:
    def __init__(self, db: Session, api_client: ApiClient):
        self.db = db
        self.api_client = api_client

    def query_gamelog_by_team_date(
        self,
        api_client_id: Optional[UUID] = None,
        team1: Optional[str] = None,
        team2: Optional[str] = None,
        date: Optional[date] = None,
        limit: Optional[int] = 1,
        desc: bool = False,
    ) -> list[Gamelog]:
        if not self.api_client.trusted:
            if not api_client_id:
                api_client_id = self.api_client.id

            if api_client_id != self.api_client.id:
                raise NBAError(
                    "Forbidden",
                    NBAErrorCode.API_CLIENT_NOT_AUTHORIZED,
                    HTTP_403_FORBIDDEN,
                )

        qry = self.db.query(Gamelog)
        team1_id = name_to_id[team1]
        team2_id = name_to_id[team2]

        qry = qry.filter(
            and_(
                date > Gamelog.GAME_DATE,
                and_(Gamelog.T1_TEAM_ID == team1_id, Gamelog.T2_TEAM_ID == team2_id),
            )
        )

        if desc:
            qry = qry.order_by(Gamelog.GAME_DATE.desc())
        else:
            qry = qry.order_by(Gamelog.GAME_DATE.desc())

        if limit is not None:
            qry = qry.limit(limit)

        return qry.all()
