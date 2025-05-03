from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON

from app.connectors.database_connector import Base


class Syllabus(Base):
    __tablename__ = "syllabus"

    id: int = sa.Column(sa.Integer, primary_key=True, nullable=False) # type: ignore
    name: str = sa.Column(sa.String(100), nullable=False) # type: ignore
    topics: list = sa.Column(JSON, nullable=False) # type: ignore
    created_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now()) # type: ignore
    created_by: int = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False) # type: ignore
    updated_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now()) # type: ignore
    updated_by: int = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False) # type: ignore