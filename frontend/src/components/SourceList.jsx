import React from 'react';
import './SourceList.css';

function SourceList({ sources, selectedSource, onSourceSelect }) {
  return (
    <div className="column column-1">
      <h2 className="column-title">FUENTES</h2>
      <div className="sources-container">
        {sources.map((source) => (
          <button
            key={source}
            className={`source-btn ${selectedSource === source ? 'active' : ''}`}
            onClick={() => onSourceSelect(source)}
          >
            {source}
          </button>
        ))}
      </div>
    </div>
  );
}

export default SourceList;
