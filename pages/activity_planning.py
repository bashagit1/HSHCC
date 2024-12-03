import streamlit as st
from utils.database import get_residents, add_activity_plan, get_activities_for_resident
from datetime import date, datetime

st.title("Activity Planning")

# Select Resident
residents = get_residents()
resident_options = {f"{r[1]} (ID: {r[0]})": r[0] for r in residents}

if resident_options:
    selected_resident = st.selectbox("Select a Resident", options=resident_options.keys())

    if selected_resident:
        resident_id = resident_options[selected_resident]

        # Add Activity Plan
        st.subheader("Assign an Activity Plan")
        with st.form("add_activity_form"):
            date_str = st.date_input("Date", date.today())
            activity_name = st.text_input("Activity Name")
            activity_type = st.selectbox("Activity Type", ["Physical", "Mental", "Recreational", "Social", "Other"])
            description = st.text_area("Activity Description")
            
            # Set default time to 10:00 AM
            default_time = datetime.combine(date.today(), datetime.min.time()).replace(hour=10, minute=0)
            time = st.time_input("Activity Time", value=default_time.time())
            
            submitted = st.form_submit_button("Assign Activity Plan")

            if submitted:
                add_activity_plan(resident_id, date_str.strftime("%Y-%m-%d"), activity_name, activity_type, description, time.strftime("%H:%M"))
                st.success(f"Activity plan for {selected_resident} on {date_str} added successfully!")

        # View Activity Plans
        st.subheader("Activity Plans for This Resident")
        activities = get_activities_for_resident(resident_id)

        if activities:
            for activity in activities:
                st.write(f"Date: {activity[0]} | Activity: {activity[1]} | Type: {activity[2]} | Time: {activity[4]} | Description: {activity[3]}")
        else:
            st.write("No activity plans found.")
else:
    st.warning("No residents found. Please add residents first.")
