# Quick Start Guide

Get the Sleep Quality Analysis API running in 5 minutes!

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git (optional, for cloning)

## 1️⃣ Setup (2 minutes)

### Download and navigate
```bash
# If cloning from GitHub
git clone <your-repo-url>
cd hosting

# Or navigate to existing folder
cd path/to/hosting
```

### Create virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

## 2️⃣ Configure (1 minute)

### Setup environment
```bash
# Copy template
cp .env.example .env

# Edit if needed (usually defaults are fine)
# nano .env  (or use your editor)
```

### Add model file
```bash
# Copy the trained model
cp ../sleep_model.h5 .

# Or if using separate storage
# Download from your storage location
```

## 3️⃣ Run (1 minute)

```bash
python main.py
```

You'll see:
```
Uvicorn running on http://127.0.0.1:8000
Press CTRL+C to quit
```

## 4️⃣ Test (1 minute)

### Option A: Interactive API Docs
```
Open browser → http://localhost:8000/docs
```

Click "Try it out" on any endpoint!

### Option B: Test Script
```bash
pip install requests
python test_api.py
```

### Option C: Test with cURL
```bash
curl http://localhost:8000/health
```

## 5️⃣ Use the API

### Send heart rate data

**Method 1: JSON Array**
```bash
curl -X POST http://localhost:8000/predict/array \
  -H "Content-Type: application/json" \
  -d '{"hr_values": [60, 61, 62, 63, 64, 65]}'
```

**Method 2: CSV File**
Create `data.csv`:
```
HR
60
61
62
63
64
65
```

Then send:
```bash
curl -X POST http://localhost:8000/predict/csv \
  -F "file=@data.csv"
```

**Method 3: Python**
```python
import requests

response = requests.post(
    'http://localhost:8000/predict/array',
    json={'hr_values': [60, 61, 62, 63, 64, 65]}
)
result = response.json()
print(f"Sleep Score: {result['sleep_quality']['final_score']}")
```

## Response Example

```json
{
  "total_windows": 10,
  "total_duration": {
    "seconds": 3200,
    "hours": 0.89
  },
  "sleep_quality": {
    "final_score": 85.3,
    "quality_level": "Excellent"
  },
  "sleep_scores": {
    "duration_score": 88.5,
    "efficiency_score": 92.3,
    "deep_sleep_score": 85.2,
    "rem_sleep_score": 78.5,
    "hrv_score": 82.1
  }
}
```

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | API info |
| `/health` | GET | Health check |
| `/docs` | GET | Interactive API docs |
| `/predict/array` | POST | Predict from JSON array |
| `/predict/csv` | POST | Predict from CSV file |
| `/predict/example` | GET | Example request formats |

## Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt --upgrade
```

### "Model not found" error
```bash
# Copy model from parent directory
cp ../sleep_model.h5 .
```

### Port 8000 already in use
```bash
# Change port
python main.py --port 8001
```

### API not responding
```bash
# Check if server is running
# Stop with Ctrl+C and restart
python main.py
```

## Next Steps

1. **Explore the API**: Visit http://localhost:8000/docs
2. **Read full docs**: See [README.md](README.md)
3. **Deploy online**: See [DEPLOYMENT.md](DEPLOYMENT.md)
4. **Configure**: Edit [config.py](config.py)

## Deploy to Cloud

### Heroku (Free tier available)
```bash
# One command deployment
heroku create
git push heroku main
```

### Docker
```bash
docker build -t sleep-api .
docker run -p 8000:8000 sleep-api
```

## Get Help

- 📖 Full docs: [README.md](README.md)
- 🚀 Deployment: [DEPLOYMENT.md](DEPLOYMENT.md)
- 🏗️ Structure: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- 🐛 Issues: [GitHub Issues](../../issues)

---

**You're all set! 🎉**

For detailed information, see the full [README.md](README.md)
