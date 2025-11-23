import streamlit as st
from db import SessionLocal
from Repositories.userRepository import userRepository
from Repositories.patientRepository import patientRepository
from Repositories.logsRepository import logRepository
from Services.userService import UserService
from Services.patientService import PatientService
from Services.logService import logService

# -----------------------
# Session state
# -----------------------
if 'user' not in st.session_state:
    st.session_state.user = None

# -----------------------
# Service Providers
# -----------------------
def get_user_service():
    db = SessionLocal()
    return UserService(userRepository(db)), db

def get_patient_service():
    db = SessionLocal()
    return PatientService(patientRepository(db)), db

def get_log_service():
    db = SessionLocal()
    return logService(logRepository(db)), db

# -----------------------
# LOGIN / SIGNUP
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
                st.success("Account created! Please login.")
            db.close()

    if action == "Login":
        if st.button("Login"):
            service, db = get_user_service()
            user = service.login(username, password)
            db.close()
            if user:
                st.session_state.user = user
                st.success(f"Logged in as {username}")
                st.rerun()
            else:
                st.error("Invalid username or password")

# -----------------------
# DASHBOARD
# -----------------------
else:
    user = st.session_state.user
    st.title(f"Welcome, {user.username} ({user.role})")

    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()

    st.divider()
    st.subheader("Select Operation")

    options = ["Add Patient", "View Patient", "View Anonymized Patient"]
    if user.role == "Admin":
        options.append("View Logs")

    operation = st.radio("Menu", options)
    st.divider()

    # ------------------- ADD PATIENT -------------------
    if operation == "Add Patient":
        if str(user.role) == "Doctor":
            st.error("Doctors cannot add patients.")
        else:
            st.subheader("Add Patient")
            name = st.text_input("Name", key="name")
            age = st.number_input("Age", min_value=1, max_value=120, key="age")
            contact = st.text_input("Contact", key="contact")
            diagnosis = st.text_input("Diagnosis", key="diag")

            if st.button("Create Patient"):
                if not name or not contact or not diagnosis:
                    st.error("Name, Contact, and Diagnosis are required!")
                else:
                    service, db = get_patient_service()
                    try:
                        patient = service.create_patient(name, age, contact, diagnosis, user)
                        db.refresh(patient)
                        patient_id = patient.patient_id
                        st.success(f"Patient created with ID {patient_id}")
                    except PermissionError as e:
                        st.error(str(e))
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                    finally:
                        db.close()

    # ------------------- VIEW PATIENT -------------------
    elif operation == "View Patient":
        if str(user.role) != "Admin":
            st.error("Only Admins can view raw patient data.")
        else:
            st.subheader("View Raw Patient Data")
            pid = st.number_input("Enter Patient ID", min_value=1, key="view_id")
            if st.button("Get Patient"):
                service, db = get_patient_service()
                try:
                    patient = service.get_patient_by_id(pid, user)
                    if patient:
                        st.json({
                            "patient_id": patient.patient_id,
                            "name": patient.name,
                            "age": patient.age,
                            "contact": patient.contact,
                            "diagnosis": patient.diagnosis,
                            "date_added": str(patient.date_added)
                        })
                    else:
                        st.error("Patient not found")
                except PermissionError as e:
                    st.error(str(e))
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                finally:
                    db.close()

    # ------------------- VIEW ANONYMIZED PATIENT -------------------
    elif operation == "View Anonymized Patient":
        if user.role not in ["Admin", "Doctor"]:
            st.error("Receptionists cannot view patient data.")
        else:
            st.subheader("View Anonymized Patient Data")
            pid = st.number_input("Patient ID (Anonymized)", min_value=1, key="anon_id")
            if st.button("Get Anonymized Data"):
                service, db = get_patient_service()
                try:
                    patient = service.get_anonymized_patient_by_id(pid, user)
                    if patient:
                        st.json(patient)
                    else:
                        st.error("Patient not found")
                except PermissionError as e:
                    st.error(str(e))
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                finally:
                    db.close()

    # ------------------- VIEW LOGS -------------------
    elif operation == "View Logs":
        if user.role != "Admin":
            st.error("Only Admins can view logs.")
        else:
            st.subheader("System Logs")
            service, db = get_log_service()
            try:
                logs = service.get_all_logs(user)
                if logs:
                    for log in logs:
                        st.write(f"{log.timestamp} - {log.action} - User: {log.username}")
                else:
                    st.info("No logs found")
            except PermissionError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"Error: {str(e)}")
            finally:
                db.close()