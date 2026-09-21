"""
Flask API para Football News App
Scraping en tiempo real sin dependencia de scheduler
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import os
import sqlite3
from threading import Thread
import time

# Importar scrapers
from scrapers.goal import scrape_goal
from scrapers.marca import scrape_marca
from scrapers.onefootball import scrape_onefootball
from scrapers.instagram_romano import scrape_instagram

app = Flask(__name__)
CORS(app)

# Configuración
DB_PATH = os.getenv('DATABASE_PATH', '/tmp/news.db')
CACHE_DURATION = 300  # 5 minutos

# Variables globales de caché
cache = {
    'news': [],
    'sources': [],
    'last_update': None
}

def init_db():
    """Inicializar base de datos"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            content TEXT,
            image_url TEXT,
            source TEXT NOT NULL,
            source_url TEXT,
            author TEXT,
            published_at TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def clean_old_news():
    """Limpiar noticias mayores a 12 horas"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cutoff_time = (datetime.now() - timedelta(hours=12)).isoformat()
        cursor.execute('DELETE FROM news WHERE created_at < ?', (cutoff_time,))
        conn.commit()
        conn.close()
        print(f"✓ Limpieza completada a las {datetime.now().isoformat()}")
    except Exception as e:
        print(f"Error limpiando noticias: {e}")

def scrape_all_sources():
    """Ejecutar todos los scrapers"""
    print(f"\n{'='*50}")
    print(f"🔄 Iniciando scrape a las {datetime.now().isoformat()}")
    print(f"{'='*50}")
    
    all_news = []
    
    # Scrape Goal
    try:
        print("Scrapeando Goal...")
        goal_news = scrape_goal()
        all_news.extend(goal_news)
        print(f"✓ Goal: {len(goal_news)} noticias")
    except Exception as e:
        print(f"✗ Error Goal: {e}")
    
    # Scrape Marca
    try:
        print("Scrapeando Marca...")
        marca_news = scrape_marca()
        all_news.extend(marca_news)
        print(f"✓ Marca: {len(marca_news)} noticias")
    except Exception as e:
        print(f"✗ Error Marca: {e}")
    
    print(f"\n📰 Total noticias extraídas: {len(all_news)}")
    
    # Guardar en BD
    if all_news:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            for news in all_news:
                cursor.execute('''
                    INSERT INTO news (title, description, content, image_url, source, source_url, author, published_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    news.get('title', ''),
                    news.get('description', ''),
                    news.get('content', ''),
                    news.get('image_url', ''),
                    news.get('source', ''),
                    news.get('source_url', ''),
                    news.get('author', ''),
                    news.get('published_at', '')
                ))
            
            conn.commit()
            conn.close()
            print(f"✓ Noticias guardadas en BD")
        except Exception as e:
            print(f"✗ Error guardando en BD: {e}")
    
    # Limpiar noticias antiguas
    clean_old_news()
    
    # Actualizar caché
    cache['last_update'] = datetime.now()
    cache['news'] = all_news
    cache['sources'] = list(set([n.get('source', '') for n in all_news if n.get('source')]))
    
    print(f"{'='*50}\n")

def get_news_from_cache_or_db():
    """Obtener noticias del caché o BD"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Obtener últimas 50 noticias
        cursor.execute('''
            SELECT * FROM news 
            ORDER BY created_at DESC 
            LIMIT 50
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        news = []
        for row in rows:
            news.append(dict(row))
        
        return news
    except Exception as e:
        print(f"Error leyendo BD: {e}")
        return []

# Inicializar BD
init_db()

# ==================== RUTAS ====================

@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()}), 200

@app.route('/api/news', methods=['GET'])
def get_news():
    """Obtener noticias con filtros opcionales"""
    source = request.args.get('source', 'all')
    search = request.args.get('search', '').lower()
    
    # Trigger scraping si es necesario (cada 5 minutos)
    if cache['last_update'] is None or (datetime.now() - cache['last_update']).seconds > CACHE_DURATION:
        print("📡 Cache expirado, ejecutando scraping...")
        # Ejecutar en background para no bloquear
        thread = Thread(target=scrape_all_sources, daemon=True)
        thread.start()
    
    # Obtener noticias
    news = get_news_from_cache_or_db()
    
    # Filtrar por fuente
    if source and source != 'all':
        news = [n for n in news if n.get('source', '').lower() == source.lower()]
    
    # Filtrar por búsqueda
    if search:
        news = [n for n in news if 
                search in n.get('title', '').lower() or 
                search in n.get('description', '').lower()]
    
    print(f"API /news - Source: {source}, Search: {search}, Total: {len(news)}")
    
    return jsonify({
        'news': news,
        'total': len(news),
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/sources', methods=['GET'])
def get_sources():
    """Obtener lista de fuentes disponibles"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT source FROM news ORDER BY source')
        sources = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        # Agregar "Todos" al inicio
        if sources and 'Todos' not in sources:
            sources = ['Todos'] + sources
        
        return jsonify({'sources': sources}), 200
    except Exception as e:
        return jsonify({'sources': ['Todos', 'Goal', 'Marca', 'OneFootball', 'Instagram (Fabrizio)'], 'error': str(e)}), 200

@app.route('/api/refresh', methods=['POST'])
def refresh():
    """Forzar actualización de noticias"""
    print("📡 Refresh forzado solicitado")
    thread = Thread(target=scrape_all_sources, daemon=True)
    thread.start()
    return jsonify({'status': 'Scraping iniciado...'}), 202

@app.route('/api/stats', methods=['GET'])
def stats():
    """Estadísticas de la aplicación"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM news')
        total = cursor.fetchone()[0]
        
        cursor.execute('SELECT source, COUNT(*) as count FROM news GROUP BY source')
        sources_stats = dict(cursor.fetchall())
        
        conn.close()
        
        return jsonify({
            'total_news': total,
            'sources': sources_stats,
            'last_update': cache['last_update'].isoformat() if cache['last_update'] else None
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cleanup', methods=['POST'])
def cleanup():
    """Limpiar noticias antiguas"""
    clean_old_news()
    return jsonify({'status': 'Limpieza completada'}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint no encontrado'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500

# Ejecutar scraping inicial al iniciar
if __name__ == '__main__':
    print("🚀 Iniciando Football News API...")
    scrape_all_sources()
    app.run(host='0.0.0.0', port=5000, debug=False)
