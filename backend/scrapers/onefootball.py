"""
Scraper para OneFootball
https://onefootball.com/es/inicio
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
import re

def get_article_content(url, timeout=10):
    """Extrae contenido de artículo"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            return ""
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for element in soup(['script', 'style', 'nav', 'footer']):
            element.decompose()
        
        article = soup.find('article')
        if not article:
            article = soup.find('main')
        if not article:
            article = soup.body
        
        if not article:
            return ""
        
        content_text = ""
        paragraphs = article.find_all('p')
        
        for p in paragraphs:
            text = p.get_text(strip=True)
            if text and len(text) > 20:
                content_text += text + "\n\n"
        
        content_text = re.sub(r'\n\n+', '\n\n', content_text)
        return content_text if content_text else ""
        
    except Exception as e:
        print(f"Error extrayendo contenido OneFootball: {e}")
        return ""

def scrape_onefootball():
    """Scrape de OneFootball - últimas noticias de fútbol"""
    news_list = []
    
    try:
        # Intentar múltiples URLs de OneFootball
        urls = [
            'https://onefootball.com/es/inicio',
            'https://onefootball.com/es',
            'https://onefootball.com/es/noticias',
        ]
        
        for url in urls:
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                response = requests.get(url, headers=headers, timeout=10)
                response.encoding = 'utf-8'
                
                if response.status_code != 200:
                    continue
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # OneFootball usa diferentes selectores, intentar varios
                selectors = [
                    ('article', {}),
                    ('div', {'class': re.compile('article|news|card|item', re.I)}),
                    ('div', {'class': re.compile('Story', re.I)}),
                    ('a', {'class': re.compile('article|news', re.I)}),
                ]
                
                articles = []
                for tag, attrs in selectors:
                    articles = soup.find_all(tag, attrs, limit=10)
                    if articles:
                        break
                
                if not articles:
                    articles = soup.find_all(['article', 'div'], limit=15)
                
                for article in articles:
                    try:
                        # Extraer título - intentar múltiples selectores
                        title = ""
                        title_elem = article.find(['h1', 'h2', 'h3', 'h4', 'span', 'a'])
                        
                        if title_elem:
                            title = title_elem.get_text(strip=True)
                        
                        if not title or len(title) < 10:
                            continue
                        
                        # Extraer URL
                        link = ""
                        link_elem = article.find('a', href=True)
                        if link_elem:
                            link = link_elem.get('href', '')
                        
                        if link and not link.startswith('http'):
                            link = urljoin('https://onefootball.com', link)
                        
                        # Extraer descripción
                        description = ""
                        desc_elem = article.find('p')
                        if desc_elem:
                            description = desc_elem.get_text(strip=True)
                        
                        # Extraer imagen
                        image_url = ""
                        img_elem = article.find('img')
                        if img_elem:
                            image_url = img_elem.get('src', '') or img_elem.get('data-src', '')
                            if image_url and not image_url.startswith('http'):
                                image_url = urljoin('https://onefootball.com', image_url)
                        
                        # Extraer fecha
                        published_at = datetime.now().isoformat()
                        time_elem = article.find(['time', 'span'], class_=re.compile('time|date|fecha', re.I))
                        if time_elem:
                            published_at = time_elem.get_text(strip=True)
                        
                        # Extraer contenido completo
                        full_content = ""
                        if link:
                            full_content = get_article_content(link)
                        
                        if not full_content:
                            full_content = description
                        
                        if not title or not link:
                            continue
                        
                        news_dict = {
                            'title': title,
                            'description': description,
                            'content': full_content,
                            'image_url': image_url,
                            'source': 'OneFootball',
                            'source_url': link,
                            'author': 'OneFootball',
                            'published_at': published_at
                        }
                        
                        news_list.append(news_dict)
                        
                    except Exception as e:
                        continue
                
                if news_list:
                    print(f"OneFootball: {len(news_list)} noticias encontradas")
                    return news_list
                    
            except Exception as e:
                print(f"Error en URL {url}: {e}")
                continue
        
        print(f"OneFootball: No se encontraron noticias")
        return news_list
        
    except Exception as e:
        print(f"Error scraping OneFootball: {e}")
        return news_list
