"""
Football News App - Backend Flask
Scraping de noticias con limpieza automática cada 12 horas
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import sqlite3
import os
import json

# Importar scrapers
from scrapers.onefootball import scrape_onefootball
from scrapers.marca import scrape_marca
from scrapers.goal import scrape_goal
from scrapers.instagram_romano import scrape_instagram_romano
from utils.db import init_db, get_news, add_news, delete_old_news
from utils.cleanup import cleanup_old_news

# Configuración Flask
app = Flask(__name__)
CORS(app)

# Configuración
DATABASE = os.getenv('DATABASE_PATH', 'news.db')
SCRAPE_INTERVAL = 30  # Segundos entre scrapes
CLEANUP_INTERVAL = 3600  # 1 hora

# Inicializar base de datos
init_db(DATABASE)

# Scheduler para renovar noticias automáticamente
scheduler = BackgroundScheduler()

def scrape_all_sources():
    """Scrape de todas las fuentes de noticias"""
    try:
        print(f"[{datetime.now()}] Iniciando scrape de todas las fuentes...")
        
        sources = {
            'OneFootball': scrape_onefootball,
            'Marca': scrape_marca,
            'Goal': scrape_goal,
            'Instagram (Fabrizio)': scrape_instagram_romano
        }
        
        for source_name, scraper_func in sources.items():
            try:
                news_list = scraper_func()
                for news in news_list[:10]:  # Solo últimas 10
                    add_news(DATABASE, news)
                print(f"✓ {source_name}: {len(news_list)} noticias agregadas")
            except Exception as e:
                print(f"✗ Error scraping {source_name}: {e}")
        
        # Limpiar noticias > 12 horas
        cleanup_old_news(DATABASE)
        print("✓ Limpieza completada")
        
    except Exception as e:
        print(f"Error en scrape_all_sources: {e}")

# Eventos de scheduler
@app.before_request
def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(scrape_all_sources, 'interval', seconds=SCRAPE_INTERVAL, id='scrape_job')
        scheduler.add_job(lambda: cleanup_old_news(DATABASE), 'interval', seconds=CLEANUP_INTERVAL, id='cleanup_job')
        scheduler.start()
        print("✓ Scheduler iniciado")

# ======================== API ENDPOINTS ========================

@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

@app.route('/api/news', methods=['GET'])
def get_all_news():
    """Obtener todas las noticias (con filtro opcional)"""
    source = request.args.get('source', 'all')  # 'all', 'OneFootball', 'Marca', 'Goal', 'Instagram'
    search = request.args.get('search', '')
    
    try:
        news_list = get_news(DATABASE, source=source, search=search)
        return jsonify({
            'status': 'success',
            'count': len(news_list),
            'news': news_list
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/sources', methods=['GET'])
def get_sources():
    """Obtener lista de fuentes disponibles"""
    return jsonify({
        'status': 'success',
        'sources': [
            'Todos',
            'OneFootball',
            'Marca',
            'Goal',
            'Instagram (Fabrizio)'
        ]
    })

@app.route('/api/refresh', methods=['POST'])
def refresh_news():
    """Forzar refresh de noticias"""
    try:
        scrape_all_sources()
        return jsonify({
            'status': 'success',
            'message': 'Noticias refrescadas exitosamente'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Obtener estadísticas de noticias"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM news")
        total = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT source, COUNT(*) as count 
            FROM news 
            GROUP BY source
        """)
        by_source = dict(cursor.fetchall())
        
        cursor.execute("""
            SELECT MIN(created_at) as oldest, MAX(created_at) as newest
            FROM news
        """)
        dates = cursor.fetchone()
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'total_news': total,
            'by_source': by_source,
            'oldest': dates[0],
            'newest': dates[1]
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/cleanup', methods=['POST'])
def manual_cleanup():
    """Limpiar manualmente noticias > 12 horas"""
    try:
        cleanup_old_news(DATABASE)
        return jsonify({
            'status': 'success',
            'message': 'Limpieza completada'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'status': 'error', 'message': 'Endpoint no encontrado'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'status': 'error', 'message': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    # Primer scrape al iniciar
    scrape_all_sources()
    
    # Modo de ejecución
    debug_mode = os.getenv('FLASK_ENV', 'production') == 'development'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
