import streamlit as st
from utils.database import get_residents, add_meal_plan, get_meal_plans_for_resident
from datetime import date

st.title("Nutrition and Meal Management")

# Select Resident
residents = get_residents()
resident_options = {f"{r[1]} (ID: {r[0]})": r[0] for r in residents}

if resident_options:
    selected_resident = st.selectbox("Select a Resident", options=resident_options.keys())

    if selected_resident:
        resident_id = resident_options[selected_resident]

        # Add Meal Plan
        st.subheader("Assign a Meal Plan")
        with st.form("add_meal_plan_form"):
            date_str = st.date_input("Date", date.today())
            breakfast = st.text_input("Breakfast")
            lunch = st.text_input("Lunch")
            dinner = st.text_input("Dinner")
            snacks = st.text_input("Snacks")
            submitted = st.form_submit_button("Assign Meal Plan")

            if submitted:
                add_meal_plan(resident_id, date_str.strftime("%Y-%m-%d"), breakfast, lunch, dinner, snacks)
                st.success(f"Meal plan for {selected_resident} on {date_str} added successfully!")

        # View Meal Plans
        st.subheader("Meal Plans for This Resident")
        meal_plans = get_meal_plans_for_resident(resident_id)

        if meal_plans:
            for plan in meal_plans:
                st.write(f"Date: {plan[0]} | Breakfast: {plan[1]} | Lunch: {plan[2]} | Dinner: {plan[3]} | Snacks: {plan[4]}")
        else:
            st.write("No meal plans found.")
else:
    st.warning("No residents found. Please add residents first.")
