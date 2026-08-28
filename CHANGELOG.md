# Changelog

Todos los cambios importantes de este proyecto serán documentados en este archivo.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).

## [1.0.0] - 2024-01-15

### Agregado

- ✅ Sistema de 3 columnas
  - Columna 1: Listado de fuentes (OneFootball, Marca, Goal, Instagram)
  - Columna 2: Feed de noticias con preview
  - Columna 3: Contenido de texto puro

- ✅ Scrapers para múltiples fuentes
  - OneFootball (https://onefootball.com/es/inicio)
  - Marca (https://www.marca.com/futbol.html)
  - Goal (https://www.goal.com/es/noticias)
  - Instagram Fabrizio Romano (@fabriziorom)

- ✅ Funcionalidades principales
  - Botón Refresh para actualizar noticias
  - Modo Oscuro/Claro con persistencia
  - Filtro de noticias por palabras clave
  - Botón Copiar contenido al portapapeles
  - Contador de noticias en tiempo real (NOTITOTAL)

- ✅ Backend
  - API REST con Flask
  - Scraping automático cada 30 segundos
  - Limpieza automática de noticias > 12 horas
  - Base de datos SQLite
  - APScheduler para tareas automáticas
  - CORS habilitado

- ✅ Frontend
  - React 18 con Vite
  - Diseño responsivo (Desktop, Tablet, Mobile)
  - Grid de 3 columnas
  - LocalStorage para preferencias
  - Interfaz intuitiva y moderna

- ✅ Despliegue
  - Preparado para Vercel
  - GitHub + Vercel CI/CD
  - Docker Compose para desarrollo
  - Documentación completa

- ✅ Documentación
  - README.md con instrucciones de instalación
  - DEPLOY.md con guía paso a paso
  - Comentarios en código
  - Ejemplos de uso

### Técnico

- Backend: Flask + BeautifulSoup4 + APScheduler
- Frontend: React 18 + Vite + CSS3
- Base de datos: SQLite con limpieza automática
- Hosting: Vercel (versión gratuita)
- Control de versiones: Git + GitHub

### Cambios

- Arquitectura modular y escalable
- Separación clara Backend/Frontend
- Código limpio y bien documentado

### Arreglado

- CORS habilitado para desarrollo
- Timeouts configurables para scrapers
- Manejo de errores en scrapers

## Próximas Características Planeadas

### v1.1.0 (Planeado)

- [ ] Agregar más fuentes de noticias
- [ ] Notificaciones push para noticias nuevas
- [ ] Exportar noticias a JSON/CSV
- [ ] Historial de búsquedas
- [ ] Favoritos/Bookmarks
- [ ] Tema personalizado (color primario)
- [ ] Integración con API Twitter para transferencias
- [ ] Caché mejorado con Redis

### v1.2.0 (Planeado)

- [ ] Base de datos PostgreSQL/MongoDB
- [ ] Autenticación de usuarios
- [ ] Perfil de usuario
- [ ] Listas personalizadas
- [ ] Compartir noticias en redes sociales
- [ ] Modo offline
- [ ] PWA (Progressive Web App)

### v2.0.0 (Planeado)

- [ ] Aplicación móvil nativa (React Native)
- [ ] Análisis de datos con gráficos
- [ ] Recomendaciones personalizadas
- [ ] API pública para terceros
- [ ] Webhook para integraciones
- [ ] Administrador de contenido

## Notas de Versiones Anteriores

### v0.1.0 - Versión Beta
- Prototipo inicial con estructura básica
- Implementación de scraping manual
- UI básica sin estilos

---

## Cómo Contribuir

Para reportar bugs o sugerir features:

1. Abre un [GitHub Issue](https://github.com/tuusuario/football-news-app/issues)
2. Describe el problema o idea
3. Proporciona ejemplos si es posible
4. Envía un Pull Request si tienes una solución

## Mantenimiento

- **Última actualización**: Enero 2024
- **Estado**: Activo
- **Versión actual**: 1.0.0
- **Licencia**: MIT

---

**¡Gracias por usar Football News App! ⚽**
