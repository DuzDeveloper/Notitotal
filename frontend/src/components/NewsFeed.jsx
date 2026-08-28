import React from 'react';
import './NewsFeed.css';

function NewsFeed({ news, selectedNews, onSelectNews, loading }) {
  const formatTime = (dateString) => {
    try {
      const date = new Date(dateString);
      const now = new Date();
      const diffMs = now - date;
      const diffMins = Math.floor(diffMs / 60000);
      
      if (diffMins < 60) return `hace ${diffMins}m`;
      const diffHours = Math.floor(diffMins / 60);
      if (diffHours < 24) return `hace ${diffHours}h`;
      const diffDays = Math.floor(diffHours / 24);
      return `hace ${diffDays}d`;
    } catch (e) {
      return 'Hace poco';
    }
  };

  return (
    <div className="column column-2">
      <h2 className="column-title">NOTICIAS ({news.length})</h2>
      
      {loading && <div className="loading-spinner">Cargando...</div>}
      
      <div className="news-feed">
        {news.length === 0 ? (
          <div className="empty-state">
            <p>No hay noticias disponibles</p>
            <p className="empty-hint">Haz click en una fuente o usa el botón Refresh</p>
          </div>
        ) : (
          news.map((item, index) => (
            <div
              key={`${item.source}-${index}`}
              className={`news-card ${selectedNews?.source === item.source && selectedNews?.title === item.title ? 'selected' : ''}`}
              onClick={() => onSelectNews(item)}
            >
              {item.image_url && (
                <div className="news-image-container">
                  <img
                    src={item.image_url}
                    alt={item.title}
                    className="news-image"
                    onError={(e) => {
                      e.target.style.display = 'none';
                    }}
                  />
                </div>
              )}
              
              <div className="news-card-content">
                <h3 className="news-title">{item.title}</h3>
                
                <p className="news-description">
                  {item.description || item.content || 'Sin descripción'}
                </p>
                
                <div className="news-meta">
                  <span className="news-source">{item.source}</span>
                  <span className="news-time">{formatTime(item.published_at)}</span>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default NewsFeed;
