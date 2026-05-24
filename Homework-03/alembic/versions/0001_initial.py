"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-05-24

"""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "faculties",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50), nullable=False, unique=True),
    )

    op.create_table(
        "subjects",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(100), nullable=False, unique=True),
    )

    op.create_table(
        "students",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.UniqueConstraint("last_name", "first_name", name="uq_student_name"),
    )

    op.create_table(
        "grades",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("student_id", sa.Integer, sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
        sa.Column("faculty_id", sa.Integer, sa.ForeignKey("faculties.id"), nullable=False),
        sa.Column("subject_id", sa.Integer, sa.ForeignKey("subjects.id"), nullable=False),
        sa.Column("grade", sa.Integer, nullable=False),
    )


def downgrade():
    op.drop_table("grades")
    op.drop_table("students")
    op.drop_table("subjects")
    op.drop_table("faculties")
