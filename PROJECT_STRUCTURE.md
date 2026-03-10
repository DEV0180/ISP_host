# Project Structure Guide

## Directory Layout

```
hosting/
├── main.py                          # Main FastAPI application
├── config.py                        # Configuration and settings
├── test_api.py                      # API testing script
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Docker containerization
├── docker-compose.yml               # Docker Compose configuration
├── Procfile                         # Heroku deployment config
├── .env.example                     # Environment variables template
├── .env                            # Environment variables (git ignored)
├── .gitignore                      # Git ignore rules
├── README.md                       # Main documentation
├── DEPLOYMENT.md                   # Deployment guide
├── PROJECT_STRUCTURE.md            # This file
│
├── .github/
│   └── workflows/
│       └── tests.yml              # GitHub Actions CI/CD
│
├── models/                         # Directory for model files (created at runtime)
│   └── sleep_model.h5            # Trained model (git ignored)
│
├── uploads/                        # Directory for uploaded files (created at runtime)
│   └── test_data.csv            # User uploaded files (git ignored)
│
└── logs/                          # Directory for log files (created at runtime)
    └── app.log                   # Application logs (git ignored)
```

## File Descriptions

### Core Application Files

| File | Purpose |
|------|---------|
| `main.py` | FastAPI application with all endpoints |
| `config.py` | Configuration management and constants |
| `requirements.txt` | Python package dependencies |

### Deployment Files

| File | Purpose |
|------|---------|
| `Dockerfile` | Docker image definition |
| `docker-compose.yml` | Multi-container orchestration |
| `Procfile` | Heroku deployment configuration |
| `.env.example` | Environment variables template |
| `.env` | Local environment variables (not committed) |

### Testing & CI/CD

| File | Purpose |
|------|---------|
| `test_api.py` | Automated API testing script |
| `.github/workflows/tests.yml` | GitHub Actions CI/CD pipeline |

### Documentation

| File | Purpose |
|------|---------|
| `README.md` | Main project documentation |
| `DEPLOYMENT.md` | Deployment to various cloud platforms |
| `PROJECT_STRUCTURE.md` | This file - directory structure guide |

### Git Configuration

| File | Purpose |
|------|---------|
| `.gitignore` | Files to exclude from version control |
| `.github/workflows/` | Automated workflows (tests, builds, deploys) |

## What's Git Ignored (Not Committed)

```
__pycache__/              # Python bytecode
*.pyc                     # Compiled Python files
.env                      # Local environment variables
.env.local                # Local overrides
venv/                     # Virtual environment
env/                      # Alternative virtual env
*.h5                      # Model files (use Git LFS or releases)
*.csv                     # Data files
uploads/                  # User uploaded files
logs/                     # Application logs
.vscode/                  # VS Code settings
.idea/                    # PyCharm settings
```

## Directory Usage

### At Runtime

These directories are created automatically:

```
models/          # ML model files
├── sleep_model.h5
└── other-models/

uploads/        # User uploaded CSV files
├── data1.csv
└── data2.csv

logs/           # Application logs
├── app.log
└── error.log
```

## How to Use This Structure

### Development

```bash
cd hosting/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Docker Development

```bash
docker-compose up
# App runs in container, accessible at localhost:8000
```

### Testing

```bash
python test_api.py
# Full test suite runs against the API
```

### Deployment

- **Heroku**: `git push heroku main`
- **Docker**: `docker push username/sleep-quality-api`
- **Cloud Run**: `gcloud run deploy`
- **EB**: `eb deploy`

## Adding New Files

When adding new files, consider:

1. **Is it code?** → Add to root or create subdirectory
2. **Is it a test?** → Use `test_*.py` naming convention
3. **Is it data?** → Add to `.gitignore` (data shouldn't be in git)
4. **Is it configuration?** → Consider adding to `config.py`
5. **Is it documentation?** → Use `.md` extension
6. **Is it a dependency?** → Update `requirements.txt`

## Important Notes

### Model Files

- **Do not commit** binary model files (`.h5`) to git directly
- **Use Git LFS** for version control of model files, OR
- **Store separately** with download instructions, OR
- **Use releases** to attach model files to GitHub releases

### Environment Variables

- **Never commit** `.env` to git
- Always provide `.env.example` with template
- Documents what variables are needed

### Virtual Environment

- **Never commit** `venv/` or `env/`
- Always listed in `.gitignore`
- Recreated with `pip install -r requirements.txt`

### Large Files

- CSV data files → `.gitignore`
- Uploaded files → `.gitignore` (uploads/)
- Log files → `.gitignore` (logs/)
- Model files → Git LFS or releases

## Recommended GitHub Settings

1. **Add protection rule for `main` branch**
   - Require status checks to pass before merge
   - Require PR reviews before merge
   - Dismiss stale PR approvals

2. **Set up branch deletion rule**
   - Auto-delete head branches after merge

3. **Configure branch protection exemptions**
   - Allow administrators to bypass requirements when necessary

## Quick Reference

### File Size Limits

- GitHub: 100 MB per file
- Git LFS: Recommended for files > 50 MB
- Docker Hub: Consider image compression

### Python Version Compatibility

- Minimum: Python 3.8
- Tested with: 3.9, 3.10, 3.11
- Recommended: 3.10+

### Key Dependencies

```
fastapi==0.104.1       # Web framework
uvicorn==0.24.0        # ASGI server
tensorflow==2.14.0     # ML model loading
pandas==2.0.3          # Data handling
numpy==1.24.3          # Numerical computing
```

---

**Last Updated**: March 2026
**Version**: 1.0.0
