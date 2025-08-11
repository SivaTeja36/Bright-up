from datetime import datetime

import sqlalchemy as sa

from app.connectors.database_connector import Base
from app.utils.enums import UserEducationStatus


class UserEducation(Base):
    __tablename__ = "user_education"

    id: int = sa.Column(sa.Integer, primary_key=True, nullable=False) # type: ignore
    user_id: int = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False)
    degree: str = sa.Column(sa.String(100), nullable=False) # type: ignore)
    specialization: str = sa.Column(sa.String(100), nullable=False) # type: ignore)
    start_year: int = sa.Column(sa.Integer, nullable=False) # type: ignore
    end_year: int = sa.Column(sa.Integer, nullable=True) # type: ignore
    current_year_of_study = sa.Column(sa.Integer, nullable=True)  # type: ignore 
    status: str = sa.Column(sa.String(30), nullable=False, default=UserEducationStatus.ON_GOING) # type: ignore
    city: str = sa.Column(sa.String(100), nullable=False) # type: ignore
    state: str = sa.Column(sa.String(100), nullable=False) # type: ignore
    created_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now()) # type: ignore
    created_by: int = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False) # type: ignore
    updated_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now()) # type: ignore
    updated_by: int = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False) # type: ignore