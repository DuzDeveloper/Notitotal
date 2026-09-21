"""
Flask API para Football News App - VERSIÓN SIMPLIFICADA
Solo Goal y Marca
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import os
import sqlite3
from threading import Thread
import time
import os
import shutil

# Importar SOLO Goal y Marca
from scrapers.goal import scrape_goal
from scrapers.marca import scrape_marca

app = Flask(__name__)
CORS(app)

# Configuración
DB_PATH = os.getenv('DATABASE_PATH', '/tmp/news.db')
CACHE_DURATION = 300

# Variables globales de caché
cache = {
    'news': [],
    'sources': ['Todos', 'Goal', 'Marca'],
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
        print(f"✓ Limpieza completada")
    except Exception as e:
        print(f"Error limpiando: {e}")

def scrape_all_sources():
    """Ejecutar SOLO Goal y Marca"""
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
    
    print(f"\n📰 Total: {len(all_news)} noticias")
    
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
            print(f"✓ Guardadas en BD")
        except Exception as e:
            print(f"✗ Error BD: {e}")
    
    clean_old_news()
    
    cache['last_update'] = datetime.now()
    cache['news'] = all_news
    cache['sources'] = ['Todos', 'Goal', 'Marca']
    
    print(f"{'='*50}\n")

init_db()

# ==================== RUTAS ====================

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()}), 200

@app.route('/api/news', methods=['GET'])
def get_news():
    """Obtener noticias"""
    source = request.args.get('source', 'all')
    search = request.args.get('search', '').lower()
    
    # Trigger scraping si es necesario
    if cache['last_update'] is None or (datetime.now() - cache['last_update']).seconds > CACHE_DURATION:
        print("📡 Ejecutando scraping...")
        thread = Thread(target=scrape_all_sources, daemon=True)
        thread.start()
    
    # Obtener noticias
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM news ORDER BY created_at DESC LIMIT 100')
        rows = cursor.fetchall()
        conn.close()
        news = [dict(row) for row in rows]
    except:
        news = []
    
    # Filtrar por fuente
    if source and source != 'all' and source != 'todos':
        news = [n for n in news if n.get('source', '').lower() == source.lower()]
    
    # Filtrar por búsqueda
    if search:
        news = [n for n in news if 
                search in n.get('title', '').lower() or 
                search in n.get('description', '').lower()]
    
    return jsonify({'news': news, 'total': len(news)}), 200

@app.route('/api/sources', methods=['GET'])
def get_sources():
    """Obtener SOLO Goal y Marca"""
    return jsonify({'sources': ['Todos', 'Goal', 'Marca']}), 200

@app.route('/api/refresh', methods=['POST'])
def refresh():
    """Forzar actualización"""
    thread = Thread(target=scrape_all_sources, daemon=True)
    thread.start()
    return jsonify({'status': 'Scraping iniciado...'}), 202

@app.route('/api/stats', methods=['GET'])
def stats():
    """Estadísticas"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM news')
        total = cursor.fetchone()[0]
        cursor.execute('SELECT source, COUNT(*) as count FROM news GROUP BY source')
        sources_stats = dict(cursor.fetchall())
        conn.close()
        return jsonify({'total_news': total, 'sources': sources_stats}), 200
    except:
        return jsonify({'error': 'Error'}), 500

@app.route('/api/reset-db', methods=['POST'])
def reset_db():
    """Resetear la base de datos completamente - SOLO DESARROLLO"""
    try:
        # Eliminar archivo de BD
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
            print("✓ BD eliminada")
        
        # Recrear BD limpia
        init_db()
        print("✓ BD recrea nueva")
        
        # Limpiar variables globales
        cache['news'] = []
        cache['sources'] = ['Todos', 'Goal', 'Marca']
        cache['last_update'] = None
        
        # Ejecutar scraping nuevo
        scrape_all_sources()
        
        return jsonify({'status': 'BD reseteada y scrape completado'}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
        
if __name__ == '__main__':
    scrape_all_sources()
    app.run(host='0.0.0.0', port=5000, debug=False)