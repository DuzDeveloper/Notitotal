"""
Scrapers para diferentes fuentes de noticias de fútbol
"""

from .onefootball import scrape_onefootball
from .marca import scrape_marca
from .goal import scrape_goal
from .instagram_romano import scrape_instagram_romano

__all__ = [
    'scrape_onefootball',
    'scrape_marca',
    'scrape_goal',
    'scrape_instagram_romano'
]
