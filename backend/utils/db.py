"""
Database utilities para SQLite
Gestión de noticias con expiración automática
"""

import sqlite3
from datetime import datetime
import json

def init_db(db_path):
    """Inicializar base de datos con tabla de noticias"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            content TEXT,
            image_url TEXT,
            source TEXT NOT NULL,
            source_url TEXT,
            author TEXT,
            published_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            search_text TEXT
        )
    ''')
    
    # Índices para búsqueda rápida
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_created_at ON news(created_at)
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_source ON news(source)
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_search ON news(search_text)
    ''')
    
    conn.commit()
    conn.close()
    print("✓ Base de datos inicializada")

def add_news(db_path, news_dict):
    """
    Agregar una noticia a la BD
    news_dict debe contener: title, description, content, image_url, source, source_url, author, published_at
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Crear texto de búsqueda (title + description)
        search_text = f"{news_dict.get('title', '')} {news_dict.get('description', '')}".lower()
        
        # Verificar si la noticia ya existe (por título + fuente)
        cursor.execute(
            'SELECT id FROM news WHERE title = ? AND source = ?',
            (news_dict.get('title'), news_dict.get('source'))
        )
        
        if cursor.fetchone():
            return  # Ya existe, no agregar
        
        cursor.execute('''
            INSERT INTO news 
            (title, description, content, image_url, source, source_url, author, published_at, search_text)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            news_dict.get('title'),
            news_dict.get('description'),
            news_dict.get('content'),
            news_dict.get('image_url'),
            news_dict.get('source'),
            news_dict.get('source_url'),
            news_dict.get('author'),
            news_dict.get('published_at'),
            search_text
        ))
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error adding news: {e}")
        return False

def get_news(db_path, source='all', search=''):
    """
    Obtener noticias con filtros opcionales
    source: 'all' o nombre de la fuente específica
    search: texto de búsqueda
    """
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = 'SELECT * FROM news WHERE 1=1'
        params = []
        
        # Filtro por fuente
        if source != 'all' and source != 'Todos':
            query += ' AND source = ?'
            params.append(source)
        
        # Filtro por búsqueda
        if search:
            query += ' AND search_text LIKE ?'
            params.append(f'%{search.lower()}%')
        
        # Ordenar por fecha descendente y limitar
        query += ' ORDER BY published_at DESC LIMIT 100'
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        conn.close()
        
        # Convertir a lista de diccionarios
        news_list = [dict(row) for row in rows]
        return news_list
        
    except Exception as e:
        print(f"Error getting news: {e}")
        return []

def delete_old_news(db_path):
    """
    Eliminar noticias más antiguas de 12 horas
    Ejecutarse automáticamente cada hora
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Calcular timestamp de hace 12 horas
        from datetime import datetime, timedelta
        cutoff_time = (datetime.now() - timedelta(hours=12)).isoformat()
        
        cursor.execute(
            'DELETE FROM news WHERE created_at < ?',
            (cutoff_time,)
        )
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        if deleted_count > 0:
            print(f"🗑️  {deleted_count} noticias antiguas eliminadas")
        
        return deleted_count
        
    except Exception as e:
        print(f"Error deleting old news: {e}")
        return 0

def get_stats(db_path):
    """Obtener estadísticas de la BD"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM news')
        total = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT source, COUNT(*) as count 
            FROM news 
            GROUP BY source
        ''')
        by_source = dict(cursor.fetchall())
        
        conn.close()
        return {'total': total, 'by_source': by_source}
        
    except Exception as e:
        print(f"Error getting stats: {e}")
        return {}
