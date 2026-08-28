# api/index.py
import sys
sys.path.insert(0, './backend')

from backend.app import app

# Para Vercel
handler = app
