import streamlit as st
from utils.database import get_residents, add_message, get_messages_for_resident
from datetime import date

st.title("Family Communication Portal")

# Select Resident
residents = get_residents()
resident_options = {f"{r[1]} (ID: {r[0]})": r[0] for r in residents}

if resident_options:
    selected_resident = st.selectbox("Select a Resident", options=resident_options.keys())

    if selected_resident:
        resident_id = resident_options[selected_resident]

        # Send a Message
        st.subheader("Send a Message to Caregiver/Staff")
        with st.form("send_message_form"):
            sender_name = st.text_input("Your Name (Family Member)")
            receiver_name = st.text_input("Receiver Name (Caregiver/Staff)")
            message = st.text_area("Message")
            submitted = st.form_submit_button("Send Message")

            if submitted:
                add_message(sender_name, receiver_name, message, date.today().strftime("%Y-%m-%d"), resident_id)
                st.success("Message sent successfully!")

        # View Messages
        st.subheader("Messages for This Resident")
        messages = get_messages_for_resident(resident_id)

        if messages:
            for msg in messages:
                st.write(f"From: {msg[0]} to {msg[1]} on {msg[3]}: {msg[2]}")
        else:
            st.write("No messages found.")
else:
    st.warning("No residents found. Please add residents first.")
