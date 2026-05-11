import sys
import os

# Add backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Import the FastAPI app
from main import app_handler as app

# Vercel serverless function handler
handler = app
