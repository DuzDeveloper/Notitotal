"""
Scraper para OneFootball usando su API interna
"""

import requests
import json
from datetime import datetime
from urllib.parse import urljoin
import re
from utils.text_cleaner import clean_title, clean_description, clean_content

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Referer': 'https://onefootball.com/es/noticias',
}

def get_article_content(url):
    """Extrae contenido del artículo"""
    try:
        import time
        time.sleep(1)
        
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            return ""
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remover elementos
        for el in soup(['script', 'style']):
            el.decompose()
        
        # Buscar párrafos
        paragraphs = soup.find_all('p')
        content = "\n\n".join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20])
        
        return clean_content(content) if content else ""
    except:
        return ""

def scrape_onefootball():
    """
    Scrape de OneFootball
    Intenta multiples estrategias
    """
    news_list = []
    
    # Estrategia 1: Intentar API GraphQL
    try:
        print("Intentando API GraphQL de OneFootball...")
        
        api_url = "https://www.onefootball.com/api/v3/news"
        params = {
            'limit': 30,
            'offset': 0,
            'countryCode': 'es',
        }
        
        response = requests.get(api_url, params=params, headers=HEADERS, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"API respondió con {len(data.get('data', []))} noticias")
            
            for article in data.get('data', [])[:30]:
                try:
                    title = article.get('title', '')
                    url = article.get('url', '')
                    image = article.get('image', {}).get('url', '') if article.get('image') else ''
                    
                    if not title or not url:
                        continue
                    
                    # Extraer descripción
                    description = article.get('description', '') or article.get('teaser', '')
                    
                    # Extraer contenido
                    content = article.get('body', '') or article.get('content', '') or description
                    
                    news_dict = {
                        'title': clean_title(title),
                        'description': clean_description(description),
                        'content': clean_content(content) if content else description,
                        'image_url': image,
                        'source': 'OneFootball',
                        'source_url': url,
                        'author': 'OneFootball',
                        'published_at': article.get('publishedAt', datetime.now().isoformat())
                    }
                    
                    news_list.append(news_dict)
                    print(f"✓ {title[:50]}...")
                    
                except Exception as e:
                    print(f"Error procesando artículo: {e}")
                    continue
            
            if news_list:
                print(f"✓ OneFootball (API): {len(news_list)} noticias")
                return news_list
    
    except Exception as e:
        print(f"API GraphQL falló: {e}")
    
    # Estrategia 2: Intenta RSS Feed
    try:
        print("Intentando RSS Feed de OneFootball...")
        
        rss_urls = [
            'https://www.onefootball.com/feeds/es',
            'https://www.onefootball.com/es/rss',
        ]
        
        for rss_url in rss_urls:
            try:
                response = requests.get(rss_url, headers=HEADERS, timeout=10)
                
                if response.status_code == 200:
                    import xml.etree.ElementTree as ET
                    root = ET.fromstring(response.content)
                    
                    # Buscar items en el feed
                    for item in root.findall('.//item')[:30]:
                        try:
                            title_elem = item.find('title')
                            link_elem = item.find('link')
                            desc_elem = item.find('description')
                            
                            if title_elem is None or link_elem is None:
                                continue
                            
                            title = title_elem.text or ''
                            link = link_elem.text or ''
                            description = desc_elem.text or '' if desc_elem else ''
                            
                            if not title or not link:
                                continue
                            
                            # Extraer contenido de la página
                            content = get_article_content(link)
                            if not content:
                                content = description
                            
                            news_dict = {
                                'title': clean_title(title),
                                'description': clean_description(description),
                                'content': content,
                                'image_url': '',
                                'source': 'OneFootball',
                                'source_url': link,
                                'author': 'OneFootball',
                                'published_at': datetime.now().isoformat()
                            }
                            
                            news_list.append(news_dict)
                            print(f"✓ {title[:50]}...")
                            
                        except Exception as e:
                            continue
                    
                    if news_list:
                        print(f"✓ OneFootball (RSS): {len(news_list)} noticias")
                        return news_list
            
            except Exception as e:
                continue
    
    except Exception as e:
        print(f"RSS Feed falló: {e}")
    
    print(f"✗ OneFootball: No se pudieron extraer noticias")
    return []
