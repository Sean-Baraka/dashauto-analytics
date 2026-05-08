"""
Configuration File for DashAuto Analytics
========================================
Postgraduate Diploma Project
"DATA APPLICATION FOR AUTOMATED DATA ANALYTICS AND VISUALIZATION USING DASHAPP"
"""

import os
from pathlib import Path

# Base Directory
BASE_DIR = Path(__file__).parent.absolute()

# ==================== APPLICATION SETTINGS ====================

APP_TITLE = "DashAuto Analytics"
APP_DESCRIPTION = "Automated Data Analytics and Visualization Platform"
VERSION = "1.0.0"
AUTHOR = "Your Full Name"
YEAR = "2026"

# Dash Configuration
DEBUG = True
PORT = 8050
HOST = "0.0.0.0"          # Use "127.0.0.1" for local only

# Theme Settings
DEFAULT_THEME = "CYBORG"   # Options: CYBORG, DARKLY, BOOTSTRAP, SUPERHERO, etc.
SUPPORTED_THEMES = ["CYBORG", "DARKLY", "BOOTSTRAP", "SUPERHERO", "FLATLY"]

# Data Processing Settings
MAX_ROWS_FOR_FULL_ANALYSIS = 100_000
MAX_ROWS_FOR_PLOTTING = 10_000      # Sampling threshold for visualizations
SAMPLING_RANDOM_STATE = 42

# File Upload Settings
ALLOWED_EXTENSIONS = ['.csv', '.xlsx', '.xls']
MAX_UPLOAD_SIZE_MB = 50

# Performance Settings
ENABLE_SAMPLING = True
CACHE_TIMEOUT = 300  # seconds (for future caching implementation)

# Security Settings
SECRET_KEY = os.environ.get('DASH_SECRET_KEY', 'dashauto-analytics-secret-2026')
ENFORCE_HTTPS = False

# Export Settings
EXPORT_FORMATS = ['png', 'jpeg', 'svg', 'pdf', 'csv', 'html']

# Paths
UPLOAD_FOLDER = BASE_DIR / "uploads"
STATIC_FOLDER = BASE_DIR / "assets"
LOG_FOLDER = BASE_DIR / "logs"

# Create necessary directories
for folder in [UPLOAD_FOLDER, STATIC_FOLDER, LOG_FOLDER]:
    folder.mkdir(exist_ok=True)

# ==================== PLOTLY CONFIG ====================

PLOTLY_TEMPLATE = "plotly_dark"
PLOTLY_HEIGHT = 680
PLOTLY_COLORSCALE = "RdBu_r"

# ==================== EDA SETTINGS ====================

DEFAULT_OUTLIER_THRESHOLD = 3.0  # Z-score threshold
MISSING_VALUE_THRESHOLD = 30.0   # Percentage to flag column as high missing

# ==================== DEVELOPMENT / PRODUCTION ====================

ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')  # 'development' or 'production'

if ENVIRONMENT == 'production':
    DEBUG = False
    ENFORCE_HTTPS = True

# ==================== HELPER FUNCTIONS ====================

def get_allowed_extensions():
    """Return list of allowed file extensions"""
    return ALLOWED_EXTENSIONS

def allowed_file(filename):
    """Check if file has allowed extension"""
    if not filename:
        return False
    return any(filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS)

def get_max_upload_size():
    """Return max upload size in bytes"""
    return MAX_UPLOAD_SIZE_MB * 1024 * 1024


# ==================== INFO ====================

print(f"✅ {APP_TITLE} v{VERSION} Configuration Loaded Successfully!")
print(f"   Environment: {ENVIRONMENT.upper()}")
print(f"   Debug Mode: {DEBUG}")
