import streamlit as st
from utils.database import get_residents, add_cognitive_activity, get_cognitive_activities_for_resident
from datetime import date

st.title("Cognitive Stimulation")

# Select Resident
residents = get_residents()
resident_options = {f"{r[1]} (ID: {r[0]})": r[0] for r in residents}

if resident_options:
    selected_resident = st.selectbox("Select a Resident", options=resident_options.keys())

    if selected_resident:
        resident_id = resident_options[selected_resident]

        # Add Cognitive Activity
        st.subheader("Assign a Cognitive Activity")
        with st.form("add_cognitive_activity_form"):
            date_str = st.date_input("Date", date.today())
            activity_type = st.selectbox("Activity Type", ["Memory Game", "Puzzle", "Quiz", "Math Exercise", "Reading"])
            time_spent = st.number_input("Time Spent (in minutes)", min_value=1, max_value=120, value=30)
            description = st.text_area("Activity Description")
            submitted = st.form_submit_button("Assign Cognitive Activity")

            if submitted:
                add_cognitive_activity(resident_id, date_str.strftime("%Y-%m-%d"), activity_type, time_spent, description)
                st.success(f"Cognitive activity for {selected_resident} on {date_str} added successfully!")

        # View Cognitive Activities
        st.subheader("Cognitive Activities for This Resident")
        activities = get_cognitive_activities_for_resident(resident_id)

        if activities:
            for activity in activities:
                st.write(f"Date: {activity[0]} | Activity: {activity[1]} | Time Spent: {activity[2]} minutes | Description: {activity[3]}")
        else:
            st.write("No cognitive activities found.")
else:
    st.warning("No residents found. Please add residents first.")
