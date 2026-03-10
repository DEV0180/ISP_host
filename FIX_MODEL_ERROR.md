# Quick Fix: Model Not Found Error

## The Problem

You're seeing this error:
```
Error loading model: [Errno 2] Unable to synchronously open file 
(unable to open file: name = 'sleep_model.h5', errno = 2...)
```

**This is because** `sleep_model.h5` is not in the `hosting` directory.

---

## Solution

### Option 1: Copy Model from Parent Directory (Recommended)

The model is in the parent folder. Copy it to hosting:

```bash
# From the hosting directory
cd hosting

# Windows
copy ..\sleep_model.h5 .

# macOS/Linux
cp ../sleep_model.h5 .

# Or full path
copy "D:\IIT KHARAGPUR\Sem6\IS Project\sleep_model.h5" .
```

Then restart the server:
```bash
python main.py
```

You should see:
```
✓ Model loaded successfully. Classes: 7
```

### Option 2: Use Full Path in .env

Edit `.env` file:

```env
MODEL_PATH=D:\IIT KHARAGPUR\Sem6\IS Project\sleep_model.h5
```

Or using forward slashes:
```env
MODEL_PATH=../sleep_model.h5
```

### Option 3: Download Model

If the model doesn't exist:

1. Ensure you've run the training notebook cells
2. The model should be generated from [worl.ipynb](../worl.ipynb)
3. Check if `sleep_model.h5` exists in `d:\IIT KHARAGPUR\Sem6\IS Project\`

---

## Verification

### Check If Model Exists

```bash
# Windows (from hosting directory)
dir ..\sleep_model.h5

# macOS/Linux
ls -lh ../sleep_model.h5
```

Should show file size (few MB to few hundred MB)

### Check File in API

Once running, visit:
```
http://localhost:8000/health
```

Should show:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "num_classes": 7
}
```

---

## What This Error Means

- ✅ API is running
- ❌ Model file is missing
- ❌ Cannot make predictions until model is loaded
- ✅ `/health` endpoint still works
- ✅ `/docs` page still loads

---

## Usage While Fixed

Until you fix it:
- ✅ API server runs: `http://localhost:8000`
- ✅ Swagger UI available: `http://localhost:8000/docs`
- ❌ Cannot use `/predict/*` endpoints
- ❌ Cannot use `/radar/predict` endpoint
- ✓ Can use `/radar/process` (converts phase to HR without model)

---

## Step-by-Step Fix

### 1. Check Current Location
```bash
# You should be in hosting directory
cd hosting
```

### 2. Verify Model Exists
```bash
# Windows - check parent directory
cd ..
dir sleep_model.h5
cd hosting

# macOS/Linux
ls ../sleep_model.h5
```

### 3. Copy the Model
```bash
# Windows
copy ..\sleep_model.h5 .

# macOS/Linux
cp ../sleep_model.h5 .
```

### 4. Verify Copy
```bash
# Check if file exists in hosting directory
# Windows
dir sleep_model.h5

# macOS/Linux
ls -lh sleep_model.h5
```

### 5. Restart Server
```bash
python main.py
```

### 6. Test
```bash
# In another terminal
curl http://localhost:8000/health
```

Should show: `"model_loaded": true`

---

## If Model Still Doesn't Exist

You need to **train the model** first:

1. Open `worl.ipynb` notebook
2. Run the **"traning code"** cell
3. This creates `sleep_model.h5` in the project root
4. Then copy to hosting directory (steps above)

---

## Common Issues

| Issue | Solution |
|-------|----------|
| "File not found in parent" | Run training notebook to create model |
| "Copy command doesn't work" | Use full path: `copy "D:\path\sleep_model.h5" .` |
| "File exists but still fails" | Restart Python: `Ctrl+C` then `python main.py` |
| "Permission denied" | Run terminal as Administrator |

---

## After Fix

Once fixed, you can use the full API:

```bash
# Test with sample data
python test_api.py

# Collect radar data
python radar_collector.py --duration 20

# Or send JSON
curl -X POST http://localhost:8000/predict/array \
  -H "Content-Type: application/json" \
  -d '{"hr_values": [60,61,62,63,64,65]}'
```

---

## Still Having Issues?

1. **Check file permissions** - `sleep_model.h5` should be readable
2. **Check disk space** - Model may need 500MB+ disk space
3. **Check TensorFlow** - Model loading depends on TensorFlow version
4. **Restart everything** - Close terminal and start fresh
5. **Check antivirus** - File might be blocked

---

## Quick Bash Script (macOS/Linux)

Create `fix_model.sh`:
```bash
#!/bin/bash
cd hosting
if [ -f ../sleep_model.h5 ]; then
    cp ../sleep_model.h5 .
    echo "✓ Model copied successfully"
    python main.py
else
    echo "✗ Model not found in parent directory"
    echo "Please run the training notebook first"
fi
```

Then:
```bash
chmod +x fix_model.sh
./fix_model.sh
```

---

## Quick Batch Script (Windows)

Create `fix_model.bat`:
```batch
@echo off
cd hosting
if exist ..\sleep_model.h5 (
    copy ..\sleep_model.h5 .
    echo Model copied successfully
    python main.py
) else (
    echo Model not found in parent directory
    echo Please run the training notebook first
    pause
)
```

Then:
```batch
fix_model.bat
```

---

**The fix usually takes 30 seconds! 🚀**

Once done, all API endpoints will work normally.

---

**Last Updated**: March 2026
