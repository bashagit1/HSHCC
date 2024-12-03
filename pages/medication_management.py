import streamlit as st
from utils.database import get_residents, add_medication, get_medications
from datetime import datetime

st.title("Medication Management")

# Select Resident
residents = get_residents()
resident_options = {f"{r[1]} (ID: {r[0]})": r[0] for r in residents}

if resident_options:
    selected_resident = st.selectbox("Select a Resident", options=resident_options.keys())
    if selected_resident:
        resident_id = resident_options[selected_resident]

        # Add New Medication
        with st.form("add_medication_form"):
            st.subheader(f"Add Medication for {selected_resident}")
            medication_name = st.text_input("Medication Name")
            dosage = st.text_input("Dosage")
            frequency = st.text_input("Frequency (e.g., Once Daily, Every 8 hours)")
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")
            reminder_times = st.text_input("Reminder Times (comma-separated, e.g., 08:00, 14:00)")

            submitted = st.form_submit_button("Add Medication")
            if submitted:
                add_medication(
                    resident_id,
                    medication_name,
                    dosage,
                    frequency,
                    start_date.strftime("%Y-%m-%d"),
                    end_date.strftime("%Y-%m-%d"),
                    reminder_times
                )
                st.success("Medication added successfully!")

        # View Resident's Medications
        st.subheader(f"Medications for {selected_resident}")
        medications = get_medications(resident_id)
        if medications:
            for med in medications:
                st.write(f"**Medication Name:** {med[1]}")
                st.write(f"**Dosage:** {med[2]}")
                st.write(f"**Frequency:** {med[3]}")
                st.write(f"**Duration:** {med[4]} to {med[5]}")
                st.write(f"**Reminders:** {med[6]}")
                st.write("---")
        else:
            st.write("No medications found for this resident.")
else:
    st.warning("No residents found. Please add residents first.")
