from fastapi import FastAPI
from app.routers.students import router as students_router
from app.routers.subjects import router as subjects_router
from app.routers.users import router as users_router

from app.middlewares.logging import log_request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Homework API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.middleware("http")(log_request)

app.include_router(students_router)
app.include_router(subjects_router)
app.include_router(users_router)