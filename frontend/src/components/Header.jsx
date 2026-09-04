import React from 'react';
import './Header.css';

function Header({ newsCount, onRefresh, onToggleDarkMode, onSearch, searchTerm, loading }) {
  return (
    <header className="header">
      <div className="header-top">
        <div className="logo-section">
          <img src="/logo.png" alt="Notitotal" className="logo-image" />
          <h1>Notitotal</h1>
          <span className="news-count">NOTICIAS: {newsCount}</span>
        </div>

        <div className="controls">
          <button
            className={`btn-refresh ${loading ? 'loading' : ''}`}
            onClick={onRefresh}
            disabled={loading}
            title="Actualizar noticias"
          >
            {loading ? '⟳ Cargando...' : '⟳ Refresh'}
          </button>

          <button
            className="btn-dark-mode"
            onClick={onToggleDarkMode}
            title="Alternar modo oscuro"
          >
            🌙
          </button>
        </div>
      </div>

      <div className="header-search">
        <input
          type="text"
          className="search-input"
          placeholder="FILTRO DE NOTICIAS - Buscar por palabras clave..."
          value={searchTerm}
          onChange={(e) => onSearch(e.target.value)}
        />
        {searchTerm && (
          <button
            className="clear-search"
            onClick={() => onSearch('')}
            title="Limpiar búsqueda"
          >
            ✕
          </button>
        )}
      </div>
    </header>
  );
}

export default Header;
