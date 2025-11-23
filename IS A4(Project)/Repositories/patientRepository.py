from Models.patients import Patient
from sqlalchemy import select

class patientRepository:
    def __init__(self, session):
        self.session = session


    def get_patient_by_id(self, patient_id):
        return self.session.query(Patient).filter(Patient.patient_id == patient_id).first()
    
    
    def get_anonymized_patient_by_id(self, patient_id):
        
        stmt = select(
            Patient.anonymized_name.label("name"),
            Patient.anonymized_contact.label("contact"),
            Patient.anonymized_diagnosis.label("diagnosis")
        ).where(Patient.patient_id == patient_id)

        result = self.session.execute(stmt).first()

        if not result:
            return None
        
        return {
            "name": result.name,
            "contact": result.contact,
            "diagnosis": result.diagnosis
        }
        
        
    def create_patient(self, name, age, diagnosis):
        new_patient = Patient(name=name, age=age, diagnosis=diagnosis)
        self.session.add(new_patient)
        self.session.commit()
        return new_patient

    