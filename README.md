# ⚽ Football News App

Aplicación web para recopilar y mostrar noticias de fútbol optimizadas para crear videos en YouTube Shorts, TikTok y Reels.

## 🎯 Características

- **3 Columnas Responsivas**
  - Columna 1: Listado de fuentes (OneFootball, Marca, Goal, Instagram)
  - Columna 2: Preview de noticias con imagen, título, hora y fuente
  - Columna 3: Contenido de texto puro (sin imágenes, sin videos, sin publicidades)

- **Funcionalidades**
  - 🔄 Botón Refresh: actualizar noticias en tiempo real
  - 🌙 Modo Oscuro: cambiar entre tema claro y oscuro
  - 🔍 Filtro de noticias: buscar por palabras clave
  - 📋 Copiar contenido: con un click llevar el texto al portapapeles
  - ⏰ Limpieza automática: noticias > 12 horas se eliminan automáticamente
  - 📊 Contador de noticias: NOTITOTAL en tiempo real

- **Scraping**
  - OneFootball: https://onefootball.com/es/inicio
  - Marca: https://www.marca.com/futbol.html
  - Goal: https://www.goal.com/es/noticias
  - Instagram Fabrizio Romano: transferencias

## 🛠️ Stack Tecnológico

### Backend
- **Framework**: Flask
- **Scraping**: BeautifulSoup4 + Requests
- **Scheduler**: APScheduler
- **BD**: SQLite
- **API**: RESTful

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Estilos**: CSS3 (Grid + Flexbox)
- **Almacenamiento**: LocalStorage

### Despliegue
- **Código**: GitHub
- **Hosting**: Vercel (versión gratuita)

## 📋 Requisitos Previos

- Node.js 16+
- Python 3.9+
- Git

## 🚀 Instalación Local

### 1. Clonar el repositorio

```bash
git clone https://github.com/tuusuario/football-news-app.git
cd football-news-app
```

### 2. Configurar Backend

```bash
# Navegar a la carpeta backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env (opcional)
echo "FLASK_ENV=development" > .env
echo "DATABASE_PATH=news.db" >> .env

# Ejecutar el servidor
python app.py
```

El backend estará disponible en `http://localhost:5000`

### 3. Configurar Frontend

```bash
# Navegar a la carpeta frontend (en otra terminal)
cd frontend

# Instalar dependencias
npm install

# Crear archivo .env.local
echo "REACT_APP_API_URL=http://localhost:5000" > .env.local

# Ejecutar servidor de desarrollo
npm run dev
```

El frontend estará disponible en `http://localhost:3000`

## 📡 API Endpoints

### GET `/api/news`
Obtener noticias con filtros opcionales
```bash
GET /api/news?source=all&search=messi
```

**Parámetros:**
- `source`: 'all', 'OneFootball', 'Marca', 'Goal', 'Instagram (Fabrizio)'
- `search`: texto de búsqueda

**Respuesta:**
```json
{
  "status": "success",
  "count": 25,
  "news": [
    {
      "title": "...",
      "description": "...",
      "content": "...",
      "image_url": "...",
      "source": "Marca",
      "source_url": "...",
      "author": "...",
      "published_at": "2024-01-15T10:30:00"
    }
  ]
}
```

### GET `/api/sources`
Obtener lista de fuentes disponibles

### POST `/api/refresh`
Forzar refresh de noticias

### GET `/api/stats`
Obtener estadísticas de noticias

### POST `/api/cleanup`
Limpiar noticias > 12 horas

## 🌐 Despliegue en Vercel

### 1. Preparar repositorio Git

```bash
git init
git add .
git commit -m "Initial commit: Football News App"
git branch -M main
git remote add origin https://github.com/tuusuario/football-news-app.git
git push -u origin main
```

### 2. Conectar con Vercel

1. Ir a https://vercel.com
2. Hacer login/signup
3. Click en "New Project"
4. Seleccionar el repositorio de GitHub
5. Configurar:
   - **Root Directory**: . (raíz del proyecto)
   - **Build Command**: `npm run build && cd backend && pip install -r requirements.txt`
   - **Output Directory**: `frontend/dist`
6. Agregar variables de entorno:
   ```
   FLASK_ENV=production
   DATABASE_PATH=/tmp/news.db
   REACT_APP_API_URL=https://tuapp.vercel.app
   ```
7. Click en "Deploy"

### 3. Configuración Post-Despliegue

- Las noticias se limpiarán automáticamente cada 12 horas
- El scraping se ejecutará cada 30 segundos
- La BD SQLite se almacenará en `/tmp/` (temporal en Vercel)

Para persistencia de datos a largo plazo, considera usar:
- PostgreSQL (Vercel Postgres)
- MongoDB (MongoDB Atlas)
- Supabase

## 🔄 Flujo de Scraping

1. **Inicio**: Al arrancar la app, se hace scrape inicial de todas las fuentes
2. **Renovación**: Cada 30 segundos se actualiza automáticamente
3. **Limpieza**: Cada 1 hora se eliminan noticias > 12 horas
4. **Manual**: Click en botón "Refresh" para actualizar manualmente

## 📱 Diseño Responsive

La app se adapta a diferentes tamaños de pantalla:

- **Desktop (1200px+)**: 3 columnas
- **Tablet (768px - 1200px)**: 2 columnas + 1 full-width
- **Mobile (<768px)**: 1 columna apilada

## 🎨 Personalización

### Cambiar colores
Editar variables CSS en `frontend/src/App.css`:
```css
:root {
  --primary-color: #e74c3c;  /* Cambiar color principal */
  --secondary-color: #2c3e50;
}
```

### Agregar nuevas fuentes
1. Crear nuevo scraper en `backend/scrapers/newsource.py`
2. Importar en `backend/app.py`
3. Agregar a la lista de scrapers en `scrape_all_sources()`

### Cambiar intervalo de limpieza
En `backend/app.py`:
```python
CLEANUP_INTERVAL = 3600  # 1 hora (en segundos)
```

## 🐛 Solución de Problemas

### Las noticias no se cargan
- Verificar que el backend está corriendo en `http://localhost:5000`
- Revisar consola del navegador para errores
- Comprobar que CORS está habilitado en Flask

### Error de CORS
Si ves error de CORS, asegúrate de que `Flask-CORS` está instalado:
```bash
pip install Flask-CORS
```

### Base de datos corrupta
Eliminar `news.db` y reiniciar la app (creará una nueva BD)

### Scraping muy lento
- Aumentar `SCRAPE_INTERVAL` en `backend/app.py`
- Reducir límite de noticias (actualmente 10 por fuente)
- Usar proxy si los sitios te bloquean

## 📚 Estructura del Proyecto

```
football-news-app/
├── backend/
│   ├── app.py                    # App principal Flask
│   ├── requirements.txt          # Dependencias Python
│   ├── news.db                   # BD SQLite (auto-generado)
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── onefootball.py
│   │   ├── marca.py
│   │   ├── goal.py
│   │   └── instagram_romano.py
│   └── utils/
│       ├── db.py                 # Operaciones de BD
│       └── cleanup.py            # Limpieza automática
├── frontend/
│   ├── src/
│   │   ├── App.jsx               # Componente principal
│   │   ├── App.css               # Estilos principales
│   │   ├── main.jsx              # Entry point
│   │   ├── index.css             # Estilos globales
│   │   └── components/
│   │       ├── Header.jsx        # Header con controles
│   │       ├── SourceList.jsx    # Columna 1
│   │       ├── NewsFeed.jsx      # Columna 2
│   │       ├── NewsDetail.jsx    # Columna 3
│   │       └── *.css             # Estilos por componente
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── .env.local
├── vercel.json                   # Config de Vercel
├── .gitignore
└── README.md
```

## 📝 Notas de Desarrollo

### Para agregar persistencia de datos en Vercel:

**Opción 1: Vercel Postgres**
```python
import psycopg2

conn = psycopg2.connect(os.getenv('DATABASE_URL'))
```

**Opción 2: Supabase**
```python
import supabase

supabase = supabase.create_client(url, key)
```

**Opción 3: MongoDB Atlas**
```python
from pymongo import MongoClient

client = MongoClient(os.getenv('MONGODB_URI'))
```

## 🤝 Contribuir

1. Hacer fork del proyecto
2. Crear rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

## 🆘 Soporte

Para reportar bugs o sugerir features, abre un Issue en GitHub.

---

**Hecho con ❤️ para content creators de fútbol**

¡Si te es útil, no olvides dejar una ⭐!
