from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

class User(Base):
    """
    SQLAlchemy ORM model for the 'user' table, needed for authentication[cite: 8].
    """
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    # Store the hashed password
    hashed_password = Column(String, nullable=False) 
    # For Role-Based Access Control (RBAC) [cite: 49]
    role = Column(String, default="user", index=True) 
    is_active = Column(Integer, default=1)
    
    def __repr__(self):
        return f"<User(email='{self.email}', role='{self.role}')>"