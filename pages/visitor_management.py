import streamlit as st
from utils.database import get_residents, add_visitor, get_visitors, update_visitor_status
from datetime import date

st.title("Visitor Management")

# Select Resident
residents = get_residents()
resident_options = {f"{r[1]} (ID: {r[0]})": r[0] for r in residents}

if resident_options:
    selected_resident = st.selectbox("Select a Resident", options=resident_options.keys())
    if selected_resident:
        resident_id = resident_options[selected_resident]

        # Add Visitor Record
        with st.form("add_visitor_form"):
            st.subheader(f"Add Visitor Record for {selected_resident}")
            visitor_name = st.text_input("Visitor Name")
            visit_date = st.date_input("Visit Date", value=date.today())
            purpose = st.text_area("Purpose of Visit")
            submitted = st.form_submit_button("Add Visitor Record")

            if submitted:
                add_visitor(resident_id, visitor_name, visit_date.strftime("%Y-%m-%d"), purpose)
                st.success(f"Visitor record for {visitor_name} added successfully!")

        # View Visitor Logs
        st.subheader(f"Visitor Logs for {selected_resident}")
        visitors = get_visitors(resident_id)

        if visitors:
            for visitor in visitors:
                visitor_id, name, visit_date, purpose, status = visitor
                st.write(f"**Visitor Name:** {name}")
                st.write(f"**Visit Date:** {visit_date}")
                st.write(f"**Purpose:** {purpose}")
                st.write(f"**Approval Status:** {status}")

                if status == "Pending":
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"Approve {name}", key=f"approve_{visitor_id}"):
                            update_visitor_status(visitor_id, "Approved")
                            st.success(f"Visitor {name} approved!")
                            st.rerun()
                    with col2:
                        if st.button(f"Reject {name}", key=f"reject_{visitor_id}"):
                            update_visitor_status(visitor_id, "Rejected")
                            st.warning(f"Visitor {name} rejected!")
                            st.rerun()
                st.write("---")
        else:
            st.write("No visitor records found for this resident.")
else:
    st.warning("No residents found. Please add residents first.")
