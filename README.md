# Sleep Quality Analysis API

A FastAPI-based REST API for analyzing heart rate data to predict sleep stages and calculate comprehensive sleep quality scores.

## ⚡ Quick Start

**Getting an error about `sleep_model.h5` not found?**

👉 **[COPY_MODEL_GUIDE.md](COPY_MODEL_GUIDE.md)** - Step-by-step fix (30 seconds)

**Want the 5-minute version?**

👉 **[QUICKSTART.md](QUICKSTART.md)** - Get running in 5 minutes

**Want everything at a glance?**

👉 **[CHEATSHEET.md](CHEATSHEET.md)** - One-page reference

## Features

- 🛌 **Sleep Stage Prediction**: Classifies sleep stages (Wake, N1, N2, N3, REM, Movement, Unscored)
- 📊 **Sleep Quality Scoring**: Calculates multi-factor sleep quality scores
- 📤 **Multiple Input Formats**: Accept CSV files, JSON arrays, or radar data
- 📡 **Radar Integration**: Collect and process mmWave radar vital signs data
- 🔄 **CORS Enabled**: Ready for cross-origin requests
- 🐳 **Docker Support**: Easy containerized deployment
- 📝 **Interactive API Docs**: Automatic Swagger UI documentation

## Sleep Quality Metrics

The API calculates five key metrics:

1. **Duration Score** (35%): Sleep duration vs 8-hour ideal
2. **Efficiency Score** (20%): Percentage of non-wake sleep
3. **Deep Sleep Score** (15%): N1, N2, N3 stages vs 20% ideal
4. **REM Sleep Score** (15%): REM sleep vs 25% ideal
5. **HRV Score** (15%): Heart Rate Variability (RMSSD)

**Final Score**: Weighted combination of all metrics
- **80+**: Excellent
- **65-79**: Good
- **50-64**: Fair
- **35-49**: Poor
- **<35**: Very Poor

## Installation

### Prerequisites

- Python 3.8+
- pip or conda
- (Optional) Docker & Docker Compose

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd hosting
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Place model file**
   ```bash
   # Copy your trained sleep_model.h5 to the hosting directory
   cp ../sleep_model.h5 .
   ```

6. **Run the server**
   ```bash
   python main.py
   # Or using uvicorn directly:
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

The API will be available at `http://localhost:8000`

## Docker Deployment

### Using Docker Compose (Recommended)

1. **Build and run**
   ```bash
   docker-compose up -d
   ```

2. **Check logs**
   ```bash
   docker-compose logs -f sleep-api
   ```

3. **Stop the service**
   ```bash
   docker-compose down
   ```

### Using Docker directly

1. **Build the image**
   ```bash
   docker build -t sleep-quality-api .
   ```

2. **Run the container**
   ```bash
   docker run -p 8000:8000 \
     -e MODEL_PATH=/app/models/sleep_model.h5 \
     -v $(pwd)/models:/app/models \
     sleep-quality-api
   ```

## API Endpoints

### 1. Health Check
```
GET /health
```

Response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "num_classes": 7
}
```

### 2. Predict from CSV
```
POST /predict/csv
```

Upload a CSV file with at least one column named `HR` containing heart rate values.

**Example:**
```bash
curl -X POST "http://localhost:8000/predict/csv" \
  -F "file=@test_data.csv"
```

### 3. Predict from JSON Array
```
POST /predict/array
```

Submit heart rate data as JSON.

**Request:**
```json
{
  "hr_values": [60, 61, 62, 63, 64, 65, ...]
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/predict/array" \
  -H "Content-Type: application/json" \
  -d '{"hr_values": [60, 61, 62, 63, 64, 65]}'
```

### 4. API Documentation
```
GET /docs        # Swagger UI
GET /redoc       # ReDoc
```

### 5. Example Requests
```
GET /predict/example
```

## Response Format

```json
{
  "total_windows": 100,
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
    },
    ...
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

## Configuration

Edit `.env` to customize:

```env
# Model Configuration
MODEL_PATH=sleep_model.h5
WINDOW_SIZE=640

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False

# Server Configuration
WORKERS=4
TIMEOUT=120
```

## Data Requirements

- **Input**: Heart rate values (in bpm)
- **Minimum samples**: 640 (640 samples @ 20Hz = 32 seconds minimum)
- **Sampling rate**: Designed for 20Hz data (or downsampled to 20Hz)
- **Format**: Integer or float values

## File Structure

```
hosting/
├── main.py                 # FastAPI application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker containerization
├── docker-compose.yml     # Docker Compose configuration
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
├── README.md              # This file
└── sleep_model.h5         # Trained model (not included, add manually)
```

## Development

### Running Tests

```bash
pip install pytest pytest-asyncio httpx
pytest
```

### Code Style

```bash
pip install black flake8
black main.py config.py
flake8 main.py config.py
```

## Deployment to Cloud

### Heroku

1. Create `Procfile`:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

2. Deploy:
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

### AWS (using Elastic Beanstalk)

1. Install EB CLI
2. Initialize and deploy:
   ```bash
   eb init
   eb create sleep-api-env
   eb deploy
   ```

### Google Cloud Run

```bash
gcloud run deploy sleep-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Azure App Service

```bash
az group create --name myResourceGroup --location eastus
az appservice plan create --name myAppService --resource-group myResourceGroup --sku B1 --is-linux
az webapp create --resource-group myResourceGroup --plan myAppService --name sleepapi --runtime "PYTHON|3.10"
az webapp up --resource-group myResourceGroup --name sleepapi
```

## Troubleshooting

### Model Not Found
- Ensure `sleep_model.h5` is in the hosting directory
- Check `MODEL_PATH` in `.env`

### Port Already in Use
```bash
# Change port in .env or use:
uvicorn main:app --port 8001
```

### ModuleNotFoundError
```bash
pip install -r requirements.txt --upgrade
```

### Docker Issues
```bash
# Clear cache and rebuild
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

## API Usage Examples

### Python
```python
import requests

# JSON array method
response = requests.post(
    'http://localhost:8000/predict/array',
    json={'hr_values': [60, 61, 62, 63, ...]}
)
result = response.json()
print(f"Sleep Quality: {result['sleep_quality']['final_score']}")
```

### cURL
```bash
# CSV file method
curl -X POST http://localhost:8000/predict/csv \
  -F "file=@heart_rate_data.csv"

# JSON method
curl -X POST http://localhost:8000/predict/array \
  -H "Content-Type: application/json" \
  -d '{"hr_values": [60, 61, 62, 63, 64, 65]}'
```

### JavaScript/Fetch
```javascript
const response = await fetch('http://localhost:8000/predict/array', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ hr_values: [60, 61, 62, 63, 64, 65] })
});
const result = await response.json();
console.log(result.sleep_quality.final_score);
```

## License

[Add your license here]

## Support

For issues and questions:
- Create an issue on GitHub
- Contact: [your-email@example.com]

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

**Last Updated**: March 2026
**Version**: 1.0.0
