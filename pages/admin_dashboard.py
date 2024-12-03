import streamlit as st
from pathlib import Path

# Admin Dashboard
st.title("Admin Dashboard")
st.sidebar.subheader("Admin Menu")

# Navigation Options
menu = st.sidebar.radio(
    "Go to:",
    ["Resident Management", "Staff Management", "Family Member Portal", "Reports", "Settings"]
)

# Display selected page
if menu == "Resident Management":
    st.subheader("Manage Residents")
    # Link to resident management page
    exec(Path("pages/resident_management.py").read_text())

elif menu == "Staff Management":
    st.subheader("Manage Staff")
    # Link to staff management page
    exec(Path("pages/staff_management.py").read_text())

elif menu == "Family Member Portal":
    st.subheader("Family Member Portal")
    # Link to family portal page
    exec(Path("pages/family_portal.py").read_text())

elif menu == "Reports":
    st.subheader("Reports")
    # Link to reports page
    exec(Path("pages/reports.py").read_text())

elif menu == "Settings":
    st.subheader("Settings")
    st.write("Configure app settings here.")
    # Add any additional admin settings here.

st.write("Quick Actions")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Add New Resident"):
        st.experimental_rerun()
        exec(Path("pages/resident_management.py").read_text())  # Redirect to resident management

with col2:
    if st.button("View Reports"):
        st.experimental_rerun()
        exec(Path("pages/reports.py").read_text())  # Redirect to reports

with col3:
    if st.button("Manage Staff"):
        st.experimental_rerun()
        exec(Path("pages/staff_management.py").read_text())  # Redirect to staff management
