"""
Scraper para OneFootball
https://onefootball.com/es/inicio

NOTA: OneFootball tiene protección anti-bot. Este scraper usa estrategias
para evitar ser detectado como bot.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
import re
import time
from utils.text_cleaner import clean_title, clean_description, clean_content

# Simuladores de navegador real
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
    'Referer': 'https://www.google.com/',
    'DNT': '1'
}

def get_article_content(url, timeout=10):
    """Extrae contenido de artículo de OneFootball"""
    try:
        time.sleep(1)  # Delay para no ser detectado como bot
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            return ""
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remover elementos no deseados
        for element in soup(['script', 'style', 'nav', 'footer', 'aside']):
            element.decompose()
        
        # Buscar contenido
        article = soup.find('article')
        if not article:
            article = soup.find('div', class_=re.compile('content|body|text', re.I))
        if not article:
            article = soup.body
        
        if not article:
            return ""
        
        # Extraer párrafos
        content_text = ""
        paragraphs = article.find_all('p')
        
        for p in paragraphs:
            text = p.get_text(strip=True)
            if text and len(text) > 20:
                content_text += text + "\n\n"
        
        content_text = re.sub(r'\n\n+', '\n\n', content_text)
        return clean_content(content_text) if content_text else ""
        
    except Exception as e:
        print(f"Error extrayendo contenido OneFootball: {e}")
        return ""

def scrape_onefootball():
    """
    Scrape de OneFootball - noticias de fútbol
    
    NOTA: OneFootball tiene protección anti-bot. Si esto no funciona,
    es porque han endurecido su protección. En ese caso, recomendamos:
    - Usar Selenium/Playwright (requiere navegador)
    - Usar API de terceros
    - Remover OneFootball como fuente
    """
    news_list = []
    
    urls_to_try = [
        'https://onefootball.com/es/inicio',
        'https://onefootball.com/es/noticias',
        'https://onefootball.com/es',
    ]
    
    for url in urls_to_try:
        try:
            print(f"Intentando scrape de OneFootball: {url}")
            
            # Esperar para no ser detectado como bot
            time.sleep(2)
            
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                print(f"Status {response.status_code} en {url}")
                continue
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Estrategia 1: Buscar article tags
            articles = soup.find_all('article', limit=20)
            print(f"OneFootball - Encontrados {len(articles)} articles tags en {url}")
            
            # Estrategia 2: Buscar divs con clase article/news/story
            if not articles or len(articles) < 3:
                articles = soup.find_all('div', class_=re.compile(
                    'article|news|story|item|card|post', re.I
                ), limit=20)
                print(f"OneFootball - Encontrados {len(articles)} divs con clase")
            
            # Estrategia 3: Buscar links a noticias
            if not articles or len(articles) < 3:
                links = soup.find_all('a', href=re.compile(
                    '/es/noticias|/news|/noticia', re.I
                ), limit=20)
                articles = [link.parent for link in links if link.parent]
                print(f"OneFootball - Encontrados {len(articles)} parents de links")
            
            # Procesar artículos encontrados
            for idx, article in enumerate(articles):
                try:
                    # Extraer título
                    title = ""
                    for tag in ['h2', 'h3', 'h4', 'a', 'span']:
                        title_elem = article.find(tag)
                        if title_elem:
                            title = clean_title(title_elem.get_text(strip=True))
                            if title and len(title) > 10:
                                break
                    
                    if not title or len(title) < 10:
                        continue
                    
                    # Extraer URL
                    link = ""
                    link_elem = article.find('a', href=True)
                    if link_elem:
                        link = link_elem.get('href', '')
                    
                    if link and not link.startswith('http'):
                        link = urljoin(url, link)
                    
                    if not link:
                        continue
                    
                    # Extraer descripción
                    description = ""
                    desc_elem = article.find('p')
                    if desc_elem:
                        description = clean_description(desc_elem.get_text(strip=True))
                    
                    # Extraer imagen
                    image_url = ""
                    img_elem = article.find('img')
                    if img_elem:
                        image_url = img_elem.get('src', '') or img_elem.get('data-src', '')
                        if image_url and not image_url.startswith('http'):
                            image_url = urljoin('https://onefootball.com', image_url)
                    
                    # Extraer contenido completo
                    full_content = get_article_content(link)
                    if not full_content:
                        full_content = description
                    
                    news_dict = {
                        'title': title,
                        'description': description,
                        'content': full_content,
                        'image_url': image_url,
                        'source': 'OneFootball',
                        'source_url': link,
                        'author': 'OneFootball',
                        'published_at': datetime.now().isoformat()
                    }
                    
                    news_list.append(news_dict)
                    print(f"OneFootball - Artículo {idx}: {title[:50]}...")
                    
                except Exception as e:
                    print(f"OneFootball - Error en artículo {idx}: {e}")
                    continue
            
            # Si encontramos noticias, salir del loop de URLs
            if news_list:
                break
                
        except Exception as e:
            print(f"OneFootball - Error scrapeando {url}: {e}")
            continue
    
    print(f"✓ OneFootball: {len(news_list)} noticias encontradas")
    return news_list
