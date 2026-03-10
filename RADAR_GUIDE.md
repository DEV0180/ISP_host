# Radar Integration Guide

Complete guide to integrate mmWave radar data collection with the Sleep Quality Analysis API.

## Overview

The system consists of three components:

1. **mmWave Radar** - Hardware that collects vital signs (heart rate)
2. **Radar Collector** - Software that captures radar data
3. **Sleep API** - FastAPI that processes data and predicts sleep quality

```
Radar Hardware
      ↓
radar_collector.py (collects raw data)
      ↓
CSV File (radar_data_YYYYMMDD_HHMMSS.csv)
      ↓
API /radar/predict endpoint
      ↓
Sleep Predictions + Quality Score
```

---

## Prerequisites

### Hardware
- IWR6843AOP mmWave Sensor (or compatible)
- USB connection to COM port
- Proper serial drivers installed

### Software
```bash
pip install pyserial mmWave scipy requests
```

Or install from hosting directory:
```bash
pip install -r requirements.txt
```

---

## Setup & Usage

### 1. Start the API Server

```bash
cd hosting
python main.py
```

You should see:
```
[INFO] Processing...
✓ Model loaded successfully. Classes: 7
INFO: Uvicorn running on http://0.0.0.0:8000
```

### 2. Collect Radar Data

In a new terminal:

```bash
# Basic usage (default: 20 seconds on COM14)
python radar_collector.py

# Custom COM port and duration
python radar_collector.py --port COM3 --duration 30

# Collect only (don't send to API)
python radar_collector.py --collect-only

# Custom API URL
python radar_collector.py --api-url http://192.168.1.100:8000
```

**Options:**
```
--port PORT              COM port name (default: COM14)
--duration SECONDS       Recording duration (default: 20)
--output PATH           Output CSV file path
--api-url URL           API URL (default: http://localhost:8000)
--collect-only          Save data without sending to API
```

### 3. What Happens

1. **Connects to radar** on specified COM port
2. **Records data** for specified duration
3. **Saves CSV** with columns: `time_sec`, `unwrapPhasePeak_mm`
4. **Converts to HR** using phase-to-heart-rate algorithm
5. **Sends to API** for sleep stage prediction
6. **Returns results** with sleep quality score

---

## API Endpoints for Radar

### 1. Process Radar Data → Heart Rate

```
POST /radar/process
```

**Request:**
```json
{
  "time_sec": [0.0, 0.1, 0.2, 0.3, ...],
  "unwrapPhasePeak_mm": [10.5, 11.2, 10.8, 11.5, ...]
}
```

**Response:**
```json
{
  "status": "success",
  "samples": 100,
  "hr_values": [68.2, 69.1, 68.9, ...],
  "hr_stats": {
    "mean": 68.5,
    "min": 65.2,
    "max": 72.1,
    "std": 2.3
  }
}
```

### 2. Full Pipeline: Radar → Sleep Prediction

```
POST /radar/predict
```

**Request:**
```json
{
  "time_sec": [0.0, 0.1, 0.2, ...],
  "unwrapPhasePeak_mm": [10.5, 11.2, 10.8, ...]
}
```

**Response:**
```json
{
  "total_windows": 10,
  "total_duration": {
    "seconds": 3200,
    "hours": 0.89
  },
  "predictions": [ ... ],
  "sleep_scores": {
    "duration_score": 88.5,
    "efficiency_score": 92.3,
    "deep_sleep_score": 85.2,
    "rem_sleep_score": 78.5,
    "hrv_score": 82.1
  },
  "sleep_quality": {
    "final_score": 85.3,
    "quality_level": "Excellent"
  },
  "radar_conversion": {
    "input_samples": 100,
    "output_samples": 100,
    "hr_stats": {
      "mean": 68.5,
      "min": 65.2,
      "max": 72.1,
      "std": 2.3
    }
  }
}
```

---

## Using Pre-Recorded Data

If you already have radar CSV files:

```bash
# Send to API using dedicated script
python send_radar_data.py path/to/radar_data.csv

# With custom API URL
python send_radar_data.py path/to/radar_data.csv --api-url http://192.168.1.100:8000
```

This will:
1. Read the CSV file
2. Parse time and phase data
3. Send to API
4. Save results to `radar_data_results.json`

---

## CSV File Format

The radar collector produces CSV files with this format:

```csv
time_sec,unwrapPhasePeak_mm
0.0,10.523
0.1,11.234
0.2,10.892
0.3,11.456
...
```

**Columns:**
- `time_sec` - Elapsed time in seconds
- `unwrapPhasePeak_mm` - Unwrapped phase in millimeters

You can also manually create this format from your own radar data.

---

## Phase-to-HR Conversion

The `convert_radar_to_hr()` function:

1. **Normalizes phase data** to 0-1 range
2. **Maps to HR range** of 40-120 bpm (typical for sleep)
3. **Applies smoothing** to reduce noise
4. **Returns HR array** in bpm format

**Conversion Formula:**
```
HR = 40 + (phase_normalized * 80)
HR_smoothed = moving_average(HR, window=5)
```

### Calibration

For better accuracy, you can modify the HR range in `main.py`:

```python
def convert_radar_to_hr(phase_data: np.ndarray) -> np.ndarray:
    phase_normalized = (phase_data - min) / (max - min)
    # Change these values for your calibration
    hr_converted = 40 + (phase_normalized * 80)  # 40-120 bpm range
    return hr_smoothed
```

---

## Example Workflows

### Workflow 1: Real-Time Collection + Prediction

```bash
# Terminal 1: Start API
python main.py

# Terminal 2: Collect and automatically send
python radar_collector.py --port COM14 --duration 30
```

Output:
```
[INFO] Recording for 30 seconds...
[INFO] Output: radar_data_20260310_120000.csv
  [collected 300 samples...]
[SUCCESS] Data saved to: radar_data_20260310_120000.csv

[INFO] Sending data to API...
[SUCCESS] Sleep analysis complete!
Final Sleep Score: 85.3%
Quality Level: Excellent
```

### Workflow 2: Batch Processing

```bash
# Collect without sending
python radar_collector.py --collect-only --duration 20

# Later, process the file
python send_radar_data.py radar_data_20260310_120000.csv

# Results saved to radar_data_results.json
```

### Workflow 3: API Direct Request

```bash
curl -X POST http://localhost:8000/radar/predict \
  -H "Content-Type: application/json" \
  -d @request.json
```

Where `request.json` contains:
```json
{
  "time_sec": [0.0, 0.1, 0.2, ...],
  "unwrapPhasePeak_mm": [10.5, 11.2, 10.8, ...]
}
```

---

## Troubleshooting

### "Failed to open COM14"

**Problem:** Cannot connect to radar
**Solution:**
```bash
# Check available ports
python -m serial.tools.list_ports

# Update port in radar_collector.py or use --port flag
python radar_collector.py --port COM3
```

### "mmWave module not found"

**Problem:** mmWave library not installed
**Solution:**
```bash
pip install mmWave pyserial

# Or from requirements.txt
pip install -r requirements.txt
```

### "Cannot connect to API"

**Problem:** API server not running
**Solution:**
```bash
# Start server
python main.py

# Check http://localhost:8000/health
curl http://localhost:8000/health
```

### "Model not available"

**Problem:** sleep_model.h5 not found
**Solution:**
```bash
# Copy model from parent directory
cp ../sleep_model.h5 .

# Or evaluate without model (returns error for /predict endpoints)
```

### No data collected / No samples

**Problem:** Radar returns no valid samples
**Solution:**
1. Verify radar is powered on
2. Check USB/serial connection
3. Verify correct COM port
4. Check radar configuration
5. Try longer duration (--duration 30)

---

## Performance Tips

1. **Use 60+ seconds** of data for better accuracy
2. **Stable placement** - Keep radar steady
3. **Consistent position** - Same placement each session
4. **Quiet environment** - Reduces noise
5. **Multiple attempts** - Average results for better calibration

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────┐
│          mmWave Radar Hardware              │
│     (Captures vital signs continuously)     │
└──────────────────┬──────────────────────────┘
                   │ USB/Serial
                   ▼
┌─────────────────────────────────────────────┐
│       radar_collector.py                     │
│  • Opens COM port                            │
│  • Reads phase data                          │
│  • Saves to CSV                              │
└──────────────────┬──────────────────────────┘
                   │ CSV file
                   ▼
┌─────────────────────────────────────────────┐
│      Sleep Quality Analysis API              │
│  • POST /radar/predict                       │
│  • Convert phase → HR                        │
│  • Predict sleep stages                      │
│  • Calculate sleep quality                   │
└──────────────────┬──────────────────────────┘
                   │ JSON response
                   ▼
┌─────────────────────────────────────────────┐
│          Sleep Predictions                   │
│  • Stage classification per window           │
│  • Sleep quality metrics                     │
│  • Overall sleep score (0-100%)              │
└─────────────────────────────────────────────┘
```

---

## Next Steps

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Start API: `python main.py`
3. ✅ Collect data: `python radar_collector.py`
4. ✅ View results in terminal output
5. ✅ Process historical data: `python send_radar_data.py file.csv`

---

## Related Documentation

- [README.md](README.md) - Main API documentation
- [QUICKSTART.md](QUICKSTART.md) - 5-minute setup guide
- [DEPLOYMENT.md](DEPLOYMENT.md) - Cloud deployment

---

**Last Updated**: March 2026  
**Version**: 1.0.0
