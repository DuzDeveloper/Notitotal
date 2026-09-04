"""
Scraper para Goal - noticias de fútbol mundial
https://www.goal.com/es/noticias
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
import re

def get_article_content_goal(url, timeout=10):
    """Extrae contenido completo de artículo Goal.com"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            return ""
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for element in soup(['script', 'style', 'nav', 'footer', 'aside', 'iframe']):
            element.decompose()
        
        for element in soup.find_all(['a', 'div', 'span'], class_=re.compile('share|social|comment|follow', re.I)):
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
                if not any(x in text.lower() for x in ['compartir', 'seguir', 'comentarios']):
                    content_text += text + "\n\n"
        
        content_text = re.sub(r'\n\n+', '\n\n', content_text)
        content_text = '\n'.join([line.strip() for line in content_text.split('\n') if line.strip()])
        
        return content_text if content_text else ""
        
    except Exception as e:
        return ""

def scrape_goal():
    """Scrape de Goal"""
    news_list = []
    
    try:
        url = 'https://www.goal.com/es/noticias'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            return news_list
        
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('article', limit=10)
        
        for article in articles:
            try:
                title_elem = article.find(['h2', 'h3', 'a'])
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                if not title or len(title) < 10:
                    continue
                
                link_elem = article.find('a', href=True)
                link = link_elem.get('href', '') if link_elem else ''
                if link and not link.startswith('http'):
                    link = urljoin('https://www.goal.com', link)
                
                desc_elem = article.find('p')
                description = desc_elem.get_text(strip=True) if desc_elem else ""
                
                img_elem = article.find('img')
                image_url = img_elem.get('src', '') if img_elem else ""
                
                full_content = get_article_content_goal(link) if link else ""
                if not full_content:
                    full_content = description
                
                news_dict = {
                    'title': title,
                    'description': description,
                    'content': full_content,
                    'image_url': image_url,
                    'source': 'Goal',
                    'source_url': link,
                    'author': 'Goal',
                    'published_at': datetime.now().isoformat()
                }
                
                news_list.append(news_dict)
                
            except Exception as e:
                continue
        
        print(f"Goal: {len(news_list)} noticias")
        return news_list
        
    except Exception as e:
        print(f"Error Goal: {e}")
        return news_list
