import streamlit as st
from utils.database import get_residents, add_smart_room_data, get_smart_room_data
from datetime import datetime

st.title("Smart Room Integration")

# Select Resident
residents = get_residents()
resident_options = {f"{r[1]} (ID: {r[0]})": r[0] for r in residents}

if resident_options:
    selected_resident = st.selectbox("Select a Resident", options=resident_options.keys())

    if selected_resident:
        resident_id = resident_options[selected_resident]

        # Display and Update Smart Room Data
        st.subheader(f"Smart Room Data for {selected_resident}")

        # Fetch current smart room data
        room_data = get_smart_room_data(resident_id)

        if room_data:
            room_temperature, light_status, motion_status, last_updated = room_data
            st.write(f"Current Room Temperature: {room_temperature} °C")
            st.write(f"Light Status: {light_status}")
            st.write(f"Motion Status: {motion_status}")
            st.write(f"Last Updated: {last_updated}")
        else:
            st.write("No smart room data found.")

        # Update Smart Room Data
        st.subheader("Update Smart Room Data")

        with st.form("update_smart_room_form"):
            # Get initial values for inputs from existing data
            room_temperature = st.number_input(
                "Room Temperature (°C)", 
                min_value=15.0,  # Use float
                max_value=30.0,  # Use float
                value=room_temperature if room_data else 22.0  # Default if no data
            )

            # Ensure light_status and motion_status are initialized
            light_status = st.selectbox("Light Status", ["On", "Off"], index=0 if room_data and light_status == "On" else 1)
            motion_status = st.selectbox("Motion Status", ["Active", "Inactive"], index=0 if room_data and motion_status == "Active" else 1)

            # Current timestamp for 'last_updated'
            last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Add the submit button inside the form
            submitted = st.form_submit_button("Update Smart Room Data")

            # When the form is submitted, update the smart room data
            if submitted:
                add_smart_room_data(resident_id, room_temperature, light_status, motion_status, last_updated)
                st.success(f"Smart room data for {selected_resident} updated successfully!")

else:
    st.warning("No residents found. Please add residents first.")
