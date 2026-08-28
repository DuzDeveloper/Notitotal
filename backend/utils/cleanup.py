"""
Sistema automático de limpieza de noticias
Elimina noticias > 12 horas para evitar acumulación de archivos basura
"""

import sqlite3
from datetime import datetime, timedelta
import os

def cleanup_old_news(db_path, hours=12):
    """
    Elimina noticias más antiguas de X horas
    Por defecto: 12 horas
    """
    try:
        if not os.path.exists(db_path):
            return 0
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Calcular timestamp de hace 12 horas
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        cursor.execute(
            'DELETE FROM news WHERE created_at < ?',
            (cutoff_time.isoformat(),)
        )
        
        deleted_count = cursor.rowcount
        
        # Vacuum para reclamar espacio
        if deleted_count > 0:
            cursor.execute('VACUUM')
        
        conn.commit()
        conn.close()
        
        if deleted_count > 0:
            print(f"🗑️  [{datetime.now()}] {deleted_count} noticias antiguas eliminadas (>12h)")
        
        return deleted_count
        
    except Exception as e:
        print(f"Error en cleanup_old_news: {e}")
        return 0

def cleanup_duplicates(db_path):
    """
    Elimina noticias duplicadas (mismo título + fuente)
    Mantiene la más reciente
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM news WHERE id NOT IN (
                SELECT MAX(id) 
                FROM news 
                GROUP BY title, source
            )
        ''')
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        if deleted_count > 0:
            print(f"✓ {deleted_count} duplicados eliminados")
        
        return deleted_count
        
    except Exception as e:
        print(f"Error eliminando duplicados: {e}")
        return 0

def database_health_check(db_path):
    """Verificar la salud de la base de datos"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Total de noticias
        cursor.execute('SELECT COUNT(*) FROM news')
        total = cursor.fetchone()[0]
        
        # Noticias por fuente
        cursor.execute('''
            SELECT source, COUNT(*) as count 
            FROM news 
            GROUP BY source
            ORDER BY count DESC
        ''')
        by_source = cursor.fetchall()
        
        # Noticia más antigua
        cursor.execute('SELECT MIN(created_at) FROM news')
        oldest = cursor.fetchone()[0]
        
        # Tamaño de la BD
        db_size = os.path.getsize(db_path) / 1024  # KB
        
        conn.close()
        
        report = {
            'total_noticias': total,
            'por_fuente': dict(by_source),
            'noticia_mas_antigua': oldest,
            'tamaño_db_kb': round(db_size, 2),
            'timestamp': datetime.now().isoformat()
        }
        
        return report
        
    except Exception as e:
        print(f"Error en health_check: {e}")
        return {}

def export_news_json(db_path, output_file='news_export.json'):
    """Exportar noticias a JSON (para backup)"""
    try:
        import json
        
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM news ORDER BY created_at DESC')
        rows = cursor.fetchall()
        
        news_list = [dict(row) for row in rows]
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(news_list, f, indent=2, ensure_ascii=False)
        
        conn.close()
        print(f"✓ {len(news_list)} noticias exportadas a {output_file}")
        return True
        
    except Exception as e:
        print(f"Error exportando noticias: {e}")
        return False
