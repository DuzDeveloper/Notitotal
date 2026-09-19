"""
Scraper para OneFootball
Extrae contenido específico del HTML
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
import re
import time
from utils.text_cleaner import clean_title, clean_description, clean_content

# Headers que simulan navegador real
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Cache-Control': 'max-age=0',
}

def get_article_content_from_page(url):
    """
    Extrae el contenido completo de una noticia de OneFootball
    Buscando específicamente los párrafos <p> del contenido
    """
    try:
        time.sleep(1)  # Delay para no sobrecargar
        
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"Status {response.status_code} en {url}")
            return ""
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remover scripts y styles
        for element in soup(['script', 'style', 'nav', 'footer', 'aside']):
            element.decompose()
        
        # Buscar el contenedor principal de la noticia
        # OneFootball usa diferentes estructuras, intentar varias
        article_container = None
        
        # Estrategia 1: buscar article tag
        article_container = soup.find('article')
        
        # Estrategia 2: buscar div principal
        if not article_container:
            article_container = soup.find('div', class_=re.compile('article|content|body|text', re.I))
        
        # Estrategia 3: buscar main
        if not article_container:
            article_container = soup.find('main')
        
        # Estrategia 4: todo el body
        if not article_container:
            article_container = soup.body
        
        if not article_container:
            return ""
        
        # Extraer TODOS los párrafos de contenido
        content_parts = []
        paragraphs = article_container.find_all('p')
        
        for p in paragraphs:
            text = p.get_text(strip=True)
            
            # Filtrar párrafos muy cortos o ads
            if not text or len(text) < 15:
                continue
            
            # Filtrar párrafos de navegación/ads
            if any(word in text.lower() for word in ['compartir', 'seguir', 'comentarios', 'publicidad', 'anuncio', 'ads']):
                continue
            
            content_parts.append(text)
        
        # Unir todos los párrafos
        content_text = "\n\n".join(content_parts)
        
        if content_text:
            print(f"✓ Contenido extraído: {len(content_text)} caracteres")
        
        return clean_content(content_text) if content_text else ""
        
    except Exception as e:
        print(f"Error extrayendo contenido: {e}")
        return ""

def scrape_onefootball():
    """
    Scrape de OneFootball - lista de noticias
    """
    news_list = []
    
    urls = [
        'https://onefootball.com/es/noticias',
        'https://onefootball.com/es/inicio',
    ]
    
    for main_url in urls:
        try:
            print(f"\n📍 Scrapeando {main_url}")
            
            response = requests.get(main_url, headers=HEADERS, timeout=15)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                print(f"Status {response.status_code}")
                continue
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar todos los links de noticias
            # OneFootball estructura: /es/noticias/titulo-id
            all_links = soup.find_all('a', href=re.compile(r'/es/noticias/.*-\d+'))
            print(f"Encontrados {len(all_links)} links de noticias")
            
            if not all_links:
                # Intenta alternativa
                all_links = soup.find_all('a', href=re.compile(r'/noticias/'))
                print(f"Intento alternativo: {len(all_links)} links")
            
            # Procesar cada noticia
            processed_urls = set()  # Para evitar duplicados
            
            for idx, link in enumerate(all_links[:30]):  # Máximo 30 noticias
                try:
                    article_url = link.get('href', '')
                    
                    if not article_url:
                        continue
                    
                    if not article_url.startswith('http'):
                        article_url = urljoin('https://onefootball.com', article_url)
                    
                    # Evitar duplicados
                    if article_url in processed_urls:
                        continue
                    processed_urls.add(article_url)
                    
                    # Extraer título del link
                    title = clean_title(link.get_text(strip=True))
                    
                    if not title or len(title) < 10:
                        continue
                    
                    print(f"  [{idx}] {title[:60]}...")
                    
                    # Extraer descripción (texto cerca del link)
                    description = ""
                    parent = link.parent
                    if parent:
                        parent_text = parent.get_text(strip=True)
                        if len(parent_text) > len(title):
                            description = clean_description(parent_text[:200])
                    
                    # Buscar imagen
                    image_url = ""
                    img = link.find('img')
                    if not img and parent:
                        img = parent.find('img')
                    
                    if img:
                        image_url = img.get('src', '') or img.get('data-src', '')
                        if image_url and not image_url.startswith('http'):
                            image_url = urljoin('https://onefootball.com', image_url)
                    
                    # Extraer contenido completo
                    full_content = get_article_content_from_page(article_url)
                    
                    if not full_content:
                        full_content = description
                    
                    if not full_content:
                        print(f"    ⚠️ Sin contenido, saltando...")
                        continue
                    
                    news_dict = {
                        'title': title,
                        'description': description,
                        'content': full_content,
                        'image_url': image_url,
                        'source': 'OneFootball',
                        'source_url': article_url,
                        'author': 'OneFootball',
                        'published_at': datetime.now().isoformat()
                    }
                    
                    news_list.append(news_dict)
                    print(f"    ✓ Agregada")
                    
                    # Delay entre requests para no sobrecargar
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"  Error en noticia {idx}: {e}")
                    continue
            
            if news_list:
                break  # Si encontramos noticias, salir del loop
        
        except Exception as e:
            print(f"Error en {main_url}: {e}")
            continue
    
    print(f"\n✓ OneFootball: {len(news_list)} noticias encontradas\n")
    return news_list
