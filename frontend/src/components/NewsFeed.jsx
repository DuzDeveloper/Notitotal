import React from 'react';
import './NewsFeed.css';

function NewsFeed({ news, selectedNews, onSelectNews, loading }) {
  if (loading) {
    return (
      <div className="news-feed">
        <div className="loading-spinner">Cargando noticias...</div>
      </div>
    );
  }

  if (!news || news.length === 0) {
    return (
      <div className="news-feed">
        <div className="empty-state">
          <p>No hay noticias disponibles</p>
          <p className="empty-hint">Haz click en Refresh o cambia de fuente</p>
        </div>
      </div>
    );
  }

  return (
    <div className="news-feed">
      {news.map((newsItem, index) => (
        <div
          key={`${newsItem.source}-${index}`}
          className={`news-card ${selectedNews && selectedNews.source === newsItem.source && selectedNews.title === newsItem.title ? 'selected' : ''}`}
          onClick={() => onSelectNews(newsItem)}
        >
          {newsItem.image_url && (
            <div className="news-image-container">
              <img
                src={newsItem.image_url}
                alt={newsItem.title}
                className="news-image"
                onError={(e) => {
                  e.target.style.display = 'none';
                }}
              />
            </div>
          )}

          <div className="news-card-content">
            <div className="news-title">{newsItem.title}</div>
            <div className="news-description">{newsItem.description}</div>
            <div className="news-meta">
              <span className="news-source">{newsItem.source}</span>
              <span className="news-time">{newsItem.published_at}</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default NewsFeed;
