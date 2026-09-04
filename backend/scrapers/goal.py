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
        
        # Remover elementos no deseados
        for element in soup(['script', 'style', 'nav', 'footer', 'aside', 'iframe']):
            element.decompose()
        
        # Goal.com usa múltiples estructuras, intentar varias
        content_text = ""
        
        # Buscar contenido en diferentes selectores (Goal cambia su estructura)
        selectors = [
            'article',
            '[role="main"]',
            '.article-content',
            '.article_body',
            '.story-body',
            '.article__body',
            'main article',
            'main',
            '.content-body'
        ]
        
        article = None
        for selector in selectors:
            article = soup.select_one(selector)
            if article:
                break
        
        if not article:
            # Último recurso: tomar todo el body
            article = soup.body if soup.body else soup
        
        # Extraer párrafos
        paragraphs = article.find_all('p')
        
        for p in paragraphs:
            text = p.get_text(strip=True)
            if text and len(text) > 20:  # Filtrar párrafos muy cortos
                content_text += text + "\n\n"
        
        # Si no encontramos párrafos, intentar div class content
        if not content_text:
            content_divs = article.find_all('div', class_=re.compile('content|text|body', re.I))
            for div in content_divs[:5]:
                text = div.get_text(separator='\n', strip=True)
                if text:
                    content_text += text + "\n\n"
        
        # Si aún no hay contenido, obtener todo el texto
        if not content_text:
            content_text = article.get_text(separator='\n', strip=True)
        
        # Limpiar
        content_text = re.sub(r'\n\s*\n', '\n', content_text)
        content_text = re.sub(r' +', ' ', content_text)
        content_text = '\n'.join([line.strip() for line in content_text.split('\n') if line.strip()])
        
        # Limitar a 3000 caracteres para Goal (que tiene artículos largos)
        return content_text[:3000] if content_text else ""
        
    except Exception as e:
        print(f"Error extrayendo contenido Goal: {e}")
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
        
        # Goal.com usa diferentes estructuras para artículos
        articles = soup.find_all(['article', 'div'], class_=re.compile('card|news|article-item|article', re.I), limit=10)
        
        for article in articles:
            try:
                # Extraer título
                title_elem = article.find(['h2', 'h3', 'span', 'a'])
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                
                if not title or len(title) < 10:
                    continue
                
                # Extraer URL
                link_elem = article.find('a', href=True)
                link = link_elem.get('href', '') if link_elem else ''
                
                if link and not link.startswith('http'):
                    link = urljoin('https://www.goal.com', link)
                
                # Extraer descripción
                desc_elem = article.find('p')
                description = desc_elem.get_text(strip=True) if desc_elem else ""
                
                # Extraer imagen
                img_elem = article.find('img')
                image_url = ""
                if img_elem:
                    image_url = img_elem.get('src', '') or img_elem.get('data-src', '')
                    if image_url and not image_url.startswith('http'):
                        image_url = urljoin('https://www.goal.com', image_url)
                
                # Extraer fecha
                time_elem = article.find(['time', 'span'], class_=re.compile('time|fecha|date', re.I))
                published_at = time_elem.get_text(strip=True) if time_elem else datetime.now().isoformat()
                
                # ← EXTRAER CONTENIDO COMPLETO (MEJORADO PARA GOAL)
                full_content = ""
                if link:
                    full_content = get_article_content_goal(link)
                
                # Si no hay contenido, usar descripción
                if not full_content:
                    full_content = description
                
                news_dict = {
                    'title': title,
                    'description': description,
                    'content': full_content,  # ← CONTENIDO COMPLETO EXTRAÍDO
                    'image_url': image_url,
                    'source': 'Goal',
                    'source_url': link,
                    'author': 'Goal',
                    'published_at': published_at
                }
                
                news_list.append(news_dict)
                print(f"✓ Artículo Goal: {title[:50]}... ({len(full_content)} caracteres)")
                
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
