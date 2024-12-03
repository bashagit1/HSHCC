import streamlit as st
from pathlib import Path
from utils.database import init_db
from utils.auth import hash_password, verify_password, get_user

# Initialize the database on app start
init_db()

# State for login session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None


# Function for login
def show_login():
    st.title("CareSeniors - Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            user = get_user(username)
            if user and verify_password(password, user[2]):  # Check hashed password
                st.session_state.logged_in = True
                st.session_state.role = user[3]  # Role from database (e.g., admin, staff, family)
                st.session_state.username = user[1]  # Username
                st.success("Login successful!")
                st.rerun()  # Reload app with login session
            else:
                st.error("Invalid username or password!")


# Function for logout
def show_logout():
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.username = None
        st.rerun()


# Function to display the dashboard based on role
def show_dashboard():
    st.sidebar.title("Navigation")
    st.sidebar.write(f"Logged in as: {st.session_state.username} ({st.session_state.role})")
    show_logout()

    if st.session_state.role == "admin":
        st.title("Welcome to Admin Dashboard")
        # Add admin-specific content here
        page = st.sidebar.radio(
            "Navigate",
            (
                "Resident Management",
                "Health Monitoring",
                "Staff Management",
                "family Portal",
                "Reports",
                "Ai Predictions",
                "Cognitive Stimulation",
                "Activity Planning",
                "Nutrition Management",
                "Smart Room Integration",
                "Medication Management",
                "Visitor Management",
                "Staff Performance Tracking",
                "Doctor Appointment Booking",
                
            ),
        )
    elif st.session_state.role == "staff":
        st.title("Welcome to Staff Dashboard")
        # Staff has limited navigation options
        page = st.sidebar.radio(
            "Navigate",
            (
                "Resident Management",
                "Health Monitoring",
                "Activity Planning",
                "Visitor Management",
            ),
        )
    elif st.session_state.role == "family":
        st.title("Welcome to Family Dashboard")
        # Family can only access family portal
        page = st.sidebar.radio(
            "Navigate",
            ("Family Portal",),
        )

    # Dynamically load pages
    if page == "Resident Management":
        exec(Path("pages/resident_management.py").read_text())
    elif page == "Health Monitoring":
        exec(Path("pages/health_monitoring.py").read_text())
    elif page == "Staff Management":
        exec(Path("pages/staff_management.py").read_text())
    elif page == "family Portal":
        exec(Path("pages/family_portal.py").read_text())
    elif page == "Reports":
        exec(Path("pages/reports.py").read_text())
    elif page == "AI Predictions":
        exec(Path("pages/Ai_predictions.py").read_text())
    elif page == "Cognitive Stimulation":
        exec(Path("pages/cognitive_stimulation.py").read_text())
    elif page == "Activity Planning":
        exec(Path("pages/activity_planning.py").read_text())
    elif page == "Nutrition Management":
        exec(Path("pages/Nutrition_Management.py").read_text())
    elif page == "Smart Room Integration":
        exec(Path("pages/smart_room_integration.py").read_text())
    elif page == "Medication Management":
        exec(Path("pages/medication_management.py").read_text())
    elif page == "Visitor Management":
        exec(Path("pages/visitor_management.py").read_text())
    elif page == "Staff Performance Tracking":
        exec(Path("pages/staff_performance_tracking.py").read_text())
    elif page == "Doctor Appointment Booking":
        exec(Path("pages/doctor_appointments.py").read_text())
    
      


# Main App Logic
if not st.session_state.logged_in:
    show_login()
else:
    show_dashboard()
