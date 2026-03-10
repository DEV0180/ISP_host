"""
Test script for Sleep Quality Analysis API
Run this after starting the server to verify it's working correctly
"""

import requests
import numpy as np
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def test_health_check() -> Dict[str, Any]:
    """Test the health check endpoint"""
    print("\n" + "="*60)
    print("TEST 1: Health Check")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        response.raise_for_status()
        result = response.json()
        print(f"✓ Status: {result['status']}")
        print(f"✓ Model Loaded: {result['model_loaded']}")
        print(f"✓ Number of Classes: {result['num_classes']}")
        return result
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


def test_api_info() -> None:
    """Test the root endpoint"""
    print("\n" + "="*60)
    print("TEST 2: API Information")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/")
        response.raise_for_status()
        result = response.json()
        print(f"✓ API Name: {result['message']}")
        print(f"✓ Version: {result['version']}")
        print("✓ Available Endpoints:")
        for endpoint, path in result['endpoints'].items():
            print(f"  - {endpoint}: {path}")
    except Exception as e:
        print(f"✗ Error: {e}")


def test_predict_array() -> None:
    """Test prediction with JSON array"""
    print("\n" + "="*60)
    print("TEST 3: Prediction with JSON Array")
    print("="*60)
    
    try:
        # Generate sample HR data (20Hz for 5 minutes = 6000 samples)
        # We'll create 10 windows of 640 samples each
        hr_values = list(np.random.normal(70, 5, 6400).astype(float))
        
        print(f"Sending {len(hr_values)} HR samples...")
        
        response = requests.post(
            f"{BASE_URL}/predict/array",
            json={"hr_values": hr_values},
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        
        print(f"✓ Total Windows: {result['total_windows']}")
        print(f"✓ Duration: {result['total_duration']['hours']:.2f} hours")
        print(f"✓ Final Score: {result['sleep_quality']['final_score']:.1f}%")
        print(f"✓ Quality Level: {result['sleep_quality']['quality_level']}")
        
        print("\nSleep Score Breakdown:")
        for score_name, score_value in result['sleep_scores'].items():
            print(f"  - {score_name}: {score_value:.1f}%")
        
        print("\nFirst 3 Predictions:")
        for pred in result['predictions'][:3]:
            print(f"  Window {pred['window']}: {pred['stage']} ({pred['confidence']:.1f}%)")
        
    except Exception as e:
        print(f"✗ Error: {e}")


def test_predict_csv() -> None:
    """Test prediction with CSV file"""
    print("\n" + "="*60)
    print("TEST 4: Prediction with CSV File")
    print("="*60)
    
    try:
        # Create sample CSV in memory
        import io
        import csv
        
        # Generate sample HR data
        hr_values = list(np.random.normal(70, 5, 6400).astype(int))
        
        # Create CSV content
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(['HR'])
        for hr in hr_values:
            writer.writerow([hr])
        
        csv_content = csv_buffer.getvalue()
        
        print(f"Sending CSV with {len(hr_values)} HR samples...")
        
        # Send as multipart form data
        files = {'file': ('test_data.csv', csv_content, 'text/csv')}
        response = requests.post(
            f"{BASE_URL}/predict/csv",
            files=files,
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        
        print(f"✓ Total Windows: {result['total_windows']}")
        print(f"✓ Duration: {result['total_duration']['hours']:.2f} hours")
        print(f"✓ Final Score: {result['sleep_quality']['final_score']:.1f}%")
        print(f"✓ Quality Level: {result['sleep_quality']['quality_level']}")
        
    except Exception as e:
        print(f"✗ Error: {e}")


def test_example_endpoint() -> None:
    """Test the example requests endpoint"""
    print("\n" + "="*60)
    print("TEST 5: Example Requests Format")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/predict/example")
        response.raise_for_status()
        result = response.json()
        
        print("✓ CSV Endpoint:")
        print(f"  Path: {result['csv_endpoint']['path']}")
        print(f"  Method: {result['csv_endpoint']['method']}")
        
        print("\n✓ Array Endpoint:")
        print(f"  Path: {result['array_endpoint']['path']}")
        print(f"  Method: {result['array_endpoint']['method']}")
        print(f"  Example: {json.dumps(result['array_endpoint']['example_json'], indent=2)}")
        
    except Exception as e:
        print(f"✗ Error: {e}")


def test_edge_cases() -> None:
    """Test edge cases and error handling"""
    print("\n" + "="*60)
    print("TEST 6: Error Handling")
    print("="*60)
    
    # Test with insufficient data
    print("\n1. Testing with insufficient data (< 640 samples)...")
    try:
        response = requests.post(
            f"{BASE_URL}/predict/array",
            json={"hr_values": [60, 61, 62]},
            timeout=10
        )
        if response.status_code != 200:
            print(f"✓ Correctly rejected: {response.json()['detail']}")
        else:
            print("✗ Should have rejected insufficient data")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test with missing required field
    print("\n2. Testing with missing 'hr_values' field...")
    try:
        response = requests.post(
            f"{BASE_URL}/predict/array",
            json={"data": [60, 61, 62]},
            timeout=10
        )
        if response.status_code != 200:
            print(f"✓ Correctly rejected: {response.json()['detail']}")
        else:
            print("✗ Should have rejected missing field")
    except Exception as e:
        print(f"✗ Error: {e}")


def run_all_tests() -> None:
    """Run all tests"""
    print("\n" + "🏥 "*30)
    print("SLEEP QUALITY ANALYSIS API - TEST SUITE")
    print("🏥 "*30)
    
    try:
        health = test_health_check()
        if health and health['model_loaded']:
            test_api_info()
            test_example_endpoint()
            test_edge_cases()
            test_predict_array()
            test_predict_csv()
            
            print("\n" + "="*60)
            print("✓ ALL TESTS COMPLETED SUCCESSFULLY")
            print("="*60)
        else:
            print("\n✗ Model is not loaded properly. Cannot run prediction tests.")
            print("Please ensure sleep_model.h5 is in the correct location.")
    
    except requests.exceptions.ConnectionError:
        print("\n" + "="*60)
        print("✗ CONNECTION ERROR")
        print("="*60)
        print(f"Cannot connect to {BASE_URL}")
        print("Make sure the server is running:")
        print("  python main.py")
        print("or")
        print("  uvicorn main:app --reload")


if __name__ == "__main__":
    run_all_tests()
