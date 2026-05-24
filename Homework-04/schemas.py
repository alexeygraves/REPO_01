from pydantic import BaseModel, ConfigDict
from typing import Optional


class FacultyCreate(BaseModel):
    name: str

class FacultyUpdate(BaseModel):
    name: str

class FacultyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class SubjectCreate(BaseModel):
    name: str

class SubjectUpdate(BaseModel):
    name: str

class SubjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


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


class StudentWithGrade(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    student: StudentOut
    grade: int
