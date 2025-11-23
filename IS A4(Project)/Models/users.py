from sqlalchemy import Column, Integer, String
from db import Base

class User(Base):
    
    __tablename__ = "users"
    __allow_unmapped__ = True  

    user_id = Column(Integer, primary_key=True, autoincrement=True) 
    username = Column(String, nullable=False)                       
    hashed_password = Column(String, nullable=False)
    password : String
    role = Column(String, nullable=False)
    

    
    
