import streamlit as st
from db import SessionLocal
from Repositories.userRepository import userRepository
from Repositories.patientRepository import patientRepository
from Services.userService import UserService
from Services.patientService import PatientService

# -----------------------
# Session state
# -----------------------
if 'user' not in st.session_state:
    st.session_state.user = None

# -----------------------
# Services
# -----------------------
def get_user_service():
    db = SessionLocal()
    return UserService(userRepository(db)), db

def get_patient_service():
    db = SessionLocal()
    return PatientService(patientRepository(db)), db

# -----------------------
# Login / Signup
# -----------------------
if st.session_state.user is None:
    st.title("Hospital Management System")
    action = st.radio("Action", ["Login", "Sign Up"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if action == "Sign Up":
        role = st.selectbox("Role", ["Admin", "Doctor", "Receptionist"])
        if st.button("Sign Up"):
            service, db = get_user_service()
            existing = service.get_user_by_username(username)
            if existing:
                st.error("Username already exists")
            else:
                service.signup(username, password, role)
                db.close()
                st.success("Account created! You can login now.")

    if action == "Login":
        if st.button("Login"):
            service, db = get_user_service()
            user = service.login(username, password)
            db.close()
            if user:
                st.session_state.user = user
                st.success(f"Logged in as {username}")
            else:
                st.error("Invalid username or password")

# -----------------------
# Dashboard
# -----------------------
else:
    user = st.session_state.user
    st.title(f"Welcome, {user.username} ({user.role})")

    if st.button("Logout"):
        st.session_state.user = None
        st.experimental_rerun()

    st.header("Patient Operations")

    # Create Patient
    st.subheader("Add Patient")
    name = st.text_input("Name", key="name")
    age = st.number_input("Age", min_value=0, key="age")
    diagnosis = st.text_input("Diagnosis", key="diag")
    if st.button("Create Patient"):
        service, db = get_patient_service()
        patient = service.create_patient(name, age, diagnosis)
        db.close()
        st.success(f"Patient created with ID {patient.patient_id}")

    # View Patient by ID
    st.subheader("View Patient by ID")
    pid = st.number_input("Patient ID", min_value=1, key="view_id")
    if st.button("Get Patient"):
        service, db = get_patient_service()
        try:
            patient = service.get_patient_by_id(pid, user)
            st.json(patient.__dict__)
        except PermissionError:
            st.error("Access denied")
        db.close()

    # View Anonymized Patient
    st.subheader("View Anonymized Patient")
    pid_anon = st.number_input("Patient ID (Anonymized)", min_value=1, key="view_anon")
    if st.button("Get Anonymized Patient"):
        service, db = get_patient_service()
        try:
            patient = service.get_anonymized_patient_by_id(pid_anon, user)
            st.json(patient)
        except PermissionError:
            st.error("Access denied")
        db.close()
