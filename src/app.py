# src/app.py

import streamlit as st
import requests

def main():
    st.title("Government Hackathon Project")
    st.write("This Streamlit app interacts with the FastAPI backend to make predictions.")

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Choose a page", ["Home", "Model Prediction"])

    if page == "Home":
        st.write("Welcome to the home page!")
        st.write("Use the navigation menu to make predictions.")

    elif page == "Model Prediction":
        st.header("Model Prediction")

        # User input
        st.write("Enter the data for prediction:")
        input_data = st.text_input("Input Data")

        # Predict button
        if st.button("Predict"):
            if input_data:
                try:
                    # Send data to FastAPI backend
                    response = requests.post("http://localhost:8000/predict/", json={"input_data": input_data})
                    response.raise_for_status()
                    prediction = response.json().get("prediction")
                    st.write(f"Prediction result: {prediction}")
                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.warning("Please enter some input data.")

if __name__ == "__main__":
    main()
