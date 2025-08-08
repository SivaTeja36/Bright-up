from datetime import datetime

import sqlalchemy as sa

from app.connectors.database_connector import Base
from app.utils.enums import (
    GenderTypes, 
    Roles
)
from app.utils.hasher import Hasher

class User(Base):
    __tablename__ = "users"

    id: int = sa.Column(sa.Integer, primary_key=True, nullable=False) 
    name: str = sa.Column(sa.String(50), nullable=False) 
    email: str = sa.Column(sa.String(100), nullable=False, index=True, unique=True) 
    __gender: int = sa.Column(name="gender", type_=sa.Integer, nullable=False)
    __password: str = sa.Column(name="password", type_=sa.String(200), nullable=False, index=True) 
    phone_number: str = sa.Column(sa.String(20), nullable=False, unique=True) 
    __role: int = sa.Column(name="role", type_=sa.Integer, nullable=False)
    created_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now())
    created_by: int = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=True)
    updated_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now())
    updated_by: int = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=True)
    is_active: bool = sa.Column(sa.Boolean, nullable=False, default=True)
    
    @property
    def gender(self):
        return GenderTypes(self.__gender).name
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute, use verify_password method for verifying')
    
    @property
    def role(self):
        return Roles(self.__role).name
    
    @gender.setter
    def gender(self, gender: str):
        self.__gender = GenderTypes[gender].value
    
    @role.setter
    def role(self, role_from: str):
        self.__role = Roles[role_from].value
    
    @password.setter
    def password(self, password: str):
        self.__password = Hasher.get_password_hash(password)
    
    def verify_password(self, password: str):
        return Hasher.verify_password(password, self.__password)