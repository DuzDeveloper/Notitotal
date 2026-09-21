"""
Scrapers para Football News App
Solo Goal y Marca
"""

from .goal import scrape_goal
from .marca import scrape_marca

__all__ = ['scrape_goal', 'scrape_marca']