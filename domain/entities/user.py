from sqlalchemy import Column, Integer, String, CHAR
from infrastructure.database.connection import Base

class User(Base):
    __tablename__ = "Users"

    UserId = Column(Integer, primary_key=True, autoincrement=True)
    Username = Column(String(255), nullable=False)
    Email = Column(String(255), unique=True, nullable=False)
    PasswordHash = Column(String(512), nullable=False)
    Role = Column(String(100), nullable=True)
    LocationID = Column(String(100), nullable=True)
    ApplicationGranted = Column(String(255), nullable=True)
    ModulesGranted = Column(String(255), nullable=True)
    dcode = Column(String(100), nullable=True)
    tcode = Column(String(100), nullable=True)
    SubDivCode = Column(CHAR(1), nullable=True)
    UserType = Column(String(100), nullable=True)
    Status = Column(CHAR(1), nullable=True)

    def __repr__(self):
        return f"<User(UserId={self.UserId}, Username={self.Username}, Email={self.Email})>"
