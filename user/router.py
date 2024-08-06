from fastapi import Body, APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from user.auth.auth_handler import signJWT
from user.models import User
from user.schema import UserSchema, UserLoginSchema

router = APIRouter()


def generate_password_hash(password):
    return password + "_hashed"


def check_user(data: UserLoginSchema, db: AsyncSession = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if user:
        return True
    return False


@router.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    hashed_password = generate_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)

    db = next(get_db())
    try:
        db.add(new_user)
        db.commit()
    except IntegrityError:
        db.rollback()
        return {"detail": "Email already in use"}

    return signJWT(user.email)


@router.post("/user/login", tags=["user"])
async def user_login(
    user: UserLoginSchema = Body(), db: AsyncSession = Depends(get_db)
):
    if check_user(data=user, db=db):
        return signJWT(user.email)
    return {"error": "Wrong login details!"}
