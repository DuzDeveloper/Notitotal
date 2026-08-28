import sys
import os
sys.path.insert(0, './backend')

from backend.app import app

# Para Vercel Serverless Function
def handler(request):
    return app(request)
