from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
import io
import os
from config import MODEL_PATH, WINDOW_SIZE


# Request models
class HRDataRequest(BaseModel):
    """Heart rate data for prediction"""
    hr_values: List[float]

app = FastAPI(
    title="Sleep Quality Analysis API",
    description="Analyzes heart rate data to predict sleep stages and calculate sleep quality score",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model globally
model = None
num_classes = 0

try:
    if os.path.exists(MODEL_PATH):
        model = load_model(MODEL_PATH)
        num_classes = model.output_shape[-1]
        print(f"✓ Model loaded successfully: {MODEL_PATH}")
    else:
        print(f"⚠ Model file not found: {MODEL_PATH}")
        print("  Copy your model: cp ../sleep_model.h5 .")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    model = None
    num_classes = 0


def calculate_hrv_rmssd(hr_data):
    """Calculate Heart Rate Variability using RMSSD method"""
    successive_diffs = np.diff(hr_data)
    squared_diffs = successive_diffs ** 2
    mean_squared = np.mean(squared_diffs)
    rmssd = np.sqrt(mean_squared)
    return round(rmssd, 2)


def process_sleep_data(hr_data):
    """
    Process heart rate data and predict sleep stages
    Returns predictions and sleep quality score
    """
    if model is None:
        raise HTTPException(
            status_code=503, 
            detail="Model not loaded. Ensure sleep_model.h5 exists in hosting directory. Copy: cp ../sleep_model.h5 ."
        )
    
    # Fix missing values
    hr_series = pd.Series(hr_data)
    hr_data_filled = hr_series.ffill().bfill().values
    
    # Normalize
    hr_mean = hr_data_filled.mean()
    hr_std = hr_data_filled.std()
    if hr_std == 0:
        hr_normalized = hr_data_filled - hr_mean
    else:
        hr_normalized = (hr_data_filled - hr_mean) / hr_std
    
    # Create windows of size 640 (20 Hz * 32 sec)
    num_windows = len(hr_normalized) // WINDOW_SIZE
    
    if num_windows == 0:
        raise HTTPException(
            status_code=400, 
            detail=f"Not enough data. Minimum {WINDOW_SIZE} samples required, got {len(hr_normalized)}"
        )
    
    windows = [hr_normalized[i*WINDOW_SIZE:(i+1)*WINDOW_SIZE] for i in range(num_windows)]
    
    # Predict
    X_test = np.array(windows).reshape(num_windows, WINDOW_SIZE, 1)
    predictions = model.predict(X_test, verbose=0)
    predicted_classes = np.argmax(predictions, axis=1)
    
    # Mapping sleep stages
    stage_map = ['Wake', 'N1', 'N2', 'N3', 'REM', 'Movement', 'Unscored'][:num_classes]
    
    # Create prediction list with confidence scores
    prediction_list = []
    for i in range(num_windows):
        stage = stage_map[predicted_classes[i]]
        conf = float(np.max(predictions[i]) * 100)
        prediction_list.append({
            "window": i + 1,
            "stage": stage,
            "confidence": round(conf, 2),
            "probabilities": {stage_map[j]: round(float(predictions[i][j]) * 100, 2) 
                            for j in range(num_classes)}
        })
    
    # --- Sleep Score Calculation ---
    # Each window = 640 samples @ 20 Hz = 32 seconds
    total_seconds = num_windows * 32
    total_hours = total_seconds / 3600
    
    # Duration Score: assume 8 hours ideal
    s1 = (total_hours / 8) * 100
    
    # Efficiency Score: non-wake stages (class != 0)
    non_wake_count = np.sum(predicted_classes != 0)
    s2 = (non_wake_count / num_windows) * 100
    
    # Deep Sleep Score: classes 1,2,3
    deep_sleep_count = np.sum((predicted_classes == 1) | (predicted_classes == 2) | (predicted_classes == 3))
    deep_sleep_score = deep_sleep_count / num_windows
    s3 = (deep_sleep_score / 0.2) * 100
    
    # REM Sleep Score: class 4
    rem_sleep_count = np.sum(predicted_classes == 4)
    rem_sleep_score = rem_sleep_count / num_windows
    s4 = (rem_sleep_score / 0.25) * 100
    
    # HRV Score
    hrv_score = calculate_hrv_rmssd(hr_data_filled)
    s5 = (hrv_score / 65) * 100
    
    # Final Score
    final_score = (0.35*s1) + (0.2*s2) + (0.15*s3) + (0.15*s4) + (0.15*s5)
    
    return {
        "total_windows": num_windows,
        "total_duration": {
            "seconds": total_seconds,
            "hours": round(total_hours, 2)
        },
        "predictions": prediction_list,
        "sleep_scores": {
            "duration_score": round(s1, 2),
            "efficiency_score": round(s2, 2),
            "deep_sleep_score": round(s3, 2),
            "rem_sleep_score": round(s4, 2),
            "hrv_score": round(s5, 2)
        },
        "sleep_quality": {
            "final_score": round(final_score, 2),
            "quality_level": get_quality_level(final_score)
        }
    }


def get_quality_level(score):
    """Map score to quality level"""
    if score >= 80:
        return "Excellent"
    elif score >= 65:
        return "Good"
    elif score >= 50:
        return "Fair"
    elif score >= 35:
        return "Poor"
    else:
        return "Very Poor"


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "message": "Sleep Quality Analysis API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict_csv": "/predict/csv",
            "predict_array": "/predict/array"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy" if model is not None else "unhealthy",
        "model_loaded": model is not None,
        "num_classes": num_classes
    }


@app.post("/predict/csv")
async def predict_from_csv(file: UploadFile = File(...)):
    """
    Upload CSV file with HR column and get sleep predictions
    Expected CSV format: rows with 'HR' column containing heart rate values
    """
    try:
        # Read CSV file
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        if 'HR' not in df.columns:
            raise HTTPException(status_code=400, detail="CSV must contain 'HR' column")
        
        hr_data = df['HR'].values
        
        if len(hr_data) == 0:
            raise HTTPException(status_code=400, detail="No HR data found in CSV")
        
        result = process_sleep_data(hr_data)
        return result
        
    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Invalid CSV format")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/predict/array")
async def predict_from_array(data: HRDataRequest):
    """
    Submit heart rate data as JSON array
    Expected JSON: {"hr_values": [60, 61, 62, ...]}
    """
    try:
        hr_values = data.hr_values
        
        if not hr_values or len(hr_values) == 0:
            raise HTTPException(status_code=400, detail="hr_values must be a non-empty list")
        
        hr_data = np.array(hr_values, dtype=float)
        result = process_sleep_data(hr_data)
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid data format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/predict/example")
async def example_request():
    """Get example request format"""
    return {
        "csv_endpoint": {
            "path": "/predict/csv",
            "method": "POST",
            "description": "Upload CSV file with 'HR' column",
            "example_csv": "HR\n60\n61\n62\n..."
        },
        "array_endpoint": {
            "path": "/predict/array",
            "method": "POST",
            "description": "Send HR data as JSON array",
            "example_json": {
                "hr_values": [60, 61, 62, 63, 64, 65]
            }
        }
    }


if __name__ == "__main__":
    import uvicorn
    import os
    
    # Safely get Railway's dynamic port, or default to 8000 if running locally
    port = int(os.environ.get("PORT", 8000))
    
    # Run the app using that port
    uvicorn.run(app, host="0.0.0.0", port=port)
