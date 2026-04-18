from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine
from app.db.base import Base
from app.api.v1.router import api_router
from fastapi import File, UploadFile, HTTPException
from app.utils.s3 import upload_file_to_s3
from app.db.session import SessionLocal
from app.utils.seeds import create_default_admin

app = FastAPI(title="Thapasya ERP System")

# CORS Middleware (Crucial for your React Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def home():
    return {"message": "CI/CD working test 2 "}

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

    db=SessionLocal()

    create_default_admin(db)

    db.close()

