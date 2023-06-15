<<<<<<< HEAD
import streamlit as st
import requests
import pandas as pd


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
        response = requests.post("http://localhost:8000/predict", json=data)
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
                response = requests.post("http://localhost:8000/predict", json=data)
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
        response = requests.get("http://localhost:8000/past-predictions", params={"start_date": str(start_date), "end_date": str(end_date), "prediction_source": prediction_source})
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
=======
import requests
import streamlit as st
import pandas as pd
import datetime

# FastAPI endpoint URLs
PREDICT_URL = 'http://localhost:8000/predict'
PAST_PREDICTIONS_URL = 'http://localhost:8000/past-predictions'

# function for making predictions
def make_predictions(my_features):
    return 42

# Function to insert prediction data into the table
def insert_prediction_data(prediction_data):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.orm import declarative_base
    from sqlalchemy import Column, Integer, String, DateTime
    from sqlalchemy.sql import text

    # Define SQLAlchemy model for prediction table
    Base = declarative_base()
    class Prediction(Base):
        __tablename__ = 'predictions'
        id = Column(Integer, primary_key=True, autoincrement=True)
        prediction = Column(Integer)
        age = Column(Integer)
        sex = Column(String)
        chest_pain_type = Column(Integer)
        prediction_date = Column(DateTime)
        prediction_source = Column(String)

    # Create SQLAlchemy engine and session
    DATABASE_CONNECTION_STRING ='postgresql://postgres:test@localhost:5432/project'
    engine = create_engine(DATABASE_CONNECTION_STRING)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Insert prediction data into the table
    prediction = Prediction(**prediction_data)
    session.add(prediction)
    session.commit()

    # Close the session
    session.close()

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
        # Insert data into prediction table
        prediction_data = {
            'prediction': result,
            'age': age,
            'sex': sex,
            'chest_pain_type': chest_pain_type,
            'prediction_date': datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
            'prediction_source': 'Webapp'
        }
        insert_prediction_data(prediction_data)




    # Upload CSV file for multiple predictions
    st.subheader("Multiple Sample Prediction")
    file = st.file_uploader("Upload CSV file", type=["csv"])

    if file is not None:
        # Read CSV file and extract feature values
        df = pd.read_csv(file)
        # Make API request to model service with feature values
        data = df.to_dict('records')
        # Call make_predictions() function to get predictions for each record
        results = [make_predictions(d) for d in data]
        # Combine input features and predictions into a DataFrame
        output_df = pd.DataFrame(data)
        output_df['Prediction'] = results
        # Display prediction results
        st.dataframe(output_df)


# Past predictions display webpage
def past_predictions_page():
    from sqlalchemy import Column, Integer, String, DateTime
    from sqlalchemy.orm import declarative_base
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine
    import pandas as pd
    import streamlit as st
    
    st.header("Past Predictions")

    # Date selection components
    start_date = st.date_input("Start Date", value=None)
    end_date = st.date_input("End Date", value=None)

    # Prediction source dropdown list
    prediction_sources = ['webapp', 'scheduled predictions', 'all']
    selected_prediction_source = st.selectbox("Prediction Source", prediction_sources)

    # Retrieve predictions button
    if st.button("Retrieve Predictions"):
        # Define SQLAlchemy model for prediction table
        Base = declarative_base()
        class Prediction(Base):
            __tablename__ = 'predictions'
            id = Column(Integer, primary_key=True, autoincrement=True)
            prediction = Column(Integer)
            age = Column(Integer)
            sex = Column(String)
            chest_pain_type = Column(Integer)
            prediction_date = Column(DateTime)
            prediction_source = Column(String)

        # Create SQLAlchemy engine and session
        DATABASE_CONNECTION_STRING ='postgresql://postgres:test@localhost:5432/project'
        engine = create_engine(DATABASE_CONNECTION_STRING)
        Session = sessionmaker(bind=engine)
        session = Session()

        # Fetch past predictions based on selected dates and prediction source
        if selected_prediction_source == 'all':
            past_predictions = session.query(Prediction).filter(Prediction.prediction_date >= start_date,
                                                               Prediction.prediction_date <= end_date).all()
        else:
            past_predictions = session.query(Prediction).filter(Prediction.prediction_date >= start_date,
                                                               Prediction.prediction_date <= end_date,
                                                               Prediction.prediction_source == selected_prediction_source.capitalize()).all()

        # Display past predictions in a table
        if past_predictions:
            df = pd.DataFrame([(p.prediction, p.age, p.sex, p.chest_pain_type, p.prediction_date, p.prediction_source) for p in past_predictions],
                              columns=['Prediction', 'Age', 'Sex', 'Chest Pain Type', 'Prediction Date', 'Prediction Source'])
            st.dataframe(df)
        else:
            st.write("No past predictions found.")

        # Close the session
        session.close()


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
>>>>>>> origin/main
