from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def home():
    return {"message":"Fast api is running"}

from app.db.session import engine
from app.db.base import Base

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    print("Database connected and tables created!")