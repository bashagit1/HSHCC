# utils/ai_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

# Example: Load health data (this should come from your database or CSV)
def load_data():
    # For demonstration purposes, we use a CSV file or database
    data = pd.read_csv("health_data.csv")  # Replace with your actual data source
    return data

# Train model
def train_model():
    data = load_data()
    # Features and target variable (assuming 'hypertension' is the target column)
    X = [[120, 80, 5.5], [140, 90, 7.0], [130, 85, 6.0]]  # Example features: [BP, HR, Sugar]
    y = [0, 1, 0]  # Example labels: 0 = No Risk, 1 = Risk
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Standardize the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Initialize and train the model
    model = LogisticRegression()
    model.fit(X_train_scaled, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test_scaled)
    print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
    
    # Save the model and scaler
    joblib.dump(model, 'health_model.pkl')
    joblib.dump(scaler, 'scaler.pkl')

# Predict using the trained model
def predict_health_risk(blood_pressure, heart_rate, sugar_level):
    model = joblib.load('health_model.pkl')
    scaler = joblib.load('scaler.pkl')
    
    # Prepare the input data for prediction
    input_data = pd.DataFrame([[blood_pressure, heart_rate, sugar_level]], columns=['blood_pressure', 'heart_rate', 'sugar_level'])
    input_data_scaled = scaler.transform(input_data)
    
    # Predict risk (0 for no risk, 1 for risk)
    prediction = model.predict(input_data_scaled)
    return prediction[0]
