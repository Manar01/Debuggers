import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Load Model
try:
    model = joblib.load("knn_model.joblib")
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")

# Define input data model
class InputData(BaseModel):
    Year: int
    Engine_Size: float
    Mileage: int
    Type: str
    Make: str
    Options: str

# Preprocessing function
def preprocessing(input_features: InputData):
    dict_f = {
        'Year': input_features.Year,
        'Engine_Size': input_features.Engine_Size,
        'Mileage': input_features.Mileage,
        'Type_Accent': input_features.Type == 'Accent',
        'Type_Land Cruiser': input_features.Type == 'LandCruiser',
        'Make_Hyundai': input_features.Make == 'Hyundai',
        'Make_Mercedes': input_features.Make == 'Mercedes',
        'Options_Full': input_features.Options == 'Full',
        'Options_Standard': input_features.Options == 'Standard'
    }

    # Convert to list in correct order
    features_list = [dict_f[key] for key in sorted(dict_f)]

    # Ensure scaler is working correctly
    try:
        scaled_features = scaler.transform([features_list])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in preprocessing: {e}")

    return scaled_features

# Prediction endpoint
@app.post("/predict")
def predict(data: InputData):
    try:
        features = [[data.Year, data.Engine_Size, data.Mileage]]  # Adjust this based on your model
        prediction = model.predict(features)
        print(f"🔍 Received input: {features}, Prediction: {prediction}")  # Debugging print
        return {"prediction": int(prediction[0])}
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return {"error": str(e)}
