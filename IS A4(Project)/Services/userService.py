from Repositories import userRepository
import bcrypt

class UserService:
    def __init__(self,userRepository:userRepository.userRepository):
        self.user_repository = userRepository

    def get_user_by_id(self, user_id):
        return self.user_repository.get_user_by_id(user_id)
    
    def get_user_by_username(self, username):
        return self.user_repository.get_user_by_username(username)
    
    def signup(self, username, password, role):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        return self.user_repository.create_user(username, hashed_password, role)
    
    def login(self, username, password):
        user = self.user_repository.get_user_by_username(username)
        status = bcrypt.checkpw((password).encode('utf-8'),user.hashed_password.encode('utf-8'))
        if user and status:
            return user
        return None