from sqlalchemy import Column, Integer, String, DateTime
from db import Base

class Log(Base):
    
    __tablename__="logs"
    __allow_unmapped__ = True
    
    log_id=Column(Integer,primary_key=True,autoincrement=True)
    user_id=Column(Integer,nullable=False)
    role=Column(String,nullable=False)
    action=Column(String,nullable=False)
    timestamp=Column(DateTime,nullable=False)
    details=Column(String,nullable=True)
    
