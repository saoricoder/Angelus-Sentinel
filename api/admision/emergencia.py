import sys
import os

# Add backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

# Import FastAPI app and specific function
from main import app, admision_emergencia

# Vercel serverless function handler
handler = admision_emergencia
