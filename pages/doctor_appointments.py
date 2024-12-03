import streamlit as st
from utils.database import get_residents, get_doctors, add_appointment

st.title("Doctor Appointment Management")

# Get residents and doctors
residents = get_residents()
doctors = get_doctors()

if not residents:
    st.warning("No residents found. Please add residents first.")
elif not doctors:
    st.warning("No doctors found. Please add doctors first.")
else:
    # Map residents and doctors to display names
    resident_options = {f"{r[1]} (ID: {r[0]})": r[0] for r in residents}
    doctor_options = {f"Dr. {d[1]} ({d[2]})": d[0] for d in doctors}

    with st.form("appointment_form"):
        selected_resident = st.selectbox("Select Resident", options=resident_options.keys())
        selected_doctor = st.selectbox("Select Doctor", options=doctor_options.keys())
        appointment_date = st.date_input("Select Appointment Date")
        notes = st.text_area("Notes (optional)")
        submitted = st.form_submit_button("Book Appointment")

        if submitted:
            resident_id = resident_options[selected_resident]
            doctor_id = doctor_options[selected_doctor]
            add_appointment(resident_id, doctor_id, str(appointment_date), notes)
            st.success(f"Appointment booked for {selected_resident} with {selected_doctor} on {appointment_date}.")
