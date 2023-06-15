import streamlit as st
import requests
import pandas as pd

# Constants
API_URL = "http://localhost:8000"

# Streamlit web application
def main():
    st.title("Heart Disease Prediction")

    # Sidebar navigation
    page = st.sidebar.selectbox("Page", ["Make a Prediction", "Past Predictions"])

    if page == "Make a Prediction":
        make_prediction_page()
    elif page == "Past Predictions":
        past_predictions_page()


def make_prediction_page():
    st.header("Make a Prediction")
    age = st.number_input("Age")
    restingBP = st.number_input("Resting Blood Pressure")
    oldpeak = st.number_input("Oldpeak")
    sex = st.selectbox("Sex", ["M", "F"])
    chestpaintype = st.selectbox(
        "Chest Pain Type", ["Typical Angina", "Atypical Angina", "Non-Anginal Pain", "Asymptomatic"]
    )
    fastingBS = st.selectbox("Fasting Blood Sugar", ["Yes", "No"])
    exerciseAngina = st.selectbox("Exercise-Induced Angina", ["Yes", "No"])
    st_slope = st.selectbox("ST Slope", ["Up", "Flat", "Down"])

    if st.button("Predict"):
        # Prepare data for prediction
        data = {
            "age": age,
            "restingBP": restingBP,
            "oldpeak": oldpeak,
            "sex": sex,
            "chestpaintype": chestpaintype,
            "fastingBS": fastingBS,
            "exerciseAngina": exerciseAngina,
            "st_slope": st_slope,
        }

        # Make prediction API call
        response = requests.post(f"{API_URL}/predict", json=data)
        if response.status_code == 200:
            result = response.json()
            prediction = "You have Heart Disease" if result["prediction"] == 1 else "You don't have Heart Disease"
            st.success(f"Prediction: {prediction}")
            st.success(f"Probability: {result['probability']}%")
        else:
            st.error("Prediction failed.")

    # Upload CSV file for multiple predictions
    st.header("Upload CSV File for Multiple Predictions")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(df)  # Display the uploaded data frame

        if st.button("Predict All"):
            # Perform predictions for each row in the data frame
            predictions = []
            probabilities = []
            for _, row in df.iterrows():
                data = {
                    "age": row["age"],
                    "restingBP": row["restingBP"],
                    "oldpeak": row["oldpeak"],
                    "sex": row["sex"],
                    "chestpaintype": row["chestpaintype"],
                    "fastingBS": row["fastingBS"],
                    "exerciseAngina": row["exerciseAngina"],
                    "st_slope": row["st_slope"],
                }
                response = requests.post(f"{API_URL}/predict", json=data)
                if response.status_code == 200:
                    result = response.json()
                    prediction = "You have Heart Disease" if result["prediction"] == 1 else "You don't have Heart Disease"
                    predictions.append(prediction)
                    probabilities.append(result["probability"])
                else:
                    predictions.append("Error")
                    probabilities.append(0.0)

            # Add predictions and probabilities to the data frame
            df["Prediction"] = predictions
            df["Probability"] = probabilities
            st.write(df)  # Display the updated data frame


def past_predictions_page():
    st.header("Past Predictions")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

    prediction_source = st.selectbox("Prediction Source", ["webapp", "scheduled predictions", "all"])

    if st.button("Retrieve Predictions"):
        # Query the database and retrieve past predictions
        params = {"start_date": str(start_date), "end_date": str(end_date), "prediction_source": prediction_source}
        response = requests.get(f"{API_URL}/past-predictions", params=params)
        if response.status_code == 200:
            result = response.json()
            past_predictions = result["past_predictions"]
            if past_predictions:
                df = pd.DataFrame(past_predictions)
                st.write(df)
            else:
                st.warning("No predictions found for the selected criteria.")
        else:
            st.error("Failed to retrieve predictions.")


if __name__ == "__main__":
    main()
