from fastapi import APIRouter

from nba_backend.api.v1 import gamelogs, inference, teamstats, users  # admin,; auth,

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(gamelogs.router, prefix="/gamelogs", tags=["gamelogs"])
api_router.include_router(teamstats.router, prefix="/teamstats", tags=["teamstats"])
api_router.include_router(inference.router, prefix="/inference", tags=["inference"])
# api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
# api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
