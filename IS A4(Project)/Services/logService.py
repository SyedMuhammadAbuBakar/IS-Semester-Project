from Repositories.logsRepository import logRepository
from Models.users import User

class logService:
    def __init__(self, logRepository: logRepository):
        self.log_repository = logRepository

    def create_log(self, action, user:User):
        if str(user.role) != "Admin":#RBAC check
            raise PermissionError("Access denied: Admins only") 
        else:
            return self.log_repository.create_log(action,user)
    
    def get_all_logs(self,user:User):
        if str(user.role)!= "Admin":#RBAC check
            raise PermissionError("Access denied: Admins only")
        return self.log_repository.get_all_logs()