from sqlalchemy import Column, Integer, String, Date
from db import Base

class Patient(Base):
    
    __tablename__="patients"
    __allow_unmapped__ = True
    
    patient_id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String,nullable=False)
    age=Column(Integer,nullable=False)
    contact=Column(Integer,nullable=False)
    diagnosis=Column(String,nullable=False)
    anonymized_name=Column(String,nullable=False)
    anonymized_contact=Column(Integer,nullable=False)
    date_added=Column(Date,nullable=False)
    anonymized_diagnosis=Column(String,nullable=False)