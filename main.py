import os
import firebase_admin
from firebase_admin import credentials
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine, SessionLocal
from app.db.base import Base
from app.api.v1.router import api_router
from app.utils.seeds import create_default_admin

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(ROOT_DIR, "app", "core", "firebase-credentials.json")

if not firebase_admin._apps:
    try:
        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
    except Exception:
        pass

app = FastAPI(title="Thapasya ERP System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://localhost:5174", 
        "https://thapasya-arts-school.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def home():
    return {"message": "CI/CD working test 2"}

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        create_default_admin(db)
    finally:
        db.close()