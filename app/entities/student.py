from datetime import datetime

import sqlalchemy as sa

from app.connectors.database_connector import Base


class Student(Base):
    __tablename__ = "students"

    id: int = sa.Column(sa.Integer, primary_key=True, nullable=False) # type: ignore
    user_id: int = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False)
    degree: str = sa.Column(sa.String(100), nullable=False) # type: ignore)
    specialization: str = sa.Column(sa.String(100), nullable=False) # type: ignore)
    passout_year: int = sa.Column(sa.Integer, nullable=False) # type: ignore
    city: str = sa.Column(sa.String(100), nullable=False) # type: ignore
    state: str = sa.Column(sa.String(100), nullable=False) # type: ignore
    referral_by: int = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False) # type: ignore
    created_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now()) # type: ignore
    created_by: int = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False) # type: ignore
    updated_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now()) # type: ignore
    updated_by: int = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False) # type: ignore
    is_active: bool = sa.Column(sa.Boolean, nullable=False, default=True) # type: ignore