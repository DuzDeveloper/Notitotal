"""
Configuración del backend Flask
"""

import os
from datetime import timedelta

class Config:
    """Configuración base"""
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = FLASK_ENV == 'development'
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'news.db')
    
    # Scraping
    SCRAPE_INTERVAL = 30  # segundos
    CLEANUP_INTERVAL = 3600  # 1 hora
    NEWS_MAX_AGE = timedelta(hours=12)  # Eliminar noticias > 12 horas
    NEWS_PER_SOURCE = 10  # Máximo de noticias por fuente
    
    # Timeouts
    REQUEST_TIMEOUT = 10  # segundos
    SCRAPE_TIMEOUT = 15  # segundos
    
    # CORS
    CORS_ORIGINS = [
        'http://localhost:3000',
        'http://localhost:5000',
        'https://*.vercel.app',
        'https://*.vercel.app/*'
    ]
    
    # Headers para scrapers
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    
    # Caché en memoria
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Configuración para producción (Vercel)"""
    DEBUG = False
    TESTING = False
    
    # Vercel
    DATABASE_PATH = '/tmp/news.db'
    
    # Más conservador con recursos en Vercel
    SCRAPE_INTERVAL = 60  # Cada 1 minuto
    CLEANUP_INTERVAL = 7200  # Cada 2 horas

class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    DATABASE_PATH = ':memory:'  # BD en memoria

# Seleccionar configuración
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Obtener configuración actual"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
