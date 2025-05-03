from datetime import date, datetime

import sqlalchemy as sa

from app.connectors.database_connector import Base


class Batch(Base):
    __tablename__ = "batches"

    id: int = sa.Column(sa.Integer, primary_key=True, nullable=False) # type: ignore
    syllabus_ids: list = sa.Column(sa.ARRAY(sa.Integer), nullable=True) # type: ignore
    start_date: date = sa.Column(sa.Date, nullable=False) # type: ignore
    end_date: date = sa.Column(sa.Date, nullable=False) # type: ignore
    mentor_name: str = sa.Column(sa.String(100), nullable=False) # type: ignore
    created_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now()) # type: ignore
    created_by: int = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False) # type: ignore
    updated_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now()) # type: ignore
    updated_by: int = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False) # type: ignore
    is_active: bool = sa.Column(sa.Boolean, nullable=False, default=True) # type: ignore