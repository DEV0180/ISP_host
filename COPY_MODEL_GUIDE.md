# 🔧 COPY MODEL - Step by Step

**Your problem:** `sleep_model.h5` file not found  
**Your solution:** Copy it from parent folder (30 seconds)

---

## Your Folder Structure

```
d:\IIT KHARAGPUR\Sem6\IS Project\
│
├── sleep_model.h5           ← This file
├── worl.ipynb
├── requirements.txt
├── app.py
│
└── hosting/                 ← You're here
    ├── main.py
    ├── config.py
    ├── .env
    └── ... (other files)
```

**The model is in the parent folder!**

---

## Method 1: Windows File Explorer (Easiest)

**Step 1:** Open File Explorer  
Go to: `D:\IIT KHARAGPUR\Sem6\IS Project\`

**Step 2:** Find `sleep_model.h5`  
You should see it in the folder

**Step 3:** Copy the file  
Right-click → Copy

**Step 4:** Go to hosting folder  
Open the `hosting` subfolder

**Step 5:** Paste the file  
Right-click → Paste

**Step 6:** Verify  
You should see `sleep_model.h5` in hosting folder

✅ **Done!** Now restart the server.

---

## Method 2: Windows Command Prompt (Fastest)

**Step 1:** Open Command Prompt  
Press `Win + R` → Type `cmd` → Enter

**Step 2:** Navigate to hosting
```cmd
cd D:\IIT KHARAGPUR\Sem6\IS Project\hosting
```

**Step 3:** Copy the file
```cmd
copy ..\sleep_model.h5 .
```

You should see:
```
1 file(s) copied.
```

**Step 4:** Verify
```cmd
dir sleep_model.h5
```

Should show the file with size

✅ **Done!** Restart: `python main.py`

---

## Method 3: PowerShell (Windows 10+)

**Step 1:** Open PowerShell  
Press `Win + X` → Select PowerShell

**Step 2:** Navigate and copy
```powershell
cd "D:\IIT KHARAGPUR\Sem6\IS Project\hosting"
Copy-Item ..\sleep_model.h5 .
```

**Step 3:** Verify
```powershell
ls sleep_model.h5
```

✅ **Done!** Restart: `python main.py`

---

## Method 4: macOS Terminal

**Step 1:** Open Terminal  
Cmd + Space → Type "Terminal" → Enter

**Step 2:** Navigate to hosting
```bash
cd ~/path/to/IS\ Project/hosting
```

Or if using exact path:
```bash
cd "/path/to/IIT KHARAGPUR/Sem6/IS Project/hosting"
```

**Step 3:** Copy the file
```bash
cp ../sleep_model.h5 .
```

**Step 4:** Verify
```bash
ls -lh sleep_model.h5
```

Should show: `sleep_model.h5 (some size)`

✅ **Done!** Restart: `python main.py`

---

## Method 5: Linux Terminal

**Step 1:** Open Terminal

**Step 2:** Navigate to hosting
```bash
cd /path/to/hosting
```

**Step 3:** Copy the file
```bash
cp ../sleep_model.h5 .
```

**Step 4:** Verify
```bash
ls -lh sleep_model.h5
```

✅ **Done!** Restart: `python main.py`

---

## After Copying: Restart Server

### In Terminal/Command Prompt

**Stop the current server:**
```
Press Ctrl + C
```

You'll see:
```
^C
Shutdown complete!
```

**Start it again:**
```bash
python main.py
```

**You should see:**
```
[INFO] Processing...
✓ Model loaded successfully. Classes: 7
INFO: Uvicorn running on http://0.0.0.0:8000
```

✅ **Success!** No more model error.

---

## How to Verify It Worked

### In Browser

Visit: `http://localhost:8000/health`

You should see:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "num_classes": 7
}
```

### In Terminal

```bash
# Windows
curl http://localhost:8000/health

# macOS/Linux
curl http://localhost:8000/health
```

### Visit Swagger UI

Open browser:
```
http://localhost:8000/docs
```

All endpoints listed = Working! ✅

---

## If Copy Command Shows Error

### "File not found"

**Check the file exists:**

Windows:
```cmd
dir ..\sleep_model.h5
```

macOS/Linux:
```bash
ls ../sleep_model.h5
```

### "Access denied"

**Try as Administrator (Windows):**
1. Right-click Command Prompt
2. Select "Run as administrator"
3. Try copy command again

### "Permission denied" (Mac/Linux)

```bash
# Try with sudo
sudo cp ../sleep_model.h5 .

# Enter your password when asked
```

---

## Visual Diagram

```
Before (Error):
─────────────────────────────────────────
IS Project/
├── sleep_model.h5 ✓ (exists, but in wrong place)
└── hosting/
    ├── main.py
    └── ... (ERROR: can't find model)

After (Fixed):
─────────────────────────────────────────
IS Project/
├── sleep_model.h5 (original)
└── hosting/
    ├── sleep_model.h5 ✓ (COPY HERE)
    ├── main.py
    └── ... (now works!)
```

---

## File Size Check

After copying, check file size:

**Windows:**
```cmd
dir sleep_model.h5
```

Should show size like:
```
sleep_model.h5          123,456,789 bytes
```
(Not 0 KB!)

**macOS/Linux:**
```bash
ls -lh sleep_model.h5
```

Should show size like:
```
-rw-r--r-- 1 user group 117M Mar 10 12:00 sleep_model.h5
```
(Not empty!)

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Cannot find .." | Make sure you're in `hosting` folder |
| "File not found" | Parent folder doesn't exist; check path |
| "Permission denied" | Run as Administrator |
| "Copy failed" | Close any open files, try again |
| "Still getting error after copy" | Restart terminal & server |

---

## Quick One-Liner Commands

### Windows (Copy & Paste This)
```cmd
cd D:\IIT KHARAGPUR\Sem6\IS Project\hosting & copy ..\sleep_model.h5 . & python main.py
```

### macOS/Linux (Copy & Paste This)
```bash
cd "path/to/hosting" && cp ../sleep_model.h5 . && python main.py
```

---

## ✅ Confirmation Checklist

After following steps above:

- [ ] Found `sleep_model.h5` in parent folder
- [ ] Copied it to `hosting` folder
- [ ] Can see it in `hosting` folder (file explorer/ls)
- [ ] Restarted the server (`python main.py`)
- [ ] Checked `/health` endpoint (shows `"model_loaded": true`)
- [ ] API is running without model errors

**All checked?** You're done! 🎉

---

## Next: Use the API

Once model is fixed:

```bash
# Test the API
python test_api.py

# Collect radar data
python radar_collector.py --duration 20

# Browse API docs
# Open: http://localhost:8000/docs
```

---

## Still Having Issues?

1. Read the [FIX_MODEL_ERROR.md](FIX_MODEL_ERROR.md) guide
2. Check [QUICKSTART.md](QUICKSTART.md) for general setup
3. See [README.md](README.md) for full documentation
4. Check [CHEATSHEET.md](CHEATSHEET.md) for quick reference

---

**That's it! Really simple. 30 seconds. You got this! 🚀**

---

**Last Updated**: March 2026
