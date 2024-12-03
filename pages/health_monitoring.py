import streamlit as st
from utils.database import get_residents, add_health_record, get_health_records
from datetime import date

st.title("Health Monitoring")

# Select Resident
residents = get_residents()
resident_options = {f"{r[1]} (ID: {r[0]})": r[0] for r in residents}

if resident_options:
    selected_resident = st.selectbox("Select a Resident", options=resident_options.keys())

    if selected_resident:
        resident_id = resident_options[selected_resident]

        # Add Health Record
        st.subheader("Add Health Record")
        with st.form("add_health_record_form"):
            record_date = st.date_input("Date", value=date.today())
            blood_pressure = st.text_input("Blood Pressure (e.g., 120/80)")
            heart_rate = st.number_input("Heart Rate (bpm)", min_value=0)
            sugar_level = st.number_input("Sugar Level (mg/dL)", min_value=0.0)
            submitted = st.form_submit_button("Add Record")

            if submitted:
                add_health_record(
                    resident_id,
                    record_date.strftime("%Y-%m-%d"),
                    blood_pressure,
                    heart_rate,
                    sugar_level,
                )
                st.success("Health record added successfully!")

        # View Health Records
        st.subheader("Health Records")
        health_records = get_health_records(resident_id)

        if health_records:
            for record in health_records:
                st.write(
                    f"Date: {record[0]}, BP: {record[1]}, Heart Rate: {record[2]} bpm, Sugar: {record[3]} mg/dL"
                )
        else:
            st.write("No health records found.")
else:
    st.warning("No residents found. Please add residents first.")
