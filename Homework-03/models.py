from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base


class Faculty(Base):
    __tablename__ = "faculties"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    grades = relationship("Grade", back_populates="faculty")


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    grades = relationship("Grade", back_populates="subject")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    last_name = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)

    grades = relationship("Grade", back_populates="student")

    # в исходных данных одна и та же пара фамилия+имя встречается только один раз
    __table_args__ = (
        UniqueConstraint("last_name", "first_name", name="uq_student_name"),
    )


class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculties.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    grade = Column(Integer, nullable=False)

    student = relationship("Student", back_populates="grades")
    faculty = relationship("Faculty", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")
