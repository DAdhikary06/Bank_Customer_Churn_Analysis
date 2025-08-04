# app.py

import streamlit as st
import numpy as np
import pickle

# Load the trained model and preprocessing tools
model = pickle.load(open("model/xgb_model.pkl", "rb"))
scaler = pickle.load(open("model/scaler.pkl", "rb"))
gender_encoder = pickle.load(open("model/gender_encoder.pkl", "rb"))

# Set page config
st.set_page_config(page_title="Customer Churn Predictor", page_icon="💳")
st.title("💳 Bank Customer Churn Prediction App")
st.markdown("Predict whether a bank customer is likely to **churn** based on profile details.")

# === Input Section === #
st.header("📋 Customer Details")

credit_score = st.slider("Credit Score", 300, 850, 650)
gender = st.radio("Gender", ["Male", "Female"])
age = st.slider("Age", 18, 100, 35)
tenure = st.slider("Tenure (Years with Bank)", 0, 10, 5)
balance = st.number_input("Balance in Account", value=50000.0, min_value=0.0)
products_number = st.selectbox("Number of Products", [1, 2, 3, 4])
credit_card = st.selectbox("Has Credit Card?", [1, 0])
active_member = st.selectbox("Is Active Member?", [1, 0])
estimated_salary = st.number_input("Estimated Salary", value=100000.0, min_value=0.0)
country = st.selectbox("Country", ["France", "Germany", "Spain"])

# === Encoding === #
gender_encoded = gender_encoder.transform([gender])[0]
country_germany = 1 if country == "Germany" else 0
country_spain = 1 if country == "Spain" else 0

# === Input Vector === #
input_data = np.array([[credit_score, gender_encoded, age, tenure, balance,
                        products_number, credit_card, active_member,
                        estimated_salary, country_germany, country_spain]])

input_scaled = scaler.transform(input_data)

# === Prediction === #
if st.button("🔍 Predict Churn"):
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0][1]

    if prediction == 1:
        st.error(f"⚠️ The customer is **likely to churn**.\n\nChurn Probability: {probability:.2%}")
    else:
        st.success(f"✅ The customer is **not likely to churn**.\n\nChurn Probability: {probability:.2%}")
