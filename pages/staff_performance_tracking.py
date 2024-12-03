import streamlit as st
from utils.database import get_all_staff, get_staff_performance, add_staff_performance
from datetime import date

st.title("Staff Performance Tracking")

# Fetch Staff Data from Database
staff_list = get_all_staff()
if staff_list:
    staff_options = {staff[1]: staff[0] for staff in staff_list}

    # Select Staff Member
    selected_staff = st.selectbox("Select a Staff Member", options=staff_options.keys())
    if selected_staff:
        staff_id = staff_options[selected_staff]

        # Add Performance Record
        with st.form("add_performance_form"):
            st.subheader(f"Add Performance Record for {selected_staff}")
            task = st.text_input("Task Assigned")
            completion_status = st.selectbox("Completion Status", ["Pending", "Completed"])
            feedback = st.text_area("Feedback")
            performance_date = st.date_input("Performance Date", value=date.today())
            submitted = st.form_submit_button("Add Performance Record")

            if submitted:
                add_staff_performance(
                    staff_id, task, completion_status, feedback, performance_date.strftime("%Y-%m-%d")
                )
                st.success(f"Performance record for {selected_staff} added successfully!")

        # View Performance Records
        st.subheader(f"Performance Records for {selected_staff}")
        performance_records = get_staff_performance(staff_id)

        if performance_records:
            for record in performance_records:
                task, status, feedback, performance_date = record
                st.write(f"**Task:** {task}")
                st.write(f"**Status:** {status}")
                st.write(f"**Feedback:** {feedback if feedback else 'No feedback provided'}")
                st.write(f"**Date:** {performance_date}")
                st.write("---")
        else:
            st.write("No performance records found for this staff member.")
else:
    st.warning("No staff data found. Please add staff members first.")
