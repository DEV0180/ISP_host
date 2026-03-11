# Add HTMLResponse to your fastapi imports
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse 
# ... (keep your other imports)

# ... (keep your existing FastAPI setup, CORS, model loading, and process_sleep_data functions)

# 1. Add this new endpoint to serve your UI
@app.get("/", response_class=HTMLResponse)
async def get_ui():
    """Serve the Web Interface"""
    # Notice we changed API_URL to be a relative path '' since it's the same server
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sleep Quality Analysis</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #333; text-align: center; }
            .welcome { text-align: center; padding: 40px 0; }
            .start-btn { background-color: #28a745; color: white; padding: 15px 40px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
            .card { border: 1px solid #ddd; padding: 20px; margin: 20px 0; border-radius: 5px; display: none; }
            .card.show { display: block; }
            button { background-color: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin-top: 10px; }
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
            <p>Analyze your sleep patterns using heart rate data</p>
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

            <div class="card" id="healthCard">
                <h2>❤️ Health Check</h2>
                <button onclick="checkHealth()">Check API Status</button>
                <div id="healthResult"></div>
            </div>
        </div>

        <script>
            // No need for a hardcoded API_URL, it uses the current domain!
            const API_BASE = "";

            function startAnalysis() {
                document.getElementById('welcome').style.display = 'none';
                document.getElementById('csvCard').classList.add('show');
                document.getElementById('hrCard').classList.add('show');
                document.getElementById('healthCard').classList.add('show');
            }

            async function uploadCSV() {
                const file = document.getElementById('csvFile').files[0];
                if (!file) { alert('Please select a file'); return; }
                
                const formData = new FormData();
                formData.append('file', file);
                
                try {
                    const res = await fetch(API_BASE + '/predict/csv', { method: 'POST', body: formData });
                    const data = await res.json();
                    
                    if (res.ok) {
                        displayResult('csvResult', data);
                    } else {
                        document.getElementById('csvResult').innerHTML = '<p class="error">Error: ' + (data.detail || 'Unknown error') + '</p>';
                    }
                } catch (e) {
                    document.getElementById('csvResult').innerHTML = '<p class="error">Error: ' + e.message + '</p>';
                }
            }

            async function sendHRData() {
                const data = document.getElementById('hrData').value.split(',').map(x => parseFloat(x.trim())).filter(x => !isNaN(x));
                if (data.length < 640) { alert('Need at least 640 samples'); return; }
                
                try {
                    const res = await fetch(API_BASE + '/predict/array', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ hr_values: data })
                    });
                    const result = await res.json();
                    
                    if (res.ok) {
                        displayResult('hrResult', result);
                    } else {
                        document.getElementById('hrResult').innerHTML = '<p class="error">Error: ' + (result.detail || 'Unknown error') + '</p>';
                    }
                } catch (e) {
                    document.getElementById('hrResult').innerHTML = '<p class="error">Error: ' + e.message + '</p>';
                }
            }

            async function checkHealth() {
                try {
                    const res = await fetch(API_BASE + '/health');
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
    return html_content

# ... (keep all your other API endpoints exactly as they are)
