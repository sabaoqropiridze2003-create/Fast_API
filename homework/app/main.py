from fastapi import FastAPI
from app.routers.students import router as students_router
from app.routers.subjects import router as subjects_router
from app.routers.users import router as users_router

app = FastAPI(
    title="Homework API",
    version="0.1.0",
)

app.include_router(students_router)
app.include_router(subjects_router)
app.include_router(users_router)