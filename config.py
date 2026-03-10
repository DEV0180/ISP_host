import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Model Configuration
MODEL_PATH = os.getenv('MODEL_PATH', 'sleep_model.h5')
WINDOW_SIZE = int(os.getenv('WINDOW_SIZE', 640))  # 20 Hz * 32 sec

# API Configuration
API_HOST = os.getenv('API_HOST', '0.0.0.0')
API_PORT = int(os.getenv('API_PORT', 8000))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Server Configuration
WORKERS = int(os.getenv('WORKERS', 4))
TIMEOUT = int(os.getenv('TIMEOUT', 120))

# Model parameters
NUM_CLASSES = 7  # Wake, N1, N2, N3, REM, Movement, Unscored
SLEEP_STAGES = ['Wake', 'N1', 'N2', 'N3', 'REM', 'Movement', 'Unscored']

# Sleep Score Weights
SCORE_WEIGHTS = {
    'duration': 0.35,
    'efficiency': 0.20,
    'deep_sleep': 0.15,
    'rem_sleep': 0.15,
    'hrv': 0.15
}

# Sleep Score Reference Values
SLEEP_DURATION_IDEAL = 8.0  # hours
DEEP_SLEEP_IDEAL = 0.2  # 20%
REM_SLEEP_IDEAL = 0.25  # 25%
HRV_REFERENCE = 65.0  # bpm
