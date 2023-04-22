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
            'prediction_date': datetime.datetime.now().strftime('%Y/%m/%d'),
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
        # Call make_predictions() function to get fixed prediction value of 42 for each prediction
        results = [make_predictions(d) for d in data]
        # Display prediction results
        for idx, r in enumerate(results):
            st.write(f"Prediction {idx+1}: {r}")
            st.write(f"Input Features {idx+1}: ")
            st.write("Sex: ", data[idx]['Sex'])
            st.write("Age: ", data[idx]['Age'])
            st.write("Chest pain type: ", data[idx]['Chest pain type'])




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
