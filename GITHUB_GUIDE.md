# GitHub Setup & Push Guide

Complete guide to initialize git, create a GitHub repository, and push your code.

## Step-by-Step Guide

### 1. Create GitHub Account & Repository

1. Go to [github.com](https://github.com) and sign up (if needed)
2. Click **+** icon in top-right → **New repository**
3. Fill in:
   - **Repository name**: `sleep-quality-api` (or your choice)
   - **Description**: `FastAPI for sleep quality analysis`
   - **Public/Private**: Choose as needed
   - **DO NOT** initialize with README (we have one)
4. Click **Create repository**

### 2. Initialize Git Locally

From the `hosting` directory:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Sleep Quality Analysis API"

# Rename default branch to main (if needed)
git branch -M main
```

### 3. Connect to GitHub

Copy the commands from GitHub repository page (looks like this):

```bash
# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/sleep-quality-api.git

# Push to GitHub
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

### 4. Verify Push

Go to your GitHub repository URL in browser:
```
https://github.com/YOUR_USERNAME/sleep-quality-api
```

You should see all your files!

---

## Complete Quick Reference

```bash
# 1. Navigate to hosting directory
cd hosting

# 2. Initialize git
git init

# 3. Add all files
git add .

# 4. Create commit
git commit -m "Initial commit: Sleep Quality Analysis API"

# 5. Add remote (replace USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/sleep-quality-api.git

# 6. Push to GitHub
git branch -M main
git push -u origin main
```

---

## Handling Large Model Files

Your `sleep_model.h5` file is large and may exceed GitHub's limits.

### Option 1: Git LFS (Recommended)

If your model is in the repository:

```bash
# Install Git LFS (download from https://git-lfs.github.com/)

# After installation
git lfs install

# Track model files
git lfs track "*.h5"

# Add and commit
git add .gitattributes sleep_model.h5
git commit -m "Add model file with Git LFS"
git push
```

### Option 2: Use GitHub Releases

1. Push code without model file:
   ```bash
   git push -u origin main
   ```

2. Go to GitHub repository
3. Click **Releases** → **Create a new release**
4. Create tag `v1.0.0`
5. Upload `sleep_model.h5` as a binary file
6. Users can download model from releases

### Option 3: Keep Model Separately

The model is already in `.gitignore`, so it won't be pushed.

Create `MODELS.md` in hosting folder:

```markdown
# Models

Download the trained model:

1. From Google Drive: [link]
2. From AWS S3: [link]
3. From GitHub Releases: [link]

Extract to `hosting/` directory before running.
```

---

## After Initial Push

### Making Changes

```bash
# Make your changes, then:

git add .                          # Add all changes
git commit -m "Description"        # Create commit
git push                           # Push to GitHub
```

### Pushing Specific Files

```bash
git add main.py                    # Add specific file
git commit -m "Update: better error handling"
git push
```

### Undoing Last Commit

```bash
git reset --soft HEAD~1            # Undo commit, keep changes
git commit -m "Corrected message"
```

---

## Troubleshooting

### "fatal: remote origin already exists"

```bash
# Reset remote
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/your-repo.git
```

### "Permission denied (publickey)"

Need to setup SSH:

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your-email@example.com"

# Add to GitHub: Settings → SSH and GPG keys → New SSH key

# Then use SSH URL instead
git remote set-url origin git@github.com:YOUR_USERNAME/sleep-quality-api.git
```

### "Cannot push because files are too large"

```bash
# Option 1: Use Git LFS (see above)

# Option 2: Remove from git history
git rm --cached sleep_model.h5
git commit -m "Remove model file"
git push
```

### "rejected because the remote contains work that you do not have locally"

```bash
git pull origin main --rebase
git push origin main
```

---

## GitHub Best Practices

### 1. Update README
Ensure [README.md](README.md) has:
- [ ] Project description
- [ ] Installation instructions
- [ ] Usage examples
- [ ] API endpoints
- [ ] Deployment guide

### 2. Use .gitignore
Already set up, but ensure it includes:
- [ ] `.env` (environment variables)
- [ ] `venv/` (virtual environment)
- [ ] `*.h5` or use Git LFS
- [ ] `__pycache__/`
- [ ] `uploads/` (user data)

### 3. Setup Branch Protection
In GitHub:
1. Settings → Branches
2. Add rule for `main`
3. Require status checks

### 4. Enable Discussions
1. Settings → Discussions
2. Turn on for community support

### 5. Add Topics
1. Settings → Repository topics
2. Add: `fastapi`, `sleep-analysis`, `ml`, etc.

---

## GitHub Actions (CI/CD)

Already configured! The `.github/workflows/tests.yml` file:
- ✓ Runs tests on every push
- ✓ Checks code quality
- ✓ Scans for vulnerabilities
- ✓ Builds Docker image

View results in the **Actions** tab.

---

## Example Workflows

### After Making Changes

```bash
# 1. Make your changes
nano main.py

# 2. Test locally
python test_api.py

# 3. Stage changes
git add main.py

# 4. Commit
git commit -m "Fix: improved error handling in predictions"

# 5. Push
git push

# 6. Watch GitHub Actions run tests automatically
# Check: GitHub → Actions tab
```

### Adding New Feature

```bash
# Create feature branch
git checkout -b feature/new-endpoint

# Make changes
# ... edit files ...

# Commit
git add .
git commit -m "Feature: add batch prediction endpoint"

# Push
git push origin feature/new-endpoint

# Create Pull Request on GitHub web interface
# Review, discuss, merge
```

---

## Deployment from GitHub

### Option 1: Heroku (Easiest)

```bash
# Install Heroku CLI
# Then in repository:

heroku login
heroku create your-app-name

# Connect GitHub for automatic deploys
# On Heroku Dashboard → Deploy tab
# or use GitHub Actions
```

### Option 2: GitHub Actions to Deploy

Create deployment workflow (already in `.github/workflows/tests.yml`)

### Option 3: Manual Docker Deployment

```bash
docker build -t username/sleep-quality-api .
docker tag username/sleep-quality-api username/sleep-quality-api:latest
docker push username/sleep-quality-api
```

---

## Useful GitHub Features

### Create Release

```bash
# Tag version
git tag v1.0.0
git push origin v1.0.0

# Then on GitHub, create release from tag
# Add model file as asset if small enough
```

### View Network
Shows all branches and commits:
- GitHub → Insights → Network

### Commit History
See all commits:
- GitHub → main branch → commit history

### Compare Branches
```
https://github.com/YOUR_USERNAME/sleep-quality-api/compare/main...develop
```

---

## Security Checklist

- [ ] `.env` is in `.gitignore`
- [ ] No API keys in code
- [ ] No model files (or use Git LFS)
- [ ] Enable branch protection
- [ ] Review GitHub's security alerts
- [ ] Don't commit secrets/credentials

---

## Command Quick Reference

```bash
# View status
git status

# View changes
git diff

# View commit history
git log

# Create branch
git checkout -b branch-name

# Switch branch
git checkout main

# Delete branch
git branch -d branch-name

# Stash changes (save for later)
git stash

# Apply stashed changes
git stash pop

# View remotes
git remote -v

# Update from remote
git pull

# Force push (use carefully!)
git push --force
```

---

## Common GitHub URLs

Replace `USERNAME` and `REPO`:

| Resource | URL |
|----------|-----|
| Repository | `github.com/USERNAME/REPO` |
| Code | `github.com/USERNAME/REPO/tree/main` |
| Issues | `github.com/USERNAME/REPO/issues` |
| Pull Requests | `github.com/USERNAME/REPO/pulls` |
| Actions | `github.com/USERNAME/REPO/actions` |
| Releases | `github.com/USERNAME/REPO/releases` |
| Settings | `github.com/USERNAME/REPO/settings` |
| Discussions | `github.com/USERNAME/REPO/discussions` |

---

## Before Pushing

Final checklist:

- [ ] Code runs without errors
- [ ] `python test_api.py` passes
- [ ] `README.md` is up to date
- [ ] `.env` is in `.gitignore`
- [ ] Model file handled (LFS, releases, or ignored)
- [ ] No API keys in files
- [ ] `requirements.txt` is current
- [ ] Dockerfile builds successfully

---

**You're ready to push to GitHub! 🚀**

If you get stuck, revisit this guide or check:
- [GitHub Docs](https://docs.github.com)
- [Git Guide](https://rogerdudler.github.io/git-guide/)

---

**Last Updated**: March 2026
