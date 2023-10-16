import re
import uuid

import uvicorn
from fastapi import HTTPException, FastAPI, APIRouter
from pydantic import BaseModel, EmailStr, validator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Boolean, String

import settings

##################################
# Блок общего взаимодействия с БД
###################################


# создаем асинхронный движок для взаимодействия с БД
engine = create_async_engine(settings.REAL_DATABASE_URL, future=True, echo=True)

# создаем объект сессии асинхронной
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

###############################
# Блок с моделями базы данных
##############################
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean(), default=True)


###########################################
# Блок взаимодейтствия БД с бизнес логикой
###########################################
class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
            self, name: str, surname: str, email: str
    ) -> User:
        new_user = User(
            name=name,
            surname=surname,
            email=email
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user


########################
# БЛОК С АПИ МОДЕЛЯМИ
##########################

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TuneModel(BaseModel):
    class Config:
        """ говорим пайдентику все объекты превращать в жэсоны"""
        orm_mode = True


class ShowUser(TuneModel):
    user_id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    is_active: bool


class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr

    @validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should only letters"
            )
        return value

    @validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surame should only letters"
            )
        return value


# BLOCK WITH ROUTERS
#############################

# create instance of the app
app = FastAPI(title="luchanos-oxford-iniversity")

user_router = APIRouter()


async def _create_new_user(body: UserCreate) -> ShowUser:
    async with async_session() as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                name=body.name,
                surname=body.surname,
                email=body.email
            )
            return ShowUser(
                user_id=user.user_id,
                name=user.name,
                surname=user.surname,
                email=user.email,
                is_active=user.is_active
            )


@user_router.post('/', response_model=ShowUser)
async def create_user(body: UserCreate) -> ShowUser:
    return await _create_new_user(body)


###########################################
# create main router who collect all routers
###########################################

main_api_router = APIRouter()
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
