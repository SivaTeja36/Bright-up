from datetime import (
    date, 
    datetime
)

import sqlalchemy as sa

from app.connectors.database_connector import Base


class BatchMentor(Base):
    __tablename__ = "batch_mentors"

    id: int = sa.Column(sa.Integer, primary_key=True, nullable=False) # type: ignore
    batch_id: int = sa.Column(sa.Integer, sa.ForeignKey("batches.id"), nullable=False) # type: ignore
    mentor_id: int = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False) # type: ignore
    created_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now()) # type: ignore
    created_by: int = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False) # type: ignore
    updated_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now()) # type: ignore
    updated_by: int = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False) # type: ignore