# Deployment Guide

This guide covers how to deploy the Sleep Quality Analysis API to various platforms.

## Table of Contents

1. [Local Development](#local-development)
2. [GitHub Setup](#github-setup)
3. [Cloud Deployment](#cloud-deployment)
4. [Production Checklist](#production-checklist)

---

## Local Development

### Setup

1. **Clone and setup**
   ```bash
   git clone <your-repo-url>
   cd hosting
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Add model file**
   ```bash
   cp ../sleep_model.h5 .
   ```

4. **Run locally**
   ```bash
   python main.py
   # API available at http://localhost:8000
   ```

5. **Test the API**
   ```bash
   pip install requests
   python test_api.py
   ```

---

## GitHub Setup

### Initial Repository Setup

1. **Initialize git (if not already done)**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Sleep Quality Analysis API"
   ```

2. **Create GitHub repository**
   - Go to github.com and create a new repository
   - Name it `sleep-quality-api` or similar
   - DO NOT initialize with README (we already have one)

3. **Add remote and push**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/sleep-quality-api.git
   git branch -M main
   git push -u origin main
   ```

### Important: Handle Large Model Files

**Note**: Git has a 100MB file limit. The `sleep_model.h5` file should be handled separately:

#### Option 1: Git LFS (Recommended)
```bash
# Install Git LFS
# From: https://git-lfs.github.com/

# Track model files
git lfs install
git lfs track "*.h5"

# Add and commit
git add .gitattributes
git commit -m "Setup Git LFS for model files"

# Add model file
git add sleep_model.h5
git commit -m "Add trained sleep model"
git push
```

#### Option 2: Store Separately
Create a `MODELS.md` in the root directory:

```markdown
# Model Files

Download the trained model from:
- [Google Drive Link](#)
- [AWS S3 Link](#)

Place `sleep_model.h5` in the hosting directory before running.
```

Then push to GitHub without the model file (already in `.gitignore`).

#### Option 3: GitHub Releases
```bash
# Create release with model
git tag v1.0.0
git push origin v1.0.0

# Upload sleep_model.h5 on GitHub Releases web interface
```

---

## Cloud Deployment

### Docker Hub (for containerized deployment)

1. **Build the image**
   ```bash
   docker build -t YOUR_USERNAME/sleep-quality-api:latest .
   ```

2. **Login to Docker Hub**
   ```bash
   docker login
   ```

3. **Push to Docker Hub**
   ```bash
   docker push YOUR_USERNAME/sleep-quality-api:latest
   ```

### Heroku Deployment

1. **Install Heroku CLI**
   ```bash
   # From: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login and create app**
   ```bash
   heroku login
   heroku create your-sleep-api
   ```

3. **Deploy from GitHub**
   ```bash
   # Option A: Using Heroku Git
   git push heroku main
   
   # Option B: Connect GitHub repository
   # Go to Heroku Dashboard > Deploy > Connect to GitHub
   ```

4. **Configure environment**
   ```bash
   heroku config:set MODEL_PATH=/app/sleep_model.h5
   heroku config:set DEBUG=False
   ```

5. **View logs**
   ```bash
   heroku logs --tail
   ```

6. **Access your API**
   ```
   https://your-sleep-api.herokuapp.com
   https://your-sleep-api.herokuapp.com/docs  # Swagger UI
   ```

**Note**: Heroku has storage limitations. For large model files:
- Store on AWS S3 and download at startup
- Use Heroku Buildpacks to manage large files

### AWS Elastic Beanstalk

1. **Install EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize and deploy**
   ```bash
   eb init -p python-3.10 sleep-quality-api --region us-east-1
   eb create sleep-api-prod
   eb deploy
   ```

3. **Configure environment**
   ```bash
   eb setenv MODEL_PATH=/var/app/sleep_model.h5 DEBUG=False
   ```

4. **Monitor**
   ```bash
   eb logs
   eb status
   ```

### Google Cloud Run

1. **Authenticate with Google Cloud**
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

2. **Deploy**
   ```bash
   gcloud run deploy sleep-api \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars MODEL_PATH=/app/sleep_model.h5
   ```

3. **Get the URL**
   ```bash
   gcloud run services list
   ```

### Azure App Service

1. **Login to Azure**
   ```bash
   az login
   ```

2. **Create resource group**
   ```bash
   az group create --name myResourceGroup --location eastus
   ```

3. **Create app service plan**
   ```bash
   az appservice plan create \
     --name myAppServicePlan \
     --resource-group myResourceGroup \
     --sku B2 --is-linux
   ```

4. **Create and deploy web app**
   ```bash
   az webapp create \
     --resource-group myResourceGroup \
     --plan myAppServicePlan \
     --name sleep-quality-api \
     --runtime "PYTHON|3.10"
   
   az webapp deployment source config-zip \
     --resource-group myResourceGroup \
     --name sleep-quality-api \
     --src app.zip
   ```

### DigitalOcean App Platform

1. **Connect GitHub**
   - Login to DigitalOcean
   - Go to App Platform > Create App
   - Select your GitHub repository

2. **Configure app spec**
   - Set build command: `pip install -r requirements.txt`
   - Set run command: `uvicorn main:app --host 0.0.0.0 --port 8080`
   - Set HTTP port: 8080

3. **Deploy**
   - Click "Deploy Now"

### PythonAnywhere

1. **Upload your code**
   ```bash
   # Via git
   git clone <your-repo> /home/username/sleep-api
   ```

2. **Create web app**
   - Go to Web tab > Add new web app
   - Select "Python 3.10"
   - Select "FastAPI"

3. **Configure WSGI file**
   ```python
   # /var/www/username_pythonanywhere_com_wsgi.py
   from hosting.main import app as application
   ```

4. **Reload web app**
   - Hit the Reload button

---

## Production Checklist

- [ ] **Security**
  - [ ] Set `DEBUG=False` in production
  - [ ] Use HTTPS only
  - [ ] Set strong `SECRET_KEY` if using authentication
  - [ ] Configure CORS origins properly (not `["*"]`)
  - [ ] Add rate limiting
  - [ ] Implement authentication (API keys, JWT)

- [ ] **Performance**
  - [ ] Set up proper logging
  - [ ] Configure appropriate number of workers
  - [ ] Use proper reverse proxy (nginx)
  - [ ] Enable response compression
  - [ ] Set up caching if needed

- [ ] **Reliability**
  - [ ] Set up health checks
  - [ ] Configure auto-restart
  - [ ] Set up monitoring and alerts
  - [ ] Implement error tracking (Sentry)
  - [ ] Configure backups
  - [ ] Set up CI/CD pipeline

- [ ] **Documentation**
  - [ ] Update README with deployment info
  - [ ] Document API endpoints
  - [ ] Create postman collection
  - [ ] Write deployment runbooks

- [ ] **Code Quality**
  - [ ] Run tests: `pytest`
  - [ ] Check style: `flake8 main.py config.py`
  - [ ] Check formatting: `black main.py config.py`
  - [ ] Check coverage

- [ ] **Dependencies**
  - [ ] Pin exact versions in requirements.txt
  - [ ] Scan for vulnerabilities: `safety check`
  - [ ] Update regularly: `pip list --outdated`

---

## Monitoring and Maintenance

### Set Up Monitoring

```bash
# Install monitoring tools
pip install prometheus-client sentry-sdk

# Add to main.py
from prometheus_client import Counter, Histogram

request_count = Counter('requests_total', 'Total requests')
request_duration = Histogram('request_duration_seconds', 'Request duration')
```

### Regular Maintenance

1. **Weekly**
   - Check logs for errors
   - Monitor API response times
   - Check disk usage

2. **Monthly**
   - Update dependencies
   - Review security updates
   - Analyze usage patterns

3. **Quarterly**
   - Retrain model if needed
   - Review and improve performance
   - Audit access logs

---

## Continuous Integration/Deployment

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          pip install -r requirements.txt pytest
          pytest
      - name: Deploy to Heroku
        run: |
          git push https://heroku:${{ secrets.HEROKU_API_KEY }}@git.heroku.com/${{ secrets.HEROKU_APP_NAME }}.git main
```

---

## Troubleshooting Deployments

| Issue | Solution |
|-------|----------|
| "Model not found" | Ensure model file is in correct path or downloaded on startup |
| "Port already in use" | Change port in configuration or use different port number |
| "Out of memory" | Increase available memory or optimize model loading |
| "Timeout errors" | Increase timeout in config, optimize predictions |
| "CORS errors" | Configure CORS origins in main.py |

---

## Support

For issues:
- Check logs: `docker-compose logs` or `heroku logs --tail`
- See README.md troubleshooting section
- Create GitHub issue with error details

---

**Last Updated**: March 2026
**Version**: 1.0.0
