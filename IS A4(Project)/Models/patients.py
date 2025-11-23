from sqlalchemy import Column, Integer, String, DateTime
from db import Base
from datetime import datetime

class Patient(Base):
    
    __tablename__ = "patients"
    __allow_unmapped__ = True
    
    patient_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    contact = Column(String, nullable=True)  
    diagnosis = Column(String, nullable=False)
    anonymized_name = Column(String, nullable=True)
    anonymized_contact = Column(String, nullable=True)
    date_added = Column(DateTime, default=datetime.utcnow, nullable=False)
    anonymized_diagnosis = Column(String, nullable=True)