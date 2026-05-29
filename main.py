from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import Base, engine

import books.models
import members.models
import rentals.models

from books.router   import router as books_router
from members.router import router as members_router
from rentals.router import router as rentals_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: 테이블 생성
    Base.metadata.create_all(bind=engine)
    print("🏗️ 테이블 생성 완료! (books, members, rentals)")
    yield
    # shutdown: 필요시 정리 작업


app = FastAPI(
    title="📚 도서관 책대여관리시스템",
    description="FastAPI MVC — Like a package 구조",
    version="3.0.0",
    lifespan=lifespan,
)

app.include_router(books_router)
app.include_router(members_router)
app.include_router(rentals_router)
