import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import the main FastAPI app
from main import app_handler as app

# Vercel serverless function handler
handler = app
