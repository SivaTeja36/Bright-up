from datetime import datetime

import sqlalchemy as sa

from app.connectors.database_connector import Base
from app.utils.enums import Roles
from app.utils.hasher import Hasher

class User(Base):
    __tablename__ = "users"

    id: int = sa.Column(sa.Integer, primary_key=True, nullable=False) # type: ignore
    name: str = sa.Column(sa.String(256), nullable=False) # type: ignore
    username: str = sa.Column(sa.String(256), nullable=False, index=True, unique=True) # type: ignore
    __password: str = sa.Column(name="password", type_=sa.String(500), nullable=False, index=True) # type: ignore
    contact: str = sa.Column(sa.String(500), nullable=False, unique=True) # type: ignore
    __role: int = sa.Column(name="role", type_=sa.Integer, nullable=False) # type: ignore
    created_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now()) # type: ignore
    is_active: bool = sa.Column(sa.Boolean, nullable=False, default=True) # type: ignore
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute, use verify_password method for verifying')
    
    @property
    def role(self):
        return Roles(self.__role).name
    
    @role.setter
    def role(self, role_from: str):
        self.__role = Roles[role_from].value
    
    @password.setter
    def password(self, password:str):
        self.__password = Hasher.get_password_hash(password)
    
    def verify_password(self, password:str):
        return Hasher.verify_password(password,self.__password)