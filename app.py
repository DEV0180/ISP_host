"""
Sleep Quality Analysis Frontend
Web interface for collecting radar data and analyzing sleep quality
"""

import csv
import datetime
import json
import os
import threading
import time
from typing import Optional

import numpy as np
from flask import Flask, request, jsonify
import requests

# ================= OPTIONAL: Radar Support =================
RADAR_AVAILABLE = False
try:
    import serial
    from mmWave import vitalsign
    RADAR_AVAILABLE = True
except ImportError:
    print("[WARNING] mmWave/serial libraries not available. Radar features disabled.")
    vitalsign = None

# ================= CONFIGURATION =================
API_URL = "http://localhost:8000"  # FastAPI backend URL
UPLOADS_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOADS_FOLDER, exist_ok=True)

DURATION_SEC = 20  # Default radar duration
COM_PORT = "COM14"  # Default COM port
BAUDRATE = 921600
# ===============================================

app = Flask(__name__, template_folder=".", static_folder=".")
app.config['UPLOAD_FOLDER'] = UPLOADS_FOLDER


class RadarError(Exception):
    """Custom radar exception"""
    pass


def open_radar_port(port_name: str) -> serial.Serial:
    """Open serial connection to radar"""
    try:
        if not RADAR_AVAILABLE:
            raise RadarError("Radar libraries not installed")
        port = serial.Serial(port_name, baudrate=BAUDRATE, timeout=0.5)
        print(f"[INFO] Opened radar port: {port_name}")
        return port
    except Exception as e:
        raise RadarError(f"Failed to open {port_name}: {e}")


def collect_radar_data(
    duration: float,
    port_name: str,
    output_path: Optional[str] = None,
    stop_event: Optional[threading.Event] = None,
) -> str:
    """Collect radar data to CSV file"""
    if not RADAR_AVAILABLE or vitalsign is None:
        raise RadarError("Radar not available")

    if duration <= 0:
        raise ValueError("Duration must be positive")

    stop_event = stop_event or threading.Event()

    try:
        port = open_radar_port(port_name)
        vts = vitalsign.VitalSign(port)
        port.flushInput()
    except Exception as e:
        raise RadarError(f"Failed to initialize radar: {e}")

    if output_path is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(UPLOADS_FOLDER, f"radar_data_{timestamp}.csv")

    start_time = time.time()
    print(f"[INFO] Recording radar data for {duration} seconds...")

    try:
        with open(output_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["time_sec", "unwrapPhasePeak_mm"])
            count = 0

            while True:
                if stop_event.is_set():
                    print("[INFO] Stop signal received")
                    break

                elapsed = time.time() - start_time
                if elapsed >= duration:
                    print("[INFO] Duration completed")
                    break

                try:
                    dck, vd, rangeBuf = vts.tlvRead(False)
                    if not dck:
                        continue
                    value = vd.unwrapPhasePeak_mm
                    writer.writerow([elapsed, value])
                    count += 1
                except Exception as e:
                    print(f"[WARNING] Error reading data: {e}")
                    continue

    except Exception as e:
        print(f"[ERROR] Error writing data: {e}")
        raise
    finally:
        print("[INFO] Closing radar")
        try:
            vts.close()
        except Exception:
            pass
        try:
            port.close()
        except Exception:
            pass

    print(f"[INFO] Collected {count} samples. Data saved to: {output_path}")
    return output_path


@app.route("/")
def index():
    """Home page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sleep Quality Analysis</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #333; text-align: center; }
            .welcome { text-align: center; padding: 40px 0; }
            .start-btn { background-color: #28a745; color: white; padding: 15px 40px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
            .start-btn:hover { background-color: #218838; }
            .card { border: 1px solid #ddd; padding: 20px; margin: 20px 0; border-radius: 5px; display: none; }
            .card.show { display: block; }
            button { background-color: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin-top: 10px; }
            button:hover { background-color: #0056b3; }
            input, textarea { padding: 8px; margin: 5px 0; width: 100%; box-sizing: border-box; }
            .result { background-color: #f0f0f0; padding: 15px; border-radius: 5px; margin-top: 20px; }
            .error { color: red; font-weight: bold; }
            .success { color: green; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>😴 Sleep Quality Analysis Platform</h1>
        
        <div class="welcome" id="welcome">
            <p>Welcome to the Sleep Quality Analysis System</p>
            <p>Analyze your sleep patterns using heart rate data or radar sensors</p>
            <button class="start-btn" onclick="startAnalysis()">Start Analysis</button>
        </div>

        <div id="toolsContainer">
            <div class="card" id="csvCard">
                <h2>📤 Upload CSV File</h2>
                <input type="file" id="csvFile" accept=".csv">
                <button onclick="uploadCSV()">Analyze CSV</button>
                <div id="csvResult"></div>
            </div>

            <div class="card" id="hrCard">
                <h2>📊 Send Heart Rate Data</h2>
                <textarea id="hrData" placeholder="Paste comma-separated HR values (min 640 values)" style="height: 100px;"></textarea>
                <button onclick="sendHRData()">Analyze Heart Rate</button>
                <div id="hrResult"></div>
            </div>

            <div class="card" id="radarCard">
                <h2>📡 Collect Radar Data</h2>
                <label>Duration (seconds): <input type="number" id="duration" value="20" min="5" max="300"></label>
                <label>COM Port: <input type="text" id="comPort" value="COM14"></label>
                <button onclick="collectRadar()">Start Radar Collection</button>
                <div id="radarResult"></div>
            </div>

            <div class="card" id="healthCard">
                <h2>❤️ Health Check</h2>
                <button onclick="checkHealth()">Check API Status</button>
                <div id="healthResult"></div>
            </div>
        </div>

        <script>
            const API_URL = "http://localhost:8000";

            function startAnalysis() {
                document.getElementById('welcome').style.display = 'none';
                document.getElementById('csvCard').classList.add('show');
                document.getElementById('hrCard').classList.add('show');
                document.getElementById('radarCard').classList.add('show');
                document.getElementById('healthCard').classList.add('show');
            }

            async function uploadCSV() {
                const file = document.getElementById('csvFile').files[0];
                if (!file) { alert('Please select a file'); return; }
                
                const formData = new FormData();
                formData.append('file', file);
                
                try {
                    const res = await fetch(API_URL + '/predict/csv', { method: 'POST', body: formData });
                    const data = await res.json();
                    
                    if (res.ok) {
                        displayResult('csvResult', data);
                    } else {
                        document.getElementById('csvResult').innerHTML = '<p class="error">Error: ' + (data.detail || data.error || 'Unknown error') + '</p>';
                    }
                } catch (e) {
                    document.getElementById('csvResult').innerHTML = '<p class="error">Error: ' + e.message + '</p>';
                }
            }

            async function sendHRData() {
                const data = document.getElementById('hrData').value.split(',').map(x => parseFloat(x.trim())).filter(x => !isNaN(x));
                if (data.length < 640) { alert('Need at least 640 samples'); return; }
                
                try {
                    const res = await fetch(API_URL + '/predict/array', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ hr_values: data })
                    });
                    const result = await res.json();
                    
                    if (res.ok) {
                        displayResult('hrResult', result);
                    } else {
                        document.getElementById('hrResult').innerHTML = '<p class="error">Error: ' + (result.detail || result.error || 'Unknown error') + '</p>';
                    }
                } catch (e) {
                    document.getElementById('hrResult').innerHTML = '<p class="error">Error: ' + e.message + '</p>';
                }
            }

            async function collectRadar() {
                const duration = document.getElementById('duration').value;
                const comPort = document.getElementById('comPort').value;
                
                try {
                    const res = await fetch('/collect-radar', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ duration: parseInt(duration), port: comPort })
                    });
                    const data = await res.json();
                    
                    if (data.success) {
                        document.getElementById('radarResult').innerHTML = '<p class="success">✓ Data collected! Analyzing...</p>';
                        analyzeRadarData(data.file_path);
                    } else {
                        document.getElementById('radarResult').innerHTML = '<p class="error">Error: ' + data.error + '</p>';
                    }
                } catch (e) {
                    document.getElementById('radarResult').innerHTML = '<p class="error">Error: ' + e.message + '</p>';
                }
            }

            async function analyzeRadarData(filePath) {
                try {
                    const res = await fetch('/analyze-radar', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ file_path: filePath })
                    });
                    const data = await res.json();
                    if (data.success) {
                        displayResult('radarResult', data.result);
                    } else {
                        document.getElementById('radarResult').innerHTML = '<p class="error">Error: ' + data.error + '</p>';
                    }
                } catch (e) {
                    document.getElementById('radarResult').innerHTML = '<p class="error">Error analyzing: ' + e.message + '</p>';
                }
            }

            async function checkHealth() {
                try {
                    const res = await fetch(API_URL + '/health');
                    const data = await res.json();
                    const status = data.model_loaded ? '<p class="success">✓ API Healthy</p>' : '<p class="error">✗ Model not loaded</p>';
                    document.getElementById('healthResult').innerHTML = status + '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                } catch (e) {
                    document.getElementById('healthResult').innerHTML = '<p class="error">Cannot connect to API: ' + e.message + '</p>';
                }
            }

            function displayResult(elementId, data) {
                const html = '<div class="result"><h3>✓ Analysis Results</h3>' +
                    '<p><strong>Sleep Score:</strong> ' + data.sleep_quality.final_score + '% (' + data.sleep_quality.quality_level + ')</p>' +
                    '<p><strong>Duration:</strong> ' + data.total_duration.hours + ' hours</p>' +
                    '<p><strong>Component Scores:</strong></p>' +
                    '<ul>' +
                    '<li>Duration: ' + data.sleep_scores.duration_score + '%</li>' +
                    '<li>Efficiency: ' + data.sleep_scores.efficiency_score + '%</li>' +
                    '<li>Deep Sleep: ' + data.sleep_scores.deep_sleep_score + '%</li>' +
                    '<li>REM Sleep: ' + data.sleep_scores.rem_sleep_score + '%</li>' +
                    '<li>HRV: ' + data.sleep_scores.hrv_score + '%</li>' +
                    '</ul></div>';
                document.getElementById(elementId).innerHTML = html;
            }
        </script>
    </body>
    </html>
    """


@app.route("/collect-radar", methods=["POST"])
def collect_radar():
    """Endpoint to collect radar data"""
    try:
        data = request.json
        duration = data.get('duration', DURATION_SEC)
        port = data.get('port', COM_PORT)

        if not RADAR_AVAILABLE:
            return jsonify({'success': False, 'error': 'Radar not available. Install: pip install pyserial mmWave'})

        if duration < 5 or duration > 300:
            return jsonify({'success': False, 'error': 'Duration must be between 5 and 300 seconds'})

        file_path = collect_radar_data(duration, port)
        return jsonify({'success': True, 'file_path': file_path})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route("/analyze-radar", methods=["POST"])
def analyze_radar():
    """Analyze collected radar data (convert phase to HR and predict sleep)"""
    try:
        data = request.json
        file_path = data.get('file_path')

        if not os.path.exists(file_path):
            return jsonify({'success': False, 'error': 'File not found'})

        # Read CSV
        time_sec = []
        phase_data = []
        with open(file_path, 'r') as f:
            f.readline()  # Skip header
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    try:
                        time_sec.append(float(parts[0]))
                        phase_data.append(float(parts[1]))
                    except ValueError:
                        continue

        if not phase_data:
            return jsonify({'success': False, 'error': 'No valid data in file'})

        # Convert phase data to HR values (simple conversion)
        # Phase peak in mm -> approximate HR (60-100 bpm range)
        phase_array = np.array(phase_data)
        hr_values = 60 + (phase_array - phase_array.min()) / (phase_array.max() - phase_array.min() + 0.001) * 40
        hr_values = np.clip(hr_values, 40, 150).tolist()

        # Send to API
        try:
            res = requests.post(f"{API_URL}/predict/array", json={'hr_values': hr_values}, timeout=60)
            if res.status_code == 200:
                return jsonify({'success': True, 'result': res.json()})
            else:
                return jsonify({'success': False, 'error': 'API Error: ' + str(res.status_code)})
        except requests.exceptions.ConnectionError:
            return jsonify({'success': False, 'error': 'Cannot connect to API backend. Is it running on port 8000?'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


# ================= MAIN =================
if __name__ == "__main__":
    print("Starting Sleep Quality Analysis Frontend")
    print(f"API Backend: {API_URL}")
    print(f"Radar Support: {'✓ Available' if RADAR_AVAILABLE else '✗ Not available'}")
    print("Open browser: http://localhost:5000")
    app.run(debug=True, port=5000, host="0.0.0.0")
