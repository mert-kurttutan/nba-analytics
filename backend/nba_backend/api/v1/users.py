from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from starlette.status import HTTP_204_NO_CONTENT

from nba_backend.api import deps
from nba_backend.models import ApiClient, User
from nba_backend.schemas import protocol
from nba_backend.user_repository import UserRepository

router = APIRouter()


@router.get("/by_username", response_model=list[protocol.FrontEndUser])
def get_users_ordered_by_username(
    api_client_id: Optional[UUID] = None,
    gte_username: Optional[str] = None,
    gt_id: Optional[UUID] = None,
    lte_username: Optional[str] = None,
    lt_id: Optional[UUID] = None,
    search_text: Optional[str] = None,
    auth_method: Optional[str] = None,
    max_count: Optional[int] = Query(100, gt=0, le=10000),
    desc: Optional[bool] = False,
    api_client: ApiClient = Depends(deps.get_api_client),
    db: Session = Depends(deps.get_db),
):
    ur = UserRepository(db, api_client)
    users = ur.query_users_ordered_by_username(
        api_client_id=api_client_id,
        gte_username=gte_username,
        gt_id=gt_id,
        lte_username=lte_username,
        lt_id=lt_id,
        auth_method=auth_method,
        search_text=search_text,
        limit=max_count,
        desc=desc,
    )
    return [u.to_protocol_frontend_user() for u in users]


@router.get("/by_display_name", response_model=list[protocol.FrontEndUser])
def get_users_ordered_by_display_name(
    api_client_id: Optional[UUID] = None,
    gte_display_name: Optional[str] = None,
    gt_id: Optional[UUID] = None,
    lte_display_name: Optional[str] = None,
    lt_id: Optional[UUID] = None,
    auth_method: Optional[str] = None,
    search_text: Optional[str] = None,
    max_count: Optional[int] = Query(100, gt=0, le=10000),
    desc: Optional[bool] = False,
    api_client: ApiClient = Depends(deps.get_api_client),
    db: Session = Depends(deps.get_db),
):
    ur = UserRepository(db, api_client)
    users = ur.query_users_ordered_by_display_name(
        api_client_id=api_client_id,
        gte_display_name=gte_display_name,
        gt_id=gt_id,
        lte_display_name=lte_display_name,
        lt_id=lt_id,
        auth_method=auth_method,
        search_text=search_text,
        limit=max_count,
        desc=desc,
    )
    return [u.to_protocol_frontend_user() for u in users]


@router.get("/{user_id}", response_model=protocol.FrontEndUser)
def get_user(
    user_id: UUID,
    api_client_id: UUID = None,
    db: Session = Depends(deps.get_db),
    api_client: ApiClient = Depends(deps.get_api_client),
):
    """
    Get a user by global user ID. Only trusted clients can resolve users they did not register.
    """
    ur = UserRepository(db, api_client)
    user: User = ur.get_user(user_id, api_client_id)
    return user.to_protocol_frontend_user()


@router.put("/{user_id}", status_code=HTTP_204_NO_CONTENT)
def update_user(
    user_id: UUID,
    enabled: Optional[bool] = None,
    notes: Optional[str] = None,
    show_on_leaderboard: Optional[bool] = None,
    tos_acceptance: Optional[bool] = None,
    db: Session = Depends(deps.get_db),
    api_client: ApiClient = Depends(deps.get_trusted_api_client),
):
    """
    Update a user by global user ID. Only trusted clients can update users.
    """
    ur = UserRepository(db, api_client)
    ur.update_user(user_id, enabled, notes, show_on_leaderboard, tos_acceptance)


@router.delete("/{user_id}", status_code=HTTP_204_NO_CONTENT)
def delete_user(
    user_id: UUID,
    db: Session = Depends(deps.get_db),
    api_client: ApiClient = Depends(deps.get_trusted_api_client),
):
    """
    Delete a user by global user ID. Only trusted clients can delete users.
    """
    ur = UserRepository(db, api_client)
    ur.mark_user_deleted(user_id)
