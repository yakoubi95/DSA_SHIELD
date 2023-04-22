from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Define the base model
Base = declarative_base()

# Define the prediction data model
class Prediction(Base):
    __tablename__ = 'predictions'
    id = Column(Integer, primary_key=True)
    prediction = Column(Integer)
    age = Column(Integer)
    sex = Column(String)
    chest_pain_type = Column(Integer)
    prediction_date = Column(DateTime, default=datetime.utcnow)
    prediction_source = Column(String)

# Create a database connection
DATABASE_URL = 'postgresql://postgres:test@localhost:5432/project'  
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the table in the database
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()


# Endpoint for making model predictions
@app.post('/predict')
def predict(request: Request, prediction_source: str = None):
    try:
        # Get feature values from request
        age = request.json()['Age']
        sex = request.json()['Sex']
        chest_pain_type = request.json()['Chest Pain Type']
        

        prediction = 42
        
        # Save prediction to database
        db = SessionLocal()
        new_prediction = Prediction(prediction=prediction, age=age, sex=sex, chest_pain_type=chest_pain_type, prediction_source=prediction_source)
        db.add(new_prediction)
        db.commit()
        db.refresh(new_prediction)
        db.close()
        
        return JSONResponse(content={'Prediction': prediction}, status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error making prediction: {}'.format(str(e)))

# Endpoint for getting past predictions
@app.get('/past-predictions')
def get_past_predictions(start_date: str, end_date: str, prediction_source: str):
    try:
        # Convert date strings to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        
        # Query past predictions from database
        db = SessionLocal()
        past_predictions = db.query(Prediction).filter(Prediction.prediction_date.between(start_date, end_date), Prediction.prediction_source == prediction_source).all()
        db.close()
        
        # Convert past predictions to dictionary
        past_predictions_dict = []
        for prediction in past_predictions:
            past_prediction_dict = {
                'Prediction': prediction.prediction,
                'Age': prediction.age,
                'Sex': prediction.sex,
                'Chest Pain Type': prediction.chest_pain_type,
                'Prediction Date': prediction.prediction_date
            }
            past_predictions_dict.append(past_prediction_dict)
        
        return JSONResponse(content={'Past Predictions': past_predictions_dict}, status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error getting past predictions: {}'.format(str(e)))
