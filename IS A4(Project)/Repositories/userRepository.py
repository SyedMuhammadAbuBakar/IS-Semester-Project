from Models import users

class userRepository:
    def __init__(self, session):
        self.session = session

    def get_user_by_username(self, username):
        return self.session.query(users.User).filter(users.User.username == username).first()   
    
    def get_user_by_id(self, user_id):
        return self.session.query(users.User).filter(users.User.user_id == user_id).first()
    
    def create_user(self, username, hashed_password, role):
        new_user = users.User(username=username, hashed_password=hashed_password, role=role)
        self.session.add(new_user)
        self.session.commit()
        return new_user