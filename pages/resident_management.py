import streamlit as st
from utils.database import add_resident, get_residents

st.title("Resident Management")

# Add new resident
with st.form("add_resident_form"):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    room_number = st.text_input("Room Number")
    medical_history = st.text_area("Medical History")
    submitted = st.form_submit_button("Add Resident")

    if submitted:
        add_resident(name, age, room_number, medical_history)
        st.success(f"Resident {name} added successfully!")

# Display all residents
st.subheader("All Residents")
residents = get_residents()
for resident in residents:
    st.write(f"ID: {resident[0]}, Name: {resident[1]}, Age: {resident[2]}, Room: {resident[3]}")
