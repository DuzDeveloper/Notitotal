"""
Scraper para Marca - noticias de fútbol
https://www.marca.com/futbol.html
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
import re

def get_article_content(url, timeout=10):
    """Extrae contenido completo de artículo Marca limpio"""
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
        
        for element in soup.find_all(['a', 'div', 'span'], class_=re.compile('share|social|comment|follow|telegram|whatsapp|facebook|twitter|mail', re.I)):
            element.decompose()
        
        for element in soup.find_all(['div', 'span'], string=re.compile('Seguir|Compartir|Mostrar|comentarios', re.I)):
            parent = element.parent
            if parent:
                parent.decompose()
        
        article = soup.find('article')
        if not article:
            article = soup.find('div', class_=re.compile('content|body|article'))
        if not article:
            article = soup.body
        
        if not article:
            return ""
        
        content_text = ""
        paragraphs = article.find_all('p')
        
        for p in paragraphs:
            text = p.get_text(strip=True)
            if text and len(text) > 20:
                if not any(x in text.lower() for x in ['compartir', 'seguir', 'comentarios', 'mail', 'telegram', 'whatsapp', 'facebook', 'twitter']):
                    content_text += text + "\n\n"
        
        content_text = re.sub(r'\n\n+', '\n\n', content_text)
        content_text = '\n'.join([line.strip() for line in content_text.split('\n') if line.strip()])
        
        return content_text if content_text else ""
        
    except Exception as e:
        return ""

def scrape_marca():
    """Scrape de Marca - noticias de fútbol"""
    news_list = []
    
    try:
        url = 'https://www.marca.com/futbol.html'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            return news_list
        
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all(['article', 'div'], class_=re.compile('ue-c|ue-w|article'), limit=10)
        
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
                        image_url = urljoin('https://www.marca.com', image_url)
                
                time_elem = article.find('time') or article.find('span', class_=re.compile('time|fecha'))
                published_at = time_elem.get_text(strip=True) if time_elem else datetime.now().isoformat()
                
                full_content = get_article_content(link) if link else ""
                if not full_content:
                    full_content = description
                
                news_dict = {
                    'title': title,
                    'description': description,
                    'content': full_content,
                    'image_url': image_url,
                    'source': 'Marca',
                    'source_url': link,
                    'author': 'Marca',
                    'published_at': published_at
                }
                
                news_list.append(news_dict)
                
            except Exception as e:
                continue
        
        print(f"Marca: {len(news_list)} noticias")
        return news_list
        
    except Exception as e:
        print(f"Error Marca: {e}")
        return news_list
