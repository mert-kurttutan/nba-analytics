from datetime import date
from typing import Optional
from uuid import UUID

import torch
from fastapi import APIRouter, Depends
from sqlmodel import Session

from nba_backend.api import deps
from nba_backend.exceptions.nba_api_error import NBAError, NBAErrorCode
from nba_backend.gamelog_repository import GamelogRepository
from nba_backend.models import ApiClient
from nba_backend.schemas import protocol
from nba_backend.teamstat_repository import TeamstatRepository

from ...inference.base_mlp import BaseMLP

router = APIRouter()


@router.get("/predict_match", response_model=list[protocol.PredictionResult])
def get_match_prediction(
    api_client_id: Optional[UUID] = None,
    team1: str = "Cleveland Cavaliers",
    team2: str = "New York Knicks",
    date: date = "2016-10-26",
    desc: bool = False,
    api_client: ApiClient = Depends(deps.get_api_client),
    db: Session = Depends(deps.get_db),
):
    # Not sure if we need this here, since this check
    # will be done in the gamelog and teamstat queries
    if not api_client.trusted:
        if not api_client_id:
            api_client_id = api_client.id

        if api_client_id != api_client.id:
            raise NBAError(
                "Forbidden", NBAErrorCode.API_CLIENT_NOT_AUTHORIZED, HTTP_403_FORBIDDEN
            )

    gr = GamelogRepository(db, api_client)
    tsr = TeamstatRepository(db, api_client)
    gamelogs = gr.query_gamelog_by_team_date(
        api_client_id=api_client_id,
        team1=team1,
        team2=team2,
        date=date,
        limit=1,
        desc=desc,
    )

    teamstats_1 = tsr.query_teamstat_by_date_team(
        api_client_id=api_client_id,
        team_name=team1,
        date=date,
        limit=1,
        desc=desc,
    )

    teamstats_2 = tsr.query_teamstat_by_date_team(
        api_client_id=api_client_id,
        team_name=team2,
        date=date,
        limit=1,
        desc=desc,
    )

    if len(teamstats_1) != 1:
        raise NBAError(
            f"The stats for {team1} on this date is not available",
            NBAErrorCode.GENERIC_ERROR,
        )
    elif len(teamstats_2) != 1:
        raise NBAError(
            f"The stats for {team2} on this date is not available",
            NBAErrorCode.GENERIC_ERROR,
        )

    team1_dict, team2_dict = preprocess_query_dict(
        teamstats_1[0].dict(), teamstats_2[0].dict(), gamelogs[0].dict()
    )
    result_arr = predict_match_from_teamstat(team1_dict, team2_dict).tolist()

    return [
        protocol.PredictionResult(team1_logit=result[0], team2_logit=result[1])
        for result in result_arr
    ]


def get_model(config):
    if config["model_name"] == "base_mlp":
        return BaseMLP(config)
    else:
        raise NotImplementedError


ckpt = torch.load("bin/prototype-v0_best.pt")
model_conf = ckpt["model_config"]
model = get_model(model_conf)
model = model.to("cpu")
print("loading model")
model.load_state_dict(ckpt["model"])


def preprocess_query_dict(
    team1_stat_dict: dict,
    team2_stat_dict: dict,
    gamelog_stat_dict: dict,
) -> tuple[dict, dict]:
    DROP_TEAM_STAT = [
        "GAME_DATE",
    ]

    team_id_offset = 1610612700

    for col in DROP_TEAM_STAT:
        del team1_stat_dict[col]
        del team2_stat_dict[col]

    del team2_stat_dict["DAY_WITHIN_SEASON"]

    del team1_stat_dict["id"]
    del team2_stat_dict["id"]

    team1_stat_dict["W_cum"] = gamelog_stat_dict["T1_W_cum"]
    team2_stat_dict["W_cum"] = gamelog_stat_dict["T2_W_cum"]

    team1_stat_dict["IS_HOME"] = 1

    team1_stat_dict["TEAM_ID"] -= team_id_offset
    team2_stat_dict["TEAM_ID"] -= team_id_offset

    team1_stat_dict = dict(sorted(team1_stat_dict.items()))
    team2_stat_dict = dict(sorted(team2_stat_dict.items()))

    return team1_stat_dict, team2_stat_dict


def predict_match_from_teamstat(team1_stat, team2_stat):
    input_arr = list(team1_stat.values())
    input_arr.extend(list(team2_stat.values()))
    input_tensor = torch.tensor([input_arr], dtype=torch.float32)
    with torch.inference_mode():
        model.eval()
        result = model(input_tensor)
    return result
