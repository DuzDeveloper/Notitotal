#!/usr/bin/env python
"""
Script de prueba rápida para validar que todo funciona correctamente
"""

import requests
import json
from datetime import datetime

def test_backend():
    """Probar conexión con backend"""
    print("\n" + "="*60)
    print("🧪 PRUEBA DE BACKEND")
    print("="*60)
    
    api_url = "http://localhost:5000"
    
    # Test 1: Health check
    print("\n✓ Test 1: Health Check")
    try:
        response = requests.get(f"{api_url}/api/health")
        if response.status_code == 200:
            print(f"  ✓ Backend online: {response.json()}")
        else:
            print(f"  ✗ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ✗ No se pudo conectar: {e}")
        return False
    
    # Test 2: Obtener fuentes
    print("\n✓ Test 2: Obtener Fuentes")
    try:
        response = requests.get(f"{api_url}/api/sources")
        if response.status_code == 200:
            sources = response.json()
            print(f"  ✓ Fuentes disponibles: {sources['sources']}")
        else:
            print(f"  ✗ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False
    
    # Test 3: Obtener noticias
    print("\n✓ Test 3: Obtener Noticias")
    try:
        response = requests.get(f"{api_url}/api/news")
        if response.status_code == 200:
            data = response.json()
            count = data.get('count', 0)
            print(f"  ✓ Noticias obtenidas: {count}")
            if count > 0:
                first_news = data['news'][0]
                print(f"    - Primer artículo: {first_news['title'][:50]}...")
                print(f"    - Fuente: {first_news['source']}")
        else:
            print(f"  ✗ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False
    
    # Test 4: Estadísticas
    print("\n✓ Test 4: Estadísticas")
    try:
        response = requests.get(f"{api_url}/api/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"  ✓ Total de noticias: {stats.get('total_news', 0)}")
            if stats.get('by_source'):
                print(f"  ✓ Por fuente:")
                for source, count in stats['by_source'].items():
                    print(f"    - {source}: {count}")
        else:
            print(f"  ✗ Error: {response.status_code}")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    print("\n" + "="*60)
    print("✓ PRUEBAS DE BACKEND COMPLETADAS")
    print("="*60)
    
    return True

def test_frontend():
    """Probar conexión con frontend"""
    print("\n" + "="*60)
    print("🧪 PRUEBA DE FRONTEND")
    print("="*60)
    
    try:
        response = requests.get("http://localhost:3000")
        if response.status_code == 200:
            print("✓ Frontend está online en http://localhost:3000")
            return True
        else:
            print(f"✗ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ No se pudo conectar al frontend: {e}")
        print("  Asegúrate de ejecutar: npm run dev")
        return False

def main():
    print("\n")
    print("   ⚽ FOOTBALL NEWS APP - TEST SUITE ⚽")
    print("\n")
    
    backend_ok = test_backend()
    frontend_ok = test_frontend()
    
    print("\n" + "="*60)
    print("📊 RESUMEN")
    print("="*60)
    print(f"Backend:  {'✓ OK' if backend_ok else '✗ FALLO'}")
    print(f"Frontend: {'✓ OK' if frontend_ok else '✗ FALLO (esperado si no está corriendo)'}")
    print("="*60 + "\n")
    
    if backend_ok:
        print("✓ El backend está funcionando correctamente!")
        print("✓ Ahora abre http://localhost:3000 en tu navegador")
    else:
        print("✗ El backend no está disponible")
        print("✓ Ejecuta: python backend/app.py")

if __name__ == '__main__':
    main()
