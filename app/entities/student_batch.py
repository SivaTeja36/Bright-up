from datetime import date, datetime

import sqlalchemy as sa

from app.connectors.database_connector import Base


class StudentBatch(Base):
    __tablename__ = "student_batches"

    id: int = sa.Column(sa.Integer, primary_key=True, nullable=False) # type: ignore
    student_id: int = sa.Column(sa.Integer, sa.ForeignKey("students.id"), nullable=False) # type: ignore
    batch_id: int = sa.Column(sa.Integer, sa.ForeignKey("batches.id"), nullable=False) # type: ignore
    amount: int = sa.Column(sa.Integer, nullable=False) # type: ignore
    joined_at: date = sa.Column(sa.Date, nullable=False) # type: ignore
    created_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now()) # type: ignore
    created_by: int = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False) # type: ignore
    updated_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now()) # type: ignore
    updated_by: int = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False) # type: ignore