import React from 'react';
import './SourceList.css';

function SourceList({ sources, selectedSource, onSourceChange }) {
  // Asegurarse que "Todos" esté al inicio
  let sourceList = [];
  
  if (sources && sources.length > 0) {
    // Si "Todos" ya está en la lista, no lo duplicar
    if (!sources.includes('Todos')) {
      sourceList = ['Todos', ...sources];
    } else {
      sourceList = sources;
    }
  } else {
    sourceList = ['Todos'];
  }

  return (
    <div className="sources-container">
      {sourceList.map((source) => (
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
