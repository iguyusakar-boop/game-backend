from pydantic import BaseModel
from typing import List


class LevelProgressResponse(BaseModel):
    current_xp: int
    level_min_xp: int
    level_max_xp: int
    xp_to_next_level: int
    progress_percent: int


class ProfileResponse(BaseModel):
    user_id: int
    username: str
    xp: int
    level: int
    streak: int
    level_progress: LevelProgressResponse


class StatsResponse(BaseModel):
    strength: int
    discipline: int
    focus: int
    energy: int


class QuestResponse(BaseModel):
    id: int
    title: str
    description: str
    quest_type: str
    target_value: int
    progress: int
    completed: bool
    xp_reward: int
    quest_date: str


class DashboardResponse(BaseModel):
    profile: ProfileResponse
    stats: StatsResponse
    today_quests: List[QuestResponse]