import React, { useState } from 'react';
import './NewsDetail.css';

function NewsDetail({ selectedNews }) {
  const [copied, setCopied] = useState(false);

  if (!selectedNews) {
    return (
      <div className="column-3">
        <div className="empty-detail">
          <p>AL DARLE CLICK A LA NOTICIA</p>
          <p>SE MOSTRARA LA NOTICIA ACA EN SOLO TEXTO</p>
          <p>(NO IMAGENES, VIDEOS, NI PUBLICIDADES)</p>
        </div>
      </div>
    );
  }

  const handleCopy = () => {
    const textToCopy = `${selectedNews.title}\n\n${selectedNews.content || selectedNews.description}`;
    navigator.clipboard.writeText(textToCopy).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  return (
    <div className="column-3">
      <div className="detail-header">
        <h2 className="detail-title">{selectedNews.title}</h2>
        <button 
          className="btn-copy" 
          onClick={handleCopy}
          title={copied ? '¡Copiado!' : 'Copiar contenido'}
        >
          {copied ? '✓ Copiado' : '📋 Copiar'}
        </button>
      </div>

      <div className="detail-meta">
        <div className="meta-item">
          <strong>Fuente:</strong> {selectedNews.source}
        </div>
        <div className="meta-item">
          <strong>Fecha:</strong> {selectedNews.published_at}
        </div>
        <div className="meta-item">
          <strong>Autor:</strong> {selectedNews.author || selectedNews.source}
        </div>
      </div>

      <div className="detail-content">
        {selectedNews.description && (
          <div className="detail-description">{selectedNews.description}</div>
        )}
        
        {selectedNews.content && (
          <div className="detail-text">{selectedNews.content}</div>
        )}

        {selectedNews.source_url && (
          <a 
            href={selectedNews.source_url} 
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
