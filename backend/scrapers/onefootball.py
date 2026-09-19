"""
Scraper para OneFootball usando Selenium
Simula un navegador real para burlar protección anti-bot
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
import re
import time
from utils.text_cleaner import clean_title, clean_description, clean_content

def get_article_content(url, timeout=10):
    """Extrae contenido de artículo"""
    try:
        time.sleep(1)
        
        # Configurar Selenium
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        try:
            driver.get(url)
            # Esperar a que cargue contenido
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "p"))
            )
            
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # Remover elementos no deseados
            for element in soup(['script', 'style', 'nav', 'footer', 'aside']):
                element.decompose()
            
            # Buscar contenido
            article = soup.find('article')
            if not article:
                article = soup.body
            
            if not article:
                return ""
            
            # Extraer párrafos
            content_text = ""
            paragraphs = article.find_all('p')
            
            for p in paragraphs:
                text = p.get_text(strip=True)
                if text and len(text) > 20:
                    content_text += text + "\n\n"
            
            content_text = re.sub(r'\n\n+', '\n\n', content_text)
            return clean_content(content_text) if content_text else ""
            
        finally:
            driver.quit()
        
    except Exception as e:
        print(f"Error extrayendo contenido OneFootball: {e}")
        return ""

def scrape_onefootball():
    """
    Scrape de OneFootball usando Selenium
    """
    news_list = []
    
    try:
        print("Iniciando Selenium para OneFootball...")
        
        # Configurar Selenium para headless
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        try:
            url = 'https://onefootball.com/es/inicio'
            print(f"Navegando a {url}...")
            driver.get(url)
            
            # Esperar a que cargue
            print("Esperando carga de elementos...")
            WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "article"))
            )
            
            # Scroll para cargar más noticias
            print("Scrolling para cargar más contenido...")
            for _ in range(3):
                driver.execute_script("window.scrollBy(0, 500)")
                time.sleep(2)
            
            # Obtener HTML renderizado
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # Buscar artículos
            articles = soup.find_all('article', limit=30)
            print(f"OneFootball - Encontrados {len(articles)} artículos")
            
            if not articles:
                # Intenta buscar divs si no hay articles
                articles = soup.find_all('div', class_=re.compile('article|news|card|story', re.I), limit=30)
                print(f"OneFootball - Encontrados {len(articles)} divs alternativos")
            
            # Procesar artículos
            for idx, article in enumerate(articles):
                try:
                    # Extraer título
                    title = ""
                    for tag in ['h2', 'h3', 'h4', 'a', 'span']:
                        title_elem = article.find(tag)
                        if title_elem:
                            title = clean_title(title_elem.get_text(strip=True))
                            if title and len(title) > 10:
                                break
                    
                    if not title or len(title) < 10:
                        continue
                    
                    # Extraer URL
                    link = ""
                    link_elem = article.find('a', href=True)
                    if link_elem:
                        link = link_elem.get('href', '')
                    
                    if link and not link.startswith('http'):
                        link = urljoin('https://onefootball.com', link)
                    
                    if not link or 'onefootball.com' not in link:
                        continue
                    
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
                            image_url = urljoin('https://onefootball.com', image_url)
                    
                    # Extraer contenido completo
                    full_content = get_article_content(link)
                    if not full_content:
                        full_content = description
                    
                    news_dict = {
                        'title': title,
                        'description': description,
                        'content': full_content,
                        'image_url': image_url,
                        'source': 'OneFootball',
                        'source_url': link,
                        'author': 'OneFootball',
                        'published_at': datetime.now().isoformat()
                    }
                    
                    news_list.append(news_dict)
                    print(f"OneFootball - Artículo {idx}: {title[:50]}...")
                    
                except Exception as e:
                    print(f"OneFootball - Error en artículo {idx}: {e}")
                    continue
            
        finally:
            driver.quit()
    
    except Exception as e:
        print(f"OneFootball - Error general: {e}")
    
    print(f"✓ OneFootball: {len(news_list)} noticias encontradas")
    return news_list
