from datetime import (
    datetime
)

import sqlalchemy as sa

from app.connectors.database_connector import Base


class Contact(Base):
    __tablename__ = "contacts"

    id: int = sa.Column(sa.Integer, primary_key=True, nullable=False) # type: ignore
    name: int = sa.Column(sa.Integer, sa.ForeignKey("batches.id"), nullable=False) # type: ignore
    phone_number: str = sa.Column(sa.String(15), nullable=False) # type: ignore
    comment: str = sa.Column(sa.Text, nullable=False) # type: ignore
    created_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now()) # type: ignore
    created_by: int = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False) # type: ignore
    updated_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now()) # type: ignore
    updated_by: int = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False) # type: ignore
    is_active: bool = sa.Column(sa.Boolean, nullable=False, default=True) # type: ignore