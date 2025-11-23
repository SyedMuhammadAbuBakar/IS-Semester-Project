import streamlit as st
import bcrypt
from db import SessionLocal
from Models.users import User
from datetime import datetime

st.set_page_config(page_title="Hospital Login", layout="centered")

# Session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Simple login
st.title("🏥 Hospital Login")

if not st.session_state.logged_in:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username and password:
            # Direct database query (no service layer)
            db = SessionLocal()
            user = db.query(User).filter(User.username == username).first()
            
            if user:
                # Check password
                if bcrypt.checkpw(password.encode(), user.hashed_password.encode()):
                    st.session_state.logged_in = True
                    st.session_state.user = user.username
                    st.success("Logged in!")
                    st.rerun()
                else:
                    st.error("Wrong password")
            else:
                st.error("User not found")
            
            db.close()
        else:
            st.warning("Enter username and password")
    
    # Signup section
    st.divider()
    st.subheader("Create Account")
    
    new_user = st.text_input("New Username", key="signup_user")
    new_pass = st.text_input("New Password", type="password", key="signup_pass")
    role = st.selectbox("Role", ["admin", "doctor", "receptionist"])
    
    if st.button("Sign Up"):
        if new_user and new_pass:
            db = SessionLocal()
            
            # Check if exists
            existing = db.query(User).filter(User.username == new_user).first()
            if existing:
                st.error("Username exists")
            else:
                # Create user
                hashed = bcrypt.hashpw(new_pass.encode(), bcrypt.gensalt())
                user = User(
                    username=new_user,
                    hashed_password=hashed.decode(),
                    role=role
                )
                db.add(user)
                db.commit()
                st.success("Account created! Please login.")
            
            db.close()

else:
    st.success(f"Welcome, {st.session_state.user}!")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()