import enum
from datetime import date, datetime
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel

from nba_backend.exceptions import NBAErrorCode


class TaskRequestType(str, enum.Enum):
    random = "random"
    summarize_story = "summarize_story"
    rate_summary = "rate_summary"
    initial_prompt = "initial_prompt"
    prompter_reply = "prompter_reply"
    assistant_reply = "assistant_reply"
    rank_initial_prompts = "rank_initial_prompts"
    rank_prompter_replies = "rank_prompter_replies"
    rank_assistant_replies = "rank_assistant_replies"
    label_initial_prompt = "label_initial_prompt"
    label_assistant_reply = "label_assistant_reply"
    label_prompter_reply = "label_prompter_reply"


class User(BaseModel):
    id: str
    display_name: str
    auth_method: Literal["discord", "local", "system"]


class Account(BaseModel):
    id: UUID
    provider: str
    provider_account_id: str


class Token(BaseModel):
    access_token: str
    token_type: str


class FrontEndUser(User):
    user_id: UUID
    enabled: bool
    deleted: bool
    notes: str
    created_date: Optional[datetime] = None
    show_on_leaderboard: bool
    streak_days: Optional[int] = None
    streak_last_day_date: Optional[datetime] = None
    last_activity_date: Optional[datetime] = None
    tos_acceptance_date: Optional[datetime] = None


class PageResult(BaseModel):
    prev: str | None
    next: str | None
    sort_key: str
    items: list
    order: Literal["asc", "desc"]


class FrontEndUserPage(PageResult):
    items: list[FrontEndUser]


class ConversationMessage(BaseModel):
    """Represents a message in a conversation between the user and the assistant."""

    id: Optional[UUID]
    user_id: Optional[UUID]
    frontend_message_id: Optional[str]
    text: str
    lang: Optional[str]  # BCP 47
    is_assistant: bool
    emojis: Optional[dict[str, int]]
    user_emojis: Optional[list[str]]
    user_is_author: Optional[bool]
    synthetic: Optional[bool]


class Conversation(BaseModel):
    """Represents a conversation between the prompter and the assistant."""

    messages: list[ConversationMessage] = []

    def __len__(self):
        return len(self.messages)

    @property
    def is_prompter_turn(self) -> bool:
        if len(self) == 0:
            return True
        last_message = self.messages[-1]
        if last_message.is_assistant:
            return True
        return False


class Message(ConversationMessage):
    parent_id: Optional[UUID]
    created_date: Optional[datetime]
    review_result: Optional[bool]
    review_count: Optional[int]
    deleted: Optional[bool]
    model_name: Optional[str]
    message_tree_id: Optional[UUID]
    ranking_count: Optional[int]
    rank: Optional[int]
    user: Optional[FrontEndUser]


class MessagePage(PageResult):
    items: list[Message]


class MessageTree(BaseModel):
    """All messages belonging to the same message tree."""

    id: UUID
    messages: list[Message] = []


class Gamelog(BaseModel):
    id: Optional[UUID]

    DAY_WITHIN_SEASON: Optional[int]
    GAME_DATE: Optional[date]
    GAME_ID: Optional[int]

    T1_IS_HOME: Optional[bool]
    T1_PLUS_MINUS: Optional[float]
    T1_PTS: Optional[float]
    T1_TEAM_ID: Optional[float]
    T1_TEAM_NAME: Optional[str]
    T1_W: Optional[float]
    T1_W_cum: Optional[float]

    T2_IS_HOME: Optional[bool]
    T2_PLUS_MINUS: Optional[float]
    T2_PTS: Optional[float]
    T2_TEAM_ID: Optional[float]
    T2_TEAM_NAME: Optional[str]
    T2_W: Optional[float]
    T2_W_cum: Optional[float]


class Teamstat(BaseModel):
    __tablename__ = "teamstat"

    id: Optional[UUID]

    DAY_WITHIN_SEASON: Optional[int]
    GAME_DATE: Optional[date]
    TEAM_ID: Optional[int]

    lag08_GP: Optional[float]
    lag08_W_PCT: Optional[float]
    lag08_FG_PCT: Optional[float]
    lag08_FT_PCT: Optional[float]
    lag08_OREB: Optional[float]
    lag08_DREB: Optional[float]
    lag08_REB: Optional[float]
    lag08_AST: Optional[float]
    lag08_TOV: Optional[float]
    lag08_STL: Optional[float]
    lag08_BLK: Optional[float]
    lag08_PTS: Optional[float]
    lag08_PLUS_MINUS: Optional[float]
    lag08_W_PCT_RANK: Optional[float]
    lag08_PTS_RANK: Optional[float]
    lag08_PLUS_MINUS_RANK: Optional[float]

    lag16_GP: Optional[float]
    lag16_W_PCT: Optional[float]
    lag16_FG_PCT: Optional[float]
    lag16_FT_PCT: Optional[float]
    lag16_OREB: Optional[float]
    lag16_DREB: Optional[float]
    lag16_REB: Optional[float]
    lag16_AST: Optional[float]
    lag16_TOV: Optional[float]
    lag16_STL: Optional[float]
    lag16_BLK: Optional[float]
    lag16_PTS: Optional[float]
    lag16_PLUS_MINUS: Optional[float]
    lag16_W_PCT_RANK: Optional[float]
    lag16_PTS_RANK: Optional[float]
    lag16_PLUS_MINUS_RANK: Optional[float]

    lag32_GP: Optional[float]
    lag32_W_PCT: Optional[float]
    lag32_FG_PCT: Optional[float]
    lag32_FT_PCT: Optional[float]
    lag32_OREB: Optional[float]
    lag32_DREB: Optional[float]
    lag32_REB: Optional[float]
    lag32_AST: Optional[float]
    lag32_TOV: Optional[float]
    lag32_STL: Optional[float]
    lag32_BLK: Optional[float]
    lag32_PTS: Optional[float]
    lag32_PLUS_MINUS: Optional[float]
    lag32_W_PCT_RANK: Optional[float]
    lag32_PTS_RANK: Optional[float]
    lag32_PLUS_MINUS_RANK: Optional[float]

    lag64_GP: Optional[float]
    lag64_W_PCT: Optional[float]
    lag64_FG_PCT: Optional[float]
    lag64_FT_PCT: Optional[float]
    lag64_OREB: Optional[float]
    lag64_DREB: Optional[float]
    lag64_REB: Optional[float]
    lag64_AST: Optional[float]
    lag64_TOV: Optional[float]
    lag64_STL: Optional[float]
    lag64_BLK: Optional[float]
    lag64_PTS: Optional[float]
    lag64_PLUS_MINUS: Optional[float]
    lag64_W_PCT_RANK: Optional[float]
    lag64_PTS_RANK: Optional[float]
    lag64_PLUS_MINUS_RANK: Optional[float]

    lag180_GP: Optional[float]
    lag180_W_PCT: Optional[float]
    lag180_FG_PCT: Optional[float]
    lag180_FT_PCT: Optional[float]
    lag180_OREB: Optional[float]
    lag180_DREB: Optional[float]
    lag180_REB: Optional[float]
    lag180_AST: Optional[float]
    lag180_TOV: Optional[float]
    lag180_STL: Optional[float]
    lag180_BLK: Optional[float]
    lag180_PTS: Optional[float]
    lag180_PLUS_MINUS: Optional[float]
    lag180_W_PCT_RANK: Optional[float]
    lag180_PTS_RANK: Optional[float]
    lag180_PLUS_MINUS_RANK: Optional[float]


class PredictionResult(BaseModel):
    team1_logit: Optional[float]
    team2_logit: Optional[float]


class NBAErrorResponse(BaseModel):
    """The format of an error response from the NBA API."""

    error_code: NBAErrorCode
    message: str
