import json
import urllib.request
import numpy as np

try:
    # Generate 650 samples (meets minimum 640 requirement)
    hr_values = list(np.random.normal(70, 5, 650).astype(float))
    data = json.dumps({'hr_values': hr_values})
    req = urllib.request.Request(
        'http://localhost:8000/predict/array', 
        data=data.encode('utf-8'), 
        headers={'Content-Type': 'application/json'}
    )
    r = urllib.request.urlopen(req)
    response = r.read().decode()
    print("Status: 200 OK")
    print("Response:")
    result = json.loads(response)
    print(f"  Final Sleep Score: {result['sleep_quality']['final_score']}%")
    print(f"  Quality Level: {result['sleep_quality']['quality_level']}")
except urllib.error.HTTPError as e:
    response = e.read().decode()
    print(f"HTTP Error {e.code}")
    print(f"Response: {response}")
except Exception as e:
    print(f"Error: {type(e).__name__}: {str(e)}")
