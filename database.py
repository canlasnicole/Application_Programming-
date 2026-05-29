from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# DB 연결 통로 (Engine)
SQLALCHEMY_DATABASE_URL = "sqlite:///./library.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# 각 요청마다 독립적인 세션
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# 모든 모델의 기반 클래스
Base = declarative_base()


def get_db():
    """의존성 주입용 — 요청마다 세션 생성 후 자동 close"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
