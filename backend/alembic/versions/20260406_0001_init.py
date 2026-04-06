"""init schema

Revision ID: 20260406_0001
Revises:
Create Date: 2026-04-06
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260406_0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_users_id", "users", ["id"])
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "courses",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("cefr_level", sa.String(length=16), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
    )
    op.create_index("ix_courses_id", "courses", ["id"])

    op.create_table(
        "lessons",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("course_id", sa.Integer(), sa.ForeignKey("courses.id"), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("transcript", sa.Text(), nullable=False),
        sa.Column("audio_url", sa.Text(), nullable=False),
        sa.Column("source_name", sa.String(length=255), nullable=False),
        sa.Column("source_url", sa.Text(), nullable=False),
        sa.Column("license_name", sa.String(length=255), nullable=False),
        sa.Column("license_url", sa.Text(), nullable=False),
        sa.Column("attribution_text", sa.Text(), nullable=False),
    )
    op.create_index("ix_lessons_id", "lessons", ["id"])

    op.create_table(
        "drills",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("lesson_id", sa.Integer(), sa.ForeignKey("lessons.id"), nullable=False),
        sa.Column("drill_type", sa.String(length=64), nullable=False),
        sa.Column("prompt_text", sa.Text(), nullable=False),
        sa.Column("base_sentence", sa.Text(), nullable=False),
        sa.Column("target_answer", sa.Text(), nullable=False),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("sequence_order", sa.Integer(), nullable=False),
    )
    op.create_index("ix_drills_id", "drills", ["id"])
    op.create_index("ix_drills_lesson_id", "drills", ["lesson_id"])

    op.create_table(
        "attempts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("drill_id", sa.Integer(), sa.ForeignKey("drills.id"), nullable=False),
        sa.Column("input_text", sa.Text(), nullable=False),
        sa.Column("is_correct", sa.Boolean(), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("feedback_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_attempts_id", "attempts", ["id"])

    op.create_table(
        "lesson_progress",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("lesson_id", sa.Integer(), sa.ForeignKey("lessons.id"), nullable=False),
        sa.Column("attempts_count", sa.Integer(), nullable=False),
        sa.Column("completed_drills", sa.Integer(), nullable=False),
        sa.Column("total_drills", sa.Integer(), nullable=False),
        sa.Column("average_score", sa.Float(), nullable=False),
        sa.Column("completion_rate", sa.Float(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("user_id", "lesson_id", name="uq_user_lesson_progress"),
    )
    op.create_index("ix_lesson_progress_id", "lesson_progress", ["id"])


def downgrade() -> None:
    op.drop_index("ix_lesson_progress_id", table_name="lesson_progress")
    op.drop_table("lesson_progress")
    op.drop_index("ix_attempts_id", table_name="attempts")
    op.drop_table("attempts")
    op.drop_index("ix_drills_lesson_id", table_name="drills")
    op.drop_index("ix_drills_id", table_name="drills")
    op.drop_table("drills")
    op.drop_index("ix_lessons_id", table_name="lessons")
    op.drop_table("lessons")
    op.drop_index("ix_courses_id", table_name="courses")
    op.drop_table("courses")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_table("users")
