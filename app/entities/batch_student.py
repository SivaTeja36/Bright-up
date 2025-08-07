from datetime import (
    date, 
    datetime
)

import sqlalchemy as sa

from app.connectors.database_connector import Base


class BatchStudent(Base):
    __tablename__ = "batch_students"

    id: int = sa.Column(sa.Integer, primary_key=True, nullable=False) # type: ignore
    batch_id: int = sa.Column(sa.Integer, sa.ForeignKey("batches.id"), nullable=False) # type: ignore
    student_id: int = sa.Column(sa.Integer, sa.ForeignKey("students.id"), nullable=False) # type: ignore
    class_amount: int = sa.Column(sa.Integer, nullable=False) # type: ignore
    amount_paid: int = sa.Column(sa.Integer, nullable=False, default=0) # type: ignore
    mentor_amount: int = sa.Column(sa.Integer, nullable=False, default=0) # type: ignore
    referral_id: int = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=True)
    referral_percentage: float = sa.Column(sa.REAL, nullable=False)
    referral_amount: int = sa.Column(sa.Integer, nullable=False, default=0) # type: ignore
    joined_at: date = sa.Column(sa.Date, nullable=False) # type: ignore
    created_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now()) # type: ignore
    created_by: int = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False) # type: ignore
    updated_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now()) # type: ignore
    updated_by: int = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False) # type: ignore