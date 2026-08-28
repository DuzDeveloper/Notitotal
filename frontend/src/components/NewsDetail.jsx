import React, { useState } from 'react';
import './NewsDetail.css';

function NewsDetail({ news, darkMode }) {
  const [copied, setCopied] = useState(false);

  const handleCopyContent = () => {
    if (news) {
      const textToCopy = `${news.title}\n\n${news.content || news.description}`;
      navigator.clipboard.writeText(textToCopy);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  if (!news) {
    return (
      <div className="column column-3">
        <div className="empty-detail">
          <p>AL DARLE CLICK A LA NOTICIA</p>
          <p>SE MOSTRARA LA NOTICIA ACA EN SOLO TEXTO</p>
          <p>(NO IMAGENES , VIDEOS , NI PUBLICIDADES)</p>
        </div>
      </div>
    );
  }

  return (
    <div className="column column-3">
      <div className="detail-header">
        <h2 className="detail-title">{news.title}</h2>
        <button
          className="btn-copy"
          onClick={handleCopyContent}
          title="Copiar contenido"
        >
          {copied ? '✓ Copiado' : '📋 Copiar'}
        </button>
      </div>

      <div className="detail-meta">
        <div className="meta-item">
          <strong>Fuente:</strong> {news.source}
        </div>
        <div className="meta-item">
          <strong>Fecha:</strong> {new Date(news.published_at).toLocaleString('es-ES')}
        </div>
        {news.author && (
          <div className="meta-item">
            <strong>Autor:</strong> {news.author}
          </div>
        )}
      </div>

      <div className="detail-content">
        <p className="detail-description">
          {news.description}
        </p>

        {news.content && (
          <div className="detail-text">
            {news.content}
          </div>
        )}

        {news.source_url && (
          <a
            href={news.source_url}
            target="_blank"
            rel="noopener noreferrer"
            className="btn-original-link"
          >
            → Ver artículo original
          </a>
        )}
      </div>

      <div className="copy-hint">
        💡 Haz click en "Copiar" para llevar el texto a tu portapapeles para videos
      </div>
    </div>
  );
}

export default NewsDetail;
