import React from 'react';
import './SourceList.css';

function SourceList({ sources, selectedSource, onSourceChange }) {
  // Las fuentes ya vienen limpias del backend (solo Goal y Marca)
  // No hacer nada especial, solo mostrar lo que el backend envía
  
  if (!sources || sources.length === 0) {
    return (
      <div className="sources-container">
        <button className="source-btn active">Todos</button>
        <button className="source-btn">Goal</button>
        <button className="source-btn">Marca</button>
      </div>
    );
  }

  return (
    <div className="sources-container">
      {sources.map((source) => (
        <button
          key={source}
          className={`source-btn ${selectedSource === source || (selectedSource === 'todos' && source === 'Todos') ? 'active' : ''}`}
          onClick={() => onSourceChange(source === 'Todos' ? 'todos' : source)}
        >
          {source}
        </button>
      ))}
    </div>
  );
}

export default SourceList;