"""
Utilidades para limpiar texto
"""

import re
import html

def clean_title(title):
    """Limpia y normaliza títulos"""
    if not title:
        return ""
    
    # Decodificar entidades HTML
    title = html.unescape(title)
    
    # Remover saltos de línea y espacios múltiples
    title = re.sub(r'\s+', ' ', title)
    
    # Remover caracteres especiales problemáticos
    title = title.replace('\n', ' ')
    title = title.replace('\r', ' ')
    title = title.replace('\t', ' ')
    
    # Trim de espacios
    title = title.strip()
    
    # Limitar a 200 caracteres máximo
    if len(title) > 200:
        title = title[:197] + '...'
    
    return title

def clean_description(description):
    """Limpia y normaliza descripciones"""
    if not description:
        return ""
    
    description = html.unescape(description)
    description = re.sub(r'\s+', ' ', description)
    description = description.replace('\n', ' ')
    description = description.strip()
    
    if len(description) > 300:
        description = description[:297] + '...'
    
    return description

def clean_content(content):
    """Limpia contenido extraído"""
    if not content:
        return ""
    
    content = html.unescape(content)
    
    # Remover múltiples saltos de línea
    content = re.sub(r'\n\s*\n', '\n\n', content)
    
    # Remover espacios múltiples
    content = re.sub(r' +', ' ', content)
    
    # Remover tabs
    content = content.replace('\t', '')
    
    return content.strip()
