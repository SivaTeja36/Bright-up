from datetime import (
    date,
    datetime
)

import sqlalchemy as sa

from app.connectors.database_connector import Base


class BatchStudentPayment(Base):
    __tablename__ = "batch_student_payments"

    id: int = sa.Column(sa.Integer, primary_key=True, nullable=False) # type: ignore
    batch_student_id: int = sa.Column(sa.Integer, sa.ForeignKey("batch_students.id"), nullable=False) # type: ignore
    payment_date: date = sa.Column(sa.Date, nullable=False) # type: ignore
    amount_paid: int = sa.Column(sa.Integer, nullable=False) # type: ignore
    mentor_share: int = sa.Column(sa.Integer, nullable=False) # type: ignore
    referral_share: int = sa.Column(sa.Integer, nullable=False, default=0) # type: ignore
    created_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now()) # type: ignore
    created_by: int = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False) # type: ignore
    updated_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now()) # type: ignore
    updated_by: int = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False) # type: ignore