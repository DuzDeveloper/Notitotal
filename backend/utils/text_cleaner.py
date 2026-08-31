"""
Utilidad para limpiar y extraer solo texto puro de HTML
"""

from bs4 import BeautifulSoup
import re

def extract_plain_text(html_content):
    """
    Extrae solo texto puro de contenido HTML
    Sin imágenes, videos, ni publicidades
    """
    if not html_content:
        return ""
    
    try:
        # Parsear HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remover scripts, styles, y elementos no deseados
        for script in soup(['script', 'style', 'nav', 'footer', 'aside']):
            script.decompose()
        
        # Obtener solo texto
        text = soup.get_text(separator='\n', strip=True)
        
        # Limpiar espacios en blanco excesivos
        text = re.sub(r'\n\s*\n', '\n', text)  # Múltiples saltos de línea
        text = re.sub(r' +', ' ', text)  # Múltiples espacios
        
        # Limitar a primeros 500 caracteres para evitar contenido muy largo
        text = text[:500].strip()
        
        return text
    except Exception as e:
        print(f"Error extrayendo texto: {e}")
        return html_content[:500] if html_content else ""

def clean_title(title):
    """Limpia el título de caracteres especiales"""
    return title.strip() if title else ""
