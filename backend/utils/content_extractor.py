"""
Extrae contenido completo de artículos
"""

import requests
from bs4 import BeautifulSoup
import re

def get_article_content(url, timeout=10):
    """
    Obtiene el contenido completo de un artículo
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=timeout)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            return ""
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remover elementos no deseados
        for element in soup(['script', 'style', 'nav', 'footer', 'aside', 'iframe']):
            element.decompose()
        
        # Buscar artículo (diferentes selectores según sitio)
        article = None
        article_selectors = [
            'article',
            '[role="main"]',
            '.article-content',
            '.post-content',
            '.content',
            '.story-body',
            'main'
        ]
        
        for selector in article_selectors:
            article = soup.select_one(selector)
            if article:
                break
        
        if not article:
            article = soup.body if soup.body else soup
        
        # Extraer texto
        text = article.get_text(separator='\n', strip=True)
        
        # Limpiar
        text = re.sub(r'\n\s*\n', '\n', text)
        text = re.sub(r' +', ' ', text)
        text = '\n'.join([line.strip() for line in text.split('\n') if line.strip()])
        
        # Limitar a 2000 caracteres (ajustable)
        return text[:2000]
        
    except Exception as e:
        print(f"Error extrayendo contenido: {e}")
        return ""
