import streamlit as st
from utils.database import add_staff, get_staff

st.title("Staff Management")

# Add new staff member
with st.form("add_staff_form"):
    name = st.text_input("Name")
    role = st.text_input("Role (e.g., Nurse, Caregiver)")
    assigned_residents = st.text_input("Assigned Residents (Comma-separated Resident IDs)")
    contact_info = st.text_input("Contact Info (e.g., phone number or email)")
    submitted = st.form_submit_button("Add Staff")

    if submitted:
        add_staff(name, role, assigned_residents, contact_info)
        st.success(f"Staff member {name} added successfully!")

# Display all staff members
st.subheader("All Staff Members")
staff = get_staff()
for member in staff:
    st.write(f"ID: {member[0]}, Name: {member[1]}, Role: {member[2]}, Assigned Residents: {member[3]}, Contact: {member[4]}")
