"""
Utilidades para el backend
"""

from .db import init_db, add_news, get_news, delete_old_news, get_stats
from .cleanup import cleanup_old_news, cleanup_duplicates, database_health_check

__all__ = [
    'init_db',
    'add_news',
    'get_news',
    'delete_old_news',
    'get_stats',
    'cleanup_old_news',
    'cleanup_duplicates',
    'database_health_check'
]
