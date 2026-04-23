from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.auth import RegisterRequest, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=TokenResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.username == data.username).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kullanıcı sorgusu hatası: {str(e)}")

    if existing_user:
        raise HTTPException(status_code=400, detail="Kullanıcı zaten var")

    try:
        hashed_pw = hash_password(data.password)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Şifre hash hatası: {str(e)}")

    try:
        new_user = User(
            username=data.username,
            hashed_password=hashed_pw,
            xp=0,
            level=1,
            streak=0
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Veritabanı kayıt hatası: {str(e)}")

    try:
        access_token = create_access_token({"sub": str(new_user.id)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token oluşturma hatası: {str(e)}")

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    try:
        user = db.query(User).filter(User.username == form_data.username).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kullanıcı sorgusu hatası: {str(e)}")

    if not user:
        raise HTTPException(status_code=401, detail="Kullanıcı bulunamadı")

    try:
        password_ok = verify_password(form_data.password, user.hashed_password)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Şifre doğrulama hatası: {str(e)}"
        )

    if not password_ok:
        raise HTTPException(status_code=401, detail="Şifre hatalı")

    try:
        access_token = create_access_token({"sub": str(user.id)})
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Token oluşturma hatası: {str(e)}"
        )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "xp": current_user.xp,
        "level": current_user.level,
        "streak": current_user.streak
    }