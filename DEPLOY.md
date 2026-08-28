# 📱 Guía de Despliegue en Vercel

Esta guía te ayudará a desplegar tu Football News App en Vercel de forma gratuita.

## Requisitos Previos

- Cuenta de GitHub
- Cuenta de Vercel (opcional, puedes crear con GitHub)
- Repositorio de código en GitHub

## Paso 1: Preparar el repositorio

### 1.1 Crear un nuevo repositorio en GitHub

```bash
# Si aún no has inicializado git
git init
git add .
git commit -m "Initial commit: Football News App"
git branch -M main
git remote add origin https://github.com/tuusuario/football-news-app.git
git push -u origin main
```

### 1.2 Asegurarse que el repositorio tiene la estructura correcta

```
football-news-app/
├── backend/          # API Flask
├── frontend/         # React app
├── vercel.json       # Config Vercel
├── package.json      # Scripts globales
├── .gitignore
└── README.md
```

## Paso 2: Configurar Vercel

### 2.1 Ir a Vercel

1. Abre https://vercel.com
2. Click en "Sign Up" o "Log In" (con GitHub)

### 2.2 Conectar repositorio

1. Click en "New Project"
2. Selecciona "Import Git Repository"
3. Busca y selecciona `football-news-app`
4. Click en "Import"

### 2.3 Configurar el proyecto

**Root Directory:**
- Dejar en blanco o seleccionar `.` (raíz del proyecto)

**Build Command:**
```
npm install && npm run build && cd backend && pip install -r requirements.txt
```

**Output Directory:**
```
frontend/dist
```

### 2.4 Agregar variables de entorno

Click en "Environment Variables" y agregar:

```
FLASK_ENV = production
DATABASE_PATH = /tmp/news.db
REACT_APP_API_URL = https://tuapp.vercel.app
```

Reemplazar `tuapp` con el nombre que Vercel te asigne.

## Paso 3: Desplegar

Click en "Deploy"

Vercel comenzará a:
1. Instalar dependencias
2. Compilar el frontend
3. Preparar el backend
4. Desplegar todo

**⏱️ Esto puede tomar 2-5 minutos**

## Paso 4: Verificar despliegue

### 4.1 Revisar la URL de producción

Una vez completado, Vercel te mostrará una URL como:
```
https://football-news-app-xyz123.vercel.app
```

### 4.2 Pruebas básicas

Abre en tu navegador:
- `https://tuapp.vercel.app/` → Debe cargar la app
- `https://tuapp.vercel.app/api/health` → Debe devolver JSON

### 4.3 Solucionar problemas

Si ves errores, revisa los logs:
1. Abre Dashboard de Vercel
2. Click en tu proyecto
3. Ir a "Deployments"
4. Click en el deployment reciente
5. Ver logs de "Build" o "Runtime"

## Paso 5: Configuración avanzada (Opcional)

### 5.1 Agregar dominio personalizado

1. En Vercel Dashboard → Settings → Domains
2. Agregar tu dominio
3. Configurar DNS en tu proveedor de dominios

### 5.2 Configurar CI/CD automático

Ya está configurado! Cada push a `main` dispara un nuevo deployment.

### 5.3 Monitorear rendimiento

En Vercel Dashboard puedes ver:
- Tiempo de compilación
- Tamaño de bundle
- Tráfico de API
- Errores en tiempo real

## Problemas Comunes y Soluciones

### ❌ Error: "No such file or directory: 'backend/requirements.txt'"

**Solución:** Asegúrate que `backend/requirements.txt` existe en tu repositorio

```bash
ls -la backend/requirements.txt
```

### ❌ Error: "Cannot find module 'Flask'"

**Solución:** Vercel no está instalando dependencias Python. Revisar:
- `pip install` está en el Build Command
- `requirements.txt` tiene todos los paquetes

### ❌ API devuelve 502 Bad Gateway

**Solución:** El backend está fallando. Revisar logs:
```bash
# Localmente
python backend/app.py

# Buscar errores en los logs de Vercel
```

### ❌ Frontend no se ve, solo código blanco

**Solución:** El build no completó. Revisar:
- `package.json` existe en `frontend/`
- `npm run build` genera `dist/`
- Paths en `vite.config.js` son correctos

### ❌ "CORS error" o "API no responde"

**Solución:** Actualizar `REACT_APP_API_URL`:

1. En Vercel Dashboard → Settings → Environment Variables
2. Cambiar `REACT_APP_API_URL` a tu URL de Vercel real
3. Redeploy (ir a Deployments y hacer redeploy del último)

### ❌ Las noticias no se cargan

**Solución:** Verificar que:
1. Backend está activo: `tuapp.vercel.app/api/health`
2. Scrapers funcionan: revisar logs de backend
3. Base de datos tiene datos: `/tmp/news.db` (temporal en Vercel)

## Actualizar la app en Vercel

Simplemente hacer push a GitHub:

```bash
git add .
git commit -m "Update: nombre del cambio"
git push origin main
```

Vercel detectará el cambio y desplegará automáticamente.

## Base de datos en Vercel

**⚠️ IMPORTANTE:** La versión actual usa SQLite en `/tmp/` que es temporal en Vercel.

Para persistencia de datos a largo plazo:

### Opción 1: Vercel Postgres (Recomendado para Vercel)

```bash
npm install @vercel/postgres
```

Crear y conectar en Vercel Dashboard.

### Opción 2: PostgreSQL externo (Railway, Supabase)

```python
import os
DATABASE_URL = os.getenv('DATABASE_URL')
```

### Opción 3: MongoDB Atlas (NoSQL)

```python
from pymongo import MongoClient
client = MongoClient(os.getenv('MONGODB_URI'))
```

## Limpieza y mantenimiento

### Ver consumo de recursos

Vercel Dashboard → Usage

### Limpiar histórico de deployments

Vercel mantiene automáticamente los últimos deployments activos.

### Desactivar un deployment

1. Ir a Deployments
2. Click en el deployment
3. Click en "Promote to Production" o "Demote from Production"

## 🎉 ¡Listo!

Tu aplicación está en vivo en Vercel y se actualiza automáticamente con cada push a GitHub.

---

## Soporte y recursos adicionales

- **Docs de Vercel:** https://vercel.com/docs
- **Vercel Discord:** https://discord.gg/vercel
- **GitHub Issues:** Si hay problemas, crea un issue

¡Que disfrutes tu Football News App! ⚽
