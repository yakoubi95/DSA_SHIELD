import joblib
import numpy as np
import psycopg2
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# FastAPI instance
app = FastAPI()

# Load the ML model
model = joblib.load(open("models/model.pkl", "rb"))

# Create a connection to the PostgreSQL database
conn = psycopg2.connect(
    dbname='project',
    user='postgres',
    password='test',
    host='localhost',
    port='5432'
)

class PredictionRequest(BaseModel):
    age: int
    restingBP: int
    oldpeak: float
    sex: str
    chestpaintype: str
    fastingBS: str
    exerciseAngina: str
    st_slope: str

@app.post("/predict")
def predict(data: PredictionRequest):
    # Convert input features to the desired format
    sex = 1 if data.sex == "M" else 0
    fastingBS = 1 if data.fastingBS == "Yes" else 0
    exerciseAngina = 1 if data.exerciseAngina == "Yes" else 0

    chestpaintype_map = {"ASY": 496, "NAP": 203, "ATA": 173}
    chestpaintype = chestpaintype_map.get(data.chestpaintype, 46)

    st_slope_map = {"Flat": 460, "Up": 395}
    st_slope = st_slope_map.get(data.st_slope, 63)

    input_list = [
        data.age,
        sex,
        chestpaintype,
        data.restingBP,
        fastingBS,
        exerciseAngina,
        data.oldpeak,
        st_slope,
    ]

    # Convert the input list to a numpy array
    final_features = np.array(input_list, dtype=float).reshape(1, -1)

    # Make prediction using the ML model
    prediction = int(model.predict(final_features)[0])
    probability = np.max(model.predict_proba(final_features)) * 100

    # Save the prediction, features, date, and source in the database
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO predictions (prediction, age, restingBP, oldpeak, sex, chestpaintype, fastingBS, exerciseAngina, st_slope, prediction_source) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (prediction, data.age, data.restingBP, data.oldpeak, data.sex, data.chestpaintype, data.fastingBS, data.exerciseAngina, data.st_slope, "Webapp"),
        )
        conn.commit()

    return {"prediction": prediction, "probability": probability}

@app.get("/past-predictions")

def get_past_predictions(start_date: str, end_date: str, prediction_source: str):
    # Create a database cursor
    cursor = conn.cursor()

    # Query the database to retrieve past predictions based on the selected date range and source
    cursor.execute(
        "SELECT prediction, age, restingBP, oldpeak, sex, chestpaintype, fastingBS, exerciseAngina, st_slope, prediction_date "
        "FROM predictions "
        "WHERE prediction_date::date >= %s::date AND prediction_date::date <= %s::date AND prediction_source = %s",
        (start_date, end_date, prediction_source),
    )

    rows = cursor.fetchall()

    # Prepare the response data
    past_predictions = []
    for row in rows:
        prediction, age, restingBP, oldpeak, sex, chestpaintype, fastingBS, exerciseAngina, st_slope, prediction_date = row
        prediction_data = {
            "prediction": prediction,
            "age": age,
            "restingBP": restingBP,
            "oldpeak": oldpeak,
            "sex": sex,
            "chestpaintype": chestpaintype,
            "fastingBS": fastingBS,
            "exerciseAngina": exerciseAngina,
            "st_slope": st_slope,
            "prediction_date": prediction_date.strftime("%Y-%m-%d %H:%M:%S"),  # Convert date to string format
            "prediction_source": prediction_source,
        }
        past_predictions.append(prediction_data)

    # Close the database cursor
    cursor.close()

    return {"past_predictions": past_predictions}
