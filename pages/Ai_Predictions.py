# pages/ai_predictions.py

import streamlit as st
from utils.database import get_residents, get_health_records
from utils.ai_model import predict_health_risk

st.title("AI Predictions for Resident Health")

# Select a Resident
residents = get_residents()
resident_options = {f"{r[1]} (ID: {r[0]})": r[0] for r in residents}

if resident_options:
    selected_resident = st.selectbox("Select a Resident", options=resident_options.keys())

    if selected_resident:
        resident_id = resident_options[selected_resident]

        # Fetch the most recent health record
        health_records = get_health_records(resident_id)
        
        if health_records:
            # Use the latest health record for prediction
            latest_record = health_records[0]
            blood_pressure, heart_rate, sugar_level = latest_record[1], latest_record[2], latest_record[3]

            # Show the latest health data
            st.write(f"Blood Pressure: {blood_pressure}")
            st.write(f"Heart Rate: {heart_rate}")
            st.write(f"Sugar Level: {sugar_level}")

            # Make prediction
            prediction = predict_health_risk(blood_pressure, heart_rate, sugar_level)
            risk_status = "Risk of Hypertension" if prediction == 1 else "No Risk"
            st.write(f"AI Prediction: {risk_status}")

        else:
            st.write("No health records found for this resident.")
else:
    st.warning("No residents found. Please add residents first.")
