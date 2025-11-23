from Repositories.patientRepository import patientRepository
from Models.users import User

class PatientService:
    def __init__(self, patientRepository: patientRepository):
        self.patient_repository = patientRepository

    def get_patient_by_id(self, patient_id, user: User):
        if str(user.role) != "Admin":
            raise PermissionError("Access denied: Admins only")
        return self.patient_repository.get_patient_by_id(patient_id, user)

    def get_anonymized_patient_by_id(self, patient_id, user: User):
        if user.role not in ["Admin", "Doctor"]:
            raise PermissionError("Access denied: Admins and Doctors only")
        return self.patient_repository.get_anonymized_patient_by_id(patient_id, user)

    def create_patient(self, name, age, contact, diagnosis, user: User):
        if user.role not in ["Admin", "Receptionist"]:
            raise PermissionError("Access denied: Doctors cannot add patients")
        return self.patient_repository.create_patient(name, age, contact, diagnosis, user)