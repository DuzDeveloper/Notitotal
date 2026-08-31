"""
Scraper para OneFootball
https://onefootball.com/es/inicio
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
import re

def scrape_onefootball():
    """
    Scrape de OneFootball - últimas noticias de fútbol
    Retorna lista de diccionarios con noticias
    """
    news_list = []
    
    try:
        url = 'https://onefootball.com/es/inicio'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"Error: Status {response.status_code} en OneFootball")
            return news_list
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Buscar artículos (estructura específica de OneFootball)
        articles = soup.find_all('article', limit=10)
        
        if not articles:
            # Alternativa: buscar divs con clase news
            articles = soup.find_all('div', class_=re.compile('news|article'), limit=10)
        
        for article in articles:
            try:
                # Extraer título
                title_elem = article.find(['h2', 'h3', 'a'])
                if not title_elem:
                    continue
                title = title_elem.get_text(strip=True)
                
                if not title or len(title) < 10:
                    continue
                
                # Extraer URL
                link_elem = article.find('a', href=True)
                link = link_elem.get('href', '') if link_elem else ''
                if link:
                    link = urljoin(url, link)
                
                # Extraer descripción
                desc_elem = article.find('p')
                description = desc_elem.get_text(strip=True) if desc_elem else ""
                
                # Extraer imagen
                img_elem = article.find('img')
                image_url = img_elem.get('src', '') if img_elem else ""
                if image_url:
                    image_url = urljoin(url, image_url)
                
                # Extraer tiempo publicado
                time_elem = article.find(['time', 'span'], class_=re.compile('time|published'))
                published_at = time_elem.get_text(strip=True) if time_elem else datetime.now().isoformat()
                
                news_dict = {
                    'title': title,
                    'description': description,
                    'content': description,  # OneFootball no tiene contenido en lista
                    'image_url': image_url,
                    'source': 'OneFootball',
                    'source_url': link,
                    'author': 'OneFootball',
                    'published_at': published_at
                }
                
                news_list.append(news_dict)
                
            except Exception as e:
                print(f"Error procesando artículo OneFootball: {e}")
                continue
        
        print(f"✓ OneFootball: {len(news_list)} noticias encontradas")
        return news_list
        
    except requests.exceptions.RequestException as e:
        print(f"Error conectando a OneFootball: {e}")
        return news_list
    except Exception as e:
        print(f"Error scraping OneFootball: {e}")
        return news_list

from utils.content_extractor import get_article_content

# En cada scraper, agregar:
full_content = get_article_content(link) if link else ""
if not full_content:
    full_content = description

# Y en news_dict:
'content': full_content,  # ← CONTENIDO COMPLETO
