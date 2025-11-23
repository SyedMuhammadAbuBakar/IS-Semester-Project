from Models.logs import Log
from Models.users import User

class logRepository:
    def __init__(self, session):
        self.session = session

    def create_log(self, action, user: User):
        new_log = Log(user_id=user.user_id,action=action,role=user.role,username=user.username)
        self.session.add(new_log)
        self.session.commit()
        return new_log
    
    def get_all_logs(self):
        return self.session.query(Log).all()