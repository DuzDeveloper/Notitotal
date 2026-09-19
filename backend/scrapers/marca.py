"""
Scraper para Marca - noticias de fútbol
https://www.marca.com/futbol.html
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
import re
from utils.text_cleaner import clean_title, clean_description, clean_content

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
                if not any(x in text.lower() for x in ['compartir', 'seguir', 'comentarios', 'mail']):
                    content_text += text + "\n\n"
        
        content_text = re.sub(r'\n\n+', '\n\n', content_text)
        return clean_content(content_text) if content_text else ""
        
    except Exception as e:
        print(f"Error extrayendo contenido Marca: {e}")
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
            print(f"Error: Status {response.status_code} en Marca")
            return news_list
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Intentar múltiples estrategias para encontrar artículos
        articles = []
        
        # Estrategia 1: buscar por article tags
        articles = soup.find_all('article', limit=20)
        print(f"Marca - Encontrados {len(articles)} articles tags")
        
        # Estrategia 2: Si no hay article tags, buscar divs con clase
        if not articles:
            articles = soup.find_all('div', class_=re.compile('ue-c|ue-w|card|news', re.I), limit=20)
            print(f"Marca - Encontrados {len(articles)} divs con clase")
        
        # Estrategia 3: Buscar links
        if not articles:
            links = soup.find_all('a', href=re.compile('/futbol/'), limit=20)
            articles = [link.parent for link in links if link.parent]
            print(f"Marca - Encontrados {len(articles)} parents de links")
        
        for idx, article in enumerate(articles):
            try:
                # Extraer título - intentar múltiples selectores
                title = ""
                title_elem = article.find(['h2', 'h3', 'h4', 'a'])
                
                if title_elem:
                    title = clean_title(title_elem.get_text(strip=True))
                
                if not title or len(title) < 10:
                    print(f"Marca - Artículo {idx}: No title encontrado")
                    continue
                
                # Extraer URL
                link = ""
                link_elem = article.find('a', href=True)
                if link_elem:
                    link = link_elem.get('href', '')
                
                if link and not link.startswith('http'):
                    link = urljoin(url, link)
                
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
                        image_url = urljoin('https://www.marca.com', image_url)
                
                # Extraer fecha
                published_at = datetime.now().isoformat()
                
                # Extraer contenido
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
                print(f"Marca - Artículo {idx}: {title[:50]}...")
                
            except Exception as e:
                print(f"Marca - Error en artículo {idx}: {e}")
                continue
        
        print(f"✓ Marca: {len(news_list)} noticias encontradas")
        return news_list
        
    except Exception as e:
        print(f"Error scraping Marca: {e}")
        return news_list
