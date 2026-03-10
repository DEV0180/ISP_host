# 🚀 Quick Reference - Sleep Quality API

One-page cheat sheet for everything you need to know.

---

## ⚡ Get Running in 30 Seconds

```bash
# 1. Copy model file
cd hosting
copy ..\sleep_model.h5 .

# 2. Install packages (if needed)
pip install -r requirements.txt

# 3. Start server
python main.py

# 4. Open in browser
# http://localhost:8000/docs
```

**Done!** ✅ API is running

---

## 📊 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Check if running + model loaded |
| `/docs` | GET | Interactive API documentation |
| `/predict/csv` | POST | Upload CSV with HR data |
| `/predict/array` | POST | Send HR as JSON array |
| `/radar/process` | POST | Convert radar phase → HR |
| `/radar/predict` | POST | Radar → HR → sleep prediction |

---

## 📡 Collect Radar Data

```bash
# Basic (20 sec on COM14)
python radar_collector.py

# Custom settings
python radar_collector.py --port COM3 --duration 60

# Collect only (don't send to API)
python radar_collector.py --collect-only
```

**Output:** `radar_data_YYYYMMDD_HHMMSS.csv`

---

## 📤 Send Data to API

### Method 1: JSON Array
```bash
curl -X POST http://localhost:8000/predict/array \
  -H "Content-Type: application/json" \
  -d '{"hr_values": [60,61,62,63,64,65]}'
```

### Method 2: CSV File
```bash
curl -X POST http://localhost:8000/predict/csv \
  -F "file=@data.csv"
```

### Method 3: Python
```python
import requests

response = requests.post(
    'http://localhost:8000/predict/array',
    json={'hr_values': [60, 61, 62, 63, 64, 65]}
)
result = response.json()
print(f"Score: {result['sleep_quality']['final_score']}")
```

### Method 4: Radar Data
```bash
curl -X POST http://localhost:8000/radar/predict \
  -H "Content-Type: application/json" \
  -d '{
    "time_sec": [0.0, 0.1, 0.2],
    "unwrapPhasePeak_mm": [10.5, 11.2, 10.8]
  }'
```

---

## 🔧 Configuration

### Edit `.env` file:
```ini
MODEL_PATH=sleep_model.h5
API_HOST=0.0.0.0
API_PORT=8000
WINDOW_SIZE=640
DEBUG=False
```

### Edit `config.py` for:
- Model parameters
- Score weights
- Reference values

---

## 📝 Response Format

```json
{
  "total_windows": 10,
  "total_duration": {
    "seconds": 3200,
    "hours": 0.89
  },
  "predictions": [
    {
      "window": 1,
      "stage": "N2",
      "confidence": 95.23,
      "probabilities": {
        "Wake": 0.5,
        "N1": 2.3,
        "N2": 95.23,
        "N3": 1.2,
        "REM": 0.7,
        "Movement": 0.1,
        "Unscored": 0.0
      }
    }
  ],
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
  }
}
```

---

## 🏥 Sleep Quality Levels

| Score | Level | Meaning |
|-------|-------|---------|
| 80-100 | Excellent | Great sleep quality |
| 65-79 | Good | Acceptable sleep |
| 50-64 | Fair | Below average |
| 35-49 | Poor | Significant issues |
| <35 | Very Poor | Urgent attention needed |

---

## 🐛 Troubleshoot

### "Model not found"
```bash
copy ..\sleep_model.h5 .
# Then restart: python main.py
```

### "Cannot connect"
```bash
# Check if running
curl http://localhost:8000/health

# If not running, start it
python main.py
```

### "Port already in use"
```bash
# Use different port in .env
API_PORT=8001

# Or kill process using port 8000
netstat -ano | findstr :8000  # Windows
lsof -i :8000                  # macOS/Linux
```

### "Module not found"
```bash
pip install -r requirements.txt --upgrade
```

---

## 🐳 Docker

```bash
# Build image
docker build -t sleep-api .

# Start container
docker run -p 8000:8000 sleep-api

# Or use Compose
docker-compose up
```

Access at: `http://localhost:8000/docs`

---

## 📂 File Structure

```
hosting/
├── main.py                 # FastAPI app
├── config.py              # Settings
├── radar_collector.py     # Radar data collection
├── send_radar_data.py     # Process saved data
├── test_api.py           # API tests
├── requirements.txt       # Dependencies
├── Dockerfile            # Container
├── .env.example          # Config template
└── README.md             # Full docs
```

---

## 📚 Documentation

- **[FIX_MODEL_ERROR.md](FIX_MODEL_ERROR.md)** ← **START HERE IF MODEL ERROR**
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup
- **[README.md](README.md)** - Complete documentation
- **[RADAR_GUIDE.md](RADAR_GUIDE.md)** - Radar integration
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deploy to cloud

---

## 🎯 Common Tasks

### Test API
```bash
python test_api.py
```

### Check Health
```bash
curl http://localhost:8000/health
```

### View Docs
```
http://localhost:8000/docs
```

### Collect 30 Sec of Radar
```bash
python radar_collector.py --duration 30
```

### Process Saved CSV
```bash
python send_radar_data.py radar_data_20260310_120000.csv
```

---

## 🌐 Deploy

### Heroku
```bash
heroku login
heroku create your-app-name
git push heroku main
```

### Docker Hub
```bash
docker build -t username/sleep-api .
docker push username/sleep-api
```

### Google Cloud Run
```bash
gcloud run deploy sleep-api \
  --source . \
  --platform managed \
  --region us-central1
```

---

## 🔑 Key Parameters

| Parameter | Value | Meaning |
|-----------|-------|---------|
| WINDOW_SIZE | 640 | 20Hz × 32sec |
| Duration Score Weight | 0.35 | 35% of final score |
| Deep Sleep % Ideal | 0.20 | 20% of sleep |
| REM Sleep % Ideal | 0.25 | 25% of sleep |
| HRV Reference | 65 bpm | Normal HRV value |

---

## 🚨 Error Codes

| Status | Meaning | Fix |
|--------|---------|-----|
| 200 | Success | - |
| 400 | Bad request | Check JSON format |
| 503 | Model unavailable | Copy sleep_model.h5 |
| 500 | Server error | Check logs |

---

## 💾 Data Format

### CSV for predictions:
```csv
HR
60
61
62
```

### JSON for predictions:
```json
{"hr_values": [60, 61, 62, 63, 64, 65]}
```

### Radar data:
```json
{
  "time_sec": [0.0, 0.1, 0.2],
  "unwrapPhasePeak_mm": [10.5, 11.2, 10.8]
}
```

---

## 🎓 Quick Tips

1. **Minimum data:** 640 samples (32 seconds at 20Hz)
2. **Better accuracy:** Use 5+ minutes of data
3. **Radar calibration:** May need tuning for your setup
4. **Storage:** Model is ~100-500MB
5. **Performance:** Uses CPU/GPU per model size

---

## 👥 Get Help

1. Read [FIX_MODEL_ERROR.md](FIX_MODEL_ERROR.md) if model issues
2. Check [RADAR_GUIDE.md](RADAR_GUIDE.md) for radar problems
3. See [DEPLOYMENT.md](DEPLOYMENT.md) for cloud issues
4. Review [README.md](README.md) for full documentation

---

## ✅ Checklist: Getting Started

- [ ] Copy sleep_model.h5 to hosting directory
- [ ] Run: `pip install -r requirements.txt`
- [ ] Run: `python main.py`
- [ ] Visit: http://localhost:8000/docs
- [ ] Test with: `python test_api.py`
- [ ] Try collecting radar: `python radar_collector.py`

---

**Everything you need on one page! 📄**

For details, see full docs in the repository.

---

**Last Updated**: March 2026  
**Version**: 1.0.0
