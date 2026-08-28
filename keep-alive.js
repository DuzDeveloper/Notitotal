// keep-alive.js - Mantiene el backend activo en Render
const BACKEND_URL = 'https://notitotal-backend.onrender.com';

async function keepAlive() {
  try {
    const response = await fetch(`${BACKEND_URL}/api/health`);
    if (response.ok) {
      console.log('✓ Backend is alive');
    }
  } catch (error) {
    console.error('✗ Backend is sleeping');
  }
}

// Ejecutar cada 14 minutos (Render se duerme después de 15)
setInterval(keepAlive, 14 * 60 * 1000);
keepAlive(); // Primera ejecución inmediata
