import requests
import streamlit as st
import pandas as pd

# FastAPI endpoint URLs
PREDICT_URL = 'http://localhost:8000/predict'
PAST_PREDICTIONS_URL = 'http://localhost:8000/past-predictions'

# Placeholder function for making predictions
def make_predictions(my_features):
    return 42

# Prediction page
def prediction_page():
    st.header("Single Sample Prediction")

    # Input fields for features
    age = st.number_input('Age', min_value=0, max_value=150, value=30)
    sex = st.selectbox('Sex', options=['Male', 'Female'])
    chest_pain_type = st.selectbox('Chest Pain Type', options=[1, 2, 3, 4])

    # Predict button
    if st.button("Predict"):
        data = {
            'Age': age,
            'Sex': sex,
            'Chest Pain Type': chest_pain_type
    }
        # Call make_predictions() function to get fixed prediction value of 42
        result = make_predictions(data)
        # Display prediction result
        st.write("Prediction: ", result)
        st.write("Input Features: ", data)
    # Upload CSV file for multiple predictions
    st.subheader("Multiple Sample Prediction")
    file = st.file_uploader("Upload CSV file", type=["csv"])
    
    if file is not None:
    # Read CSV file and extract feature values
        df = pd.read_csv(file)
    # Make API request to model service with feature values
        data = df.to_dict('records')
    # Call make_predictions() function to get fixed prediction value of 42 for each prediction
        results = [make_predictions(d) for d in data]
    # Display prediction results
        for r in results:
            st.write("Prediction: ", r)
            st.write("Input Features: ", data)
# Past predictions display webpage
def past_predictions_page():
    st.header("Past Predictions Display Webpage")

    # Date selection component
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

    # Prediction source drop-down list
    prediction_source = st.selectbox("Prediction Source", ["webapp", "scheduled predictions", "all"])

    if st.button("Retrieve Predictions"):
        # Make API request to model service with date range and prediction source
        params = {
            'start_date': start_date,
            'end_date': end_date,
            'prediction_source': prediction_source
        }
        response = requests.get(PAST_PREDICTIONS_URL, params=params)
        if response.status_code == 200:
            # Get past predictions from model service
            past_predictions = response.json()
            # Display past predictions
            for prediction in past_predictions:
                st.write("Prediction date: ", prediction['prediction_date'])
                st.write("Used features: ", prediction['used_features'])
                st.write("Prediction result: ", prediction['prediction'])
        else:
            st.write("Error retrieving past predictions")

# Main Streamlit app
def main():
    st.title("Heart Disease Prediction")
    st.write('Fill in the features for a single sample prediction or upload a CSV file for multiple predictions.')

    # Navigation menu
    pages = ["Prediction", "Past Predictions"]
    choice = st.sidebar.selectbox("Select Page", pages)
    # Display selected page
    if choice == "Prediction":
        prediction_page()
    elif choice == "Past Predictions":
        past_predictions_page()

if __name__ == "__main__":
     main()