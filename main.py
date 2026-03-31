from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine
from app.db.base import Base
from app.api.v1.endpoints import enquiry, course


app = FastAPI(title="Thapasya ERP System")

app.include_router(enquiry.router, prefix="/api/v1/enquiries", tags=["Enquiries"])
app.include_router(course.router, prefix="/api/v1/courses", tags=["Courses"])


@app.get("/")
def home():
    return {"message": "Fast API is running"}

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    print("Tables created!")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)