from fastapi import FastAPI

app=FastAPI()

from app.db.session import engine
from app.db.base import Base
from app.api.v1.router import api_router

app.include_router(api_router)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    print("Tables created!")



