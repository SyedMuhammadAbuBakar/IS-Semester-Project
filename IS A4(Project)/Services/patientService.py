from Repositories.patientRepository import patientRepository
from Models.users import User

class PatientService:
    def __init__(self, patientRepository: patientRepository):
        self.patient_repository = patientRepository

    def get_patient_by_id(self, patient_id,user:User):
        if str(user.role) != "Admin":#RBAC check
            raise PermissionError("Access denied: Admins only")
        else:
            return self.patient_repository.get_patient_by_id(patient_id)
           
    def get_anonymized_patient_by_id(self, patient_id,user:User):
        if  str(user.role) != "Admin" and str(user.role) != "Doctor":#RBAC check
            raise PermissionError("Access denied: Admins and Doctors only")
        
        else:#Return anonymized data
            return self.patient_repository.get_anonymized_patient_by_id(patient_id)
          
            
    def create_patient(self, name, age, diagnosis):
        
        
        return self.patient_repository.create_patient(name, age, diagnosis)