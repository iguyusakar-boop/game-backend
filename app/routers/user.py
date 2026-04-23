from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import DashboardResponse
from app.services.dashboard_service import get_user_dashboard_data

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/dashboard", response_model=DashboardResponse)
def get_user_dashboard(user_id: int, db: Session = Depends(get_db)):
    dashboard_data = get_user_dashboard_data(db, user_id)

    if not dashboard_data:
        raise HTTPException(status_code=404, detail="User not found")

    return dashboard_data