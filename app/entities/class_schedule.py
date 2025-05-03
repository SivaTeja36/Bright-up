from datetime import datetime, time

import sqlalchemy as sa

from app.connectors.database_connector import Base


class ClassSchedule(Base):
    __tablename__ = "class_schedules"

    id: int = sa.Column(sa.Integer, primary_key=True, nullable=False) # type: ignore
    batch_id: int = sa.Column(sa.Integer, sa.ForeignKey("batches.id"), nullable=False) # type: ignore
    day: str = sa.Column(sa.String(10), nullable=False) # type: ignore
    start_time: time = sa.Column(sa.Time, nullable=False) # type: ignore
    end_time: time = sa.Column(sa.Time, nullable=False) # type: ignore
    created_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now()) # type: ignore
    created_by: int = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False) # type: ignore
    updated_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now()) # type: ignore
    updated_by: int = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False) # type: ignore
    is_active: bool = sa.Column(sa.Boolean, nullable=False, default=True) # type: ignore