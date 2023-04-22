import psycopg2 as psycopg2
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from datetime import date, datetime
from typing import List

# Create a connection to the PostgreSQL database
conn = psycopg2.connect(
    dbname='project',
    user='postgres',
    password='test',
    host='localhost',
    port='5432'
)
cursor = conn.cursor()

# Create a FastAPI instance
app = FastAPI()

# Create a Pydantic model to represent the input data for the prediction
class predictionsData(BaseModel):
    age: int
    sex: int
    chest_pain_type: int

# Define a function to insert a new prediction record into the database
def insert_prediction(prediction_date, used_features, prediction_result, prediction_source):
    sql = """
        INSERT INTO predictions (prediction_date, used_features, prediction_result, prediction_source)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(sql, (prediction_date, used_features, prediction_result, prediction_source))
    conn.commit()

# Placeholder function for making predictions
def make_predictions(my_features: predictionsData):
    return 42

# Define a FastAPI endpoint to handle the prediction request
@app.post("/predict")
async def predict(data: predictionsData):
    # Make prediction using input data
    # Store prediction result and used features in the database
    try:
        # Make prediction using input data
        # In this example, the prediction result is just the sum of all input features
        prediction_result = make_predictions(data)

        # Store prediction result and used features in the database
        prediction_date = datetime.now()
        used_features = str(data.dict())
        prediction_source = 'webapp'
        insert_prediction(prediction_date, used_features, prediction_result, prediction_source)
        return {"Features": used_features, "prediction": prediction_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Define a function to retrieve past predictions from the database
def get_past_predictions(start_date, end_date, prediction_source):
    sql = """
        SELECT prediction_date, used_features, prediction_result
        FROM predictions
        WHERE prediction_date BETWEEN %s AND %s
        AND (%s = 'all' OR prediction_source = %s)
    """
    cursor.execute(sql, (start_date, end_date, prediction_source))
    rows = cursor.fetchall()
    past_predictions = [
        {
            "prediction_date": row[0].strftime("%Y-%m-%d %H:%M:%S"),
            "used_features": row[1],
            "prediction": row[2]
        } for row in rows
    ]
    return past_predictions

# Define a FastAPI endpoint to retrieve past predictions from the database
@app.get("/past-predictions")
async def past_predictions(start_date: date, end_date: date, prediction_source: str = 'all'):
# Retrieve past predictions from the database and return them as a JSON response
    try:
        past_predictions = get_past_predictions(start_date, end_date, prediction_source)
        return past_predictions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))