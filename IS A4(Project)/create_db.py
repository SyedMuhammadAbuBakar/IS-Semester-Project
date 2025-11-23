from db import Base, engine

import Models

from Models.users import User
from Models.logs import Log
from Models.patients import Patient

Base.metadata.create_all(bind=engine)

print("Database created!")