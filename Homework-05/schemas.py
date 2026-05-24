from pydantic import BaseModel, ConfigDict
from typing import Optional


# --- auth ---

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: str


# --- faculty ---

class FacultyCreate(BaseModel):
    name: str

class FacultyUpdate(BaseModel):
    name: str

class FacultyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


# --- subject ---

class SubjectCreate(BaseModel):
    name: str

class SubjectUpdate(BaseModel):
    name: str

class SubjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


# --- student ---

class StudentCreate(BaseModel):
    last_name: str
    first_name: str

class StudentUpdate(BaseModel):
    last_name: Optional[str] = None
    first_name: Optional[str] = None

class StudentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    last_name: str
    first_name: str


# --- grade ---

class GradeCreate(BaseModel):
    student_id: int
    faculty_id: int
    subject_id: int
    grade: int

class GradeUpdate(BaseModel):
    grade: int

class GradeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    student_id: int
    faculty_id: int
    subject_id: int
    grade: int
