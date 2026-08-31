"""
Scraper para Goal - noticias de fútbol mundial
https://www.goal.com/es/noticias
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
import re

def get_article_content(url, timeout=10):
    """Extrae contenido completo de artículo"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            return ""
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for element in soup(['script', 'style', 'nav', 'footer', 'aside']):
            element.decompose()
        
        article = soup.find('article') or soup.find('div', class_=re.compile('content|body'))
        
        if not article:
            article = soup.body if soup.body else soup
        
        text = article.get_text(separator='\n', strip=True)
        text = re.sub(r'\n\s*\n', '\n', text)
        text = re.sub(r' +', ' ', text)
        text = '\n'.join([line.strip() for line in text.split('\n') if line.strip()])
        
        return text[:1500] if text else ""
        
    except Exception as e:
        print(f"Error extrayendo contenido: {e}")
        return ""

def scrape_goal():
    """
    Scrape de Goal - noticias de fútbol mundial
    """
    news_list = []
    
    try:
        url = 'https://www.goal.com/es/noticias'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"Error: Status {response.status_code} en Goal")
            return news_list
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        articles = soup.find_all(['article', 'div'], class_=re.compile('card|news|article-item'), limit=10)
        
        for article in articles:
            try:
                title_elem = article.find(['h2', 'h3', 'span', 'a'])
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                
                if not title or len(title) < 10:
                    continue
                
                link_elem = article.find('a', href=True)
                link = link_elem.get('href', '') if link_elem else ''
                if link and not link.startswith('http'):
                    link = urljoin(url, link)
                
                desc_elem = article.find('p')
                description = desc_elem.get_text(strip=True) if desc_elem else ""
                
                img_elem = article.find('img')
                image_url = ""
                if img_elem:
                    image_url = img_elem.get('src', '') or img_elem.get('data-src', '')
                    if image_url and not image_url.startswith('http'):
                        image_url = urljoin('https://www.goal.com', image_url)
                
                time_elem = article.find(['time', 'span'], class_=re.compile('time|fecha|date'))
                published_at = time_elem.get_text(strip=True) if time_elem else datetime.now().isoformat()
                
                # ← EXTRAER CONTENIDO COMPLETO
                full_content = get_article_content(link) if link else ""
                if not full_content:
                    full_content = description
                
                news_dict = {
                    'title': title,
                    'description': description,
                    'content': full_content,  # ← CONTENIDO COMPLETO
                    'image_url': image_url,
                    'source': 'Goal',
                    'source_url': link,
                    'author': 'Goal',
                    'published_at': published_at
                }
                
                news_list.append(news_dict)
                
            except Exception as e:
                print(f"Error procesando artículo Goal: {e}")
                continue
        
        print(f"✓ Goal: {len(news_list)} noticias encontradas")
        return news_list
        
    except requests.exceptions.RequestException as e:
        print(f"Error conectando a Goal: {e}")
        return news_list
    except Exception as e:
        print(f"Error scraping Goal: {e}")
        return news_list
