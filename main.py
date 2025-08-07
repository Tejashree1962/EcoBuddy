import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get API key from environment
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

# Emission factors
EMISSION_FACTORS = {
    "car_per_km": 0.204,
    "electricity_per_kwh": 0.419,
    "meat_meal": 1.5,
    "short_flight": 750,
    "shopping": {
        "Rarely": 10,
        "Monthly": 30,
        "Weekly": 60
    }
}

st.title("🌍 EcoBuddy - Your AI Carbon Footprint Guide")

# User Inputs
travel_km = st.number_input("🚗 Daily Travel (km)", value=15.0)
electricity_kwh = st.number_input("⚡ Monthly Electricity Usage (kWh)", value=350.0)
meat_meals = st.number_input("🍗 Weekly Meat Meals", value=5.0)
flights = st.number_input("✈️ Flights per Year", value=2.0)
shopping_freq = st.selectbox("🛒 Shopping Frequency", ["Rarely", "Monthly", "Weekly"])

if st.button("Generate Report"):
    car_emission = travel_km * 30 * EMISSION_FACTORS["car_per_km"]
    electricity_emission = electricity_kwh * EMISSION_FACTORS["electricity_per_kwh"]
    meat_emission = meat_meals * 4 * EMISSION_FACTORS["meat_meal"]
    flight_emission = flights * EMISSION_FACTORS["short_flight"] / 12
    shopping_emission = EMISSION_FACTORS["shopping"][shopping_freq]

    total = car_emission + electricity_emission + meat_emission + flight_emission + shopping_emission
    st.markdown(f"### Monthly Emissions: {round(total, 2)} kg CO₂")

    # Gemini Prompt
    prompt = f"""
    You are an AI Sustainability Agent. Based on this user's data, give 3 tips to reduce their carbon footprint:
    - Daily travel: {travel_km} km
    - Electricity: {electricity_kwh} kWh/month
    - Meat meals: {meat_meals}/week
    - Flights: {flights}/year
    - Shopping: {shopping_freq}
    """

    try:
        response = model.generate_content(prompt)
        st.markdown("### Suggestions:")
        st.markdown(response.text.strip())
    except Exception as e:
        st.error(f"Error from Gemini: {e}")
