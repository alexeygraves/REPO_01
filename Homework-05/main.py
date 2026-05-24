from fastapi import Depends, FastAPI

import models
from auth import get_current_user, router as auth_router
from database import Base, engine
from routers import (
    analytics_router,
    faculty_router,
    grade_router,
    student_router,
    subject_router,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Students API")

# /auth открыт для всех — регистрация и логин
app.include_router(auth_router)

# все CRUD-роуты закрыты, требуют валидный Bearer токен
auth_dep = [Depends(get_current_user)]

app.include_router(faculty_router, dependencies=auth_dep)
app.include_router(subject_router, dependencies=auth_dep)
app.include_router(student_router, dependencies=auth_dep)
app.include_router(grade_router, dependencies=auth_dep)
app.include_router(analytics_router, dependencies=auth_dep)
