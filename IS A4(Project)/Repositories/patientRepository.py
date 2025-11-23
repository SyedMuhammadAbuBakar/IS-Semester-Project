from Models.patients import Patient
from Models.logs import Log
from sqlalchemy import select

class patientRepository:
    def __init__(self, session):
        self.session = session

    def get_patient_by_id(self, patient_id, user):
        if user.role != "Admin":
            raise PermissionError("Access denied: Admins only")

        self.session.add(Log(user_id=user.user_id, role=user.role, action=f"Accessed patient ID {patient_id}"))
        self.session.commit()

        return self.session.query(Patient).filter(Patient.patient_id == patient_id).first()

    def get_anonymized_patient_by_id(self, patient_id, user):
        if user.role not in ["Admin", "Doctor"]:
            raise PermissionError("Access denied: Receptionists cannot view patient data")

        stmt = select(
            Patient.anonymized_name.label("name"),
            Patient.anonymized_contact.label("contact"),
            Patient.diagnosis.label("diagnosis")
        ).where(Patient.patient_id == patient_id)

        result = self.session.execute(stmt).first()

        self.session.add(Log(user_id=user.user_id, role=user.role, action=f"Accessed anonymized patient ID {patient_id}"))
        self.session.commit()

        if not result:
            return None

        return {
            "name": result.name,
            "contact": result.contact,
            "diagnosis": result.diagnosis
        }

    def create_patient(self, name, age, contact, diagnosis, user):
        if user.role not in ["Admin", "Receptionist"]:
            raise PermissionError("Access denied: Doctors cannot add patients")

        new_patient = Patient(
            name=name, 
            age=age, 
            contact=contact, 
            diagnosis=diagnosis
        )
        self.session.add(new_patient)
        self.session.flush()
        
        new_patient.anonymized_name = f"PATIENT_{new_patient.patient_id}" #type: ignore
        new_patient.anonymized_contact = "XX-XXX-XXXX" # type: ignore
        new_patient.anonymized_diagnosis = diagnosis
        
        self.session.add(Log(user_id=user.user_id, role=user.role, action=f"Added patient ID {new_patient.patient_id}"))
        self.session.commit()
        
        return new_patient