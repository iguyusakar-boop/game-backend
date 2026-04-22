from fastapi import APIRouter
from app.schemas.action import ActionLogIn
from app.engines.action_engine import process_action

router = APIRouter(prefix="/actions", tags=["actions"])

@router.post("/log")
def log_action(data: ActionLogIn):
    return process_action(data)