import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import Base, engine
from app import models
from app.routers import (
    admin_auth,
    admin_buildings,
    admin_rooms,
    admin_courses,
    admin_exam_schedules,
    admin_office_hours,
    admin_campus_info,
    admin_technical_issues,
    ask,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(title="Smart Campus Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
logger.info("Database tables ensured")

app.include_router(admin_auth.router)
app.include_router(admin_buildings.router)
app.include_router(admin_rooms.router)
app.include_router(admin_courses.router)
app.include_router(admin_exam_schedules.router)
app.include_router(admin_office_hours.router)
app.include_router(admin_campus_info.router)
app.include_router(admin_technical_issues.router)
app.include_router(ask.router)

logger.info("Routers registered successfully")


@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {"message": "Smart Campus Assistant API is running"}