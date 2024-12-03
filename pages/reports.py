# pages/reports.py

import streamlit as st
from utils.database import get_residents, get_health_records
import pandas as pd

st.title("Generate Reports")

# Report Options
report_type = st.selectbox("Select Report Type", ["Resident Details", "Health Monitoring", "Activity Plans"])

if report_type == "Resident Details":
    st.subheader("Resident Details Report")
    residents = get_residents()
    
    if residents:
        # Display resident data
        resident_df = pd.DataFrame(residents, columns=["ID", "Name", "Age", "Room Number", "Medical History"])
        st.dataframe(resident_df)
        
        # Download CSV
        csv = resident_df.to_csv(index=False)
        st.download_button("Download CSV", data=csv, file_name="resident_details.csv", mime="text/csv")
    else:
        st.warning("No resident data available.")

elif report_type == "Health Monitoring":
    st.subheader("Health Monitoring Report")
    
    residents = get_residents()
    resident_options = {f"{r[1]} (ID: {r[0]})": r[0] for r in residents}

    if resident_options:
        selected_resident = st.selectbox("Select a Resident", options=resident_options.keys())
        resident_id = resident_options[selected_resident]

        health_records = get_health_records(resident_id)

        if health_records:
            health_df = pd.DataFrame(health_records, columns=["Date", "Blood Pressure", "Heart Rate", "Sugar Level"])
            st.dataframe(health_df)

            # Download CSV
            csv = health_df.to_csv(index=False)
            st.download_button("Download CSV", data=csv, file_name=f"{selected_resident}_health_records.csv", mime="text/csv")
        else:
            st.warning("No health records available for this resident.")
    else:
        st.warning("No residents found. Please add residents first.")

elif report_type == "Activity Plans":
    st.subheader("Activity Plans Report")

    try:
        activity_df = pd.read_csv("utils/activity_data.csv")  # Assuming activity plans are stored in CSV
        st.dataframe(activity_df)

        # Download CSV
        csv = activity_df.to_csv(index=False)
        st.download_button("Download CSV", data=csv, file_name="activity_plans.csv", mime="text/csv")
    except FileNotFoundError:
        st.warning("No activity plan data found. Please add activity plans.")

# End of Reports Page
