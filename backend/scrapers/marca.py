"""
Scraper para Marca
https://www.marca.com/futbol.html
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
import re

def scrape_marca():
    """
    Scrape de Marca - noticias de fútbol
    """
    news_list = []
    
    try:
        url = 'https://www.marca.com/futbol.html'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"Error: Status {response.status_code} en Marca")
            return news_list
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Buscar noticias en Marca (estructura: artículos con clase ue-c)
        articles = soup.find_all(['article', 'div'], class_=re.compile('ue-c|ue-w|article'), limit=10)
        
        for article in articles:
            try:
                # Título
                title_elem = article.find(['h2', 'h3', 'span'], class_=re.compile('title|ue-t'))
                if not title_elem:
                    title_elem = article.find(['a'])
                
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                
                if not title or len(title) < 10:
                    continue
                
                # URL
                link_elem = article.find('a', href=True)
                link = link_elem.get('href', '') if link_elem else ''
                if link and not link.startswith('http'):
                    link = urljoin(url, link)
                
                # Descripción/Párrafo
                desc_elem = article.find('p')
                description = desc_elem.get_text(strip=True) if desc_elem else ""
                
                # Imagen
                img_elem = article.find('img')
                image_url = ""
                if img_elem:
                    image_url = img_elem.get('src', '') or img_elem.get('data-src', '')
                    if image_url and not image_url.startswith('http'):
                        image_url = urljoin('https://www.marca.com', image_url)
                
                # Hora
                time_elem = article.find('time') or article.find('span', class_=re.compile('time|fecha'))
                published_at = time_elem.get_text(strip=True) if time_elem else datetime.now().isoformat()
                
                news_dict = {
                    'title': title,
                    'description': description,
                    'content': description,
                    'image_url': image_url,
                    'source': 'Marca',
                    'source_url': link,
                    'author': 'Marca',
                    'published_at': published_at
                }
                
                news_list.append(news_dict)
                
            except Exception as e:
                print(f"Error procesando artículo Marca: {e}")
                continue
        
        print(f"✓ Marca: {len(news_list)} noticias encontradas")
        return news_list
        
    except requests.exceptions.RequestException as e:
        print(f"Error conectando a Marca: {e}")
        return news_list
    except Exception as e:
        print(f"Error scraping Marca: {e}")
        return news_list
