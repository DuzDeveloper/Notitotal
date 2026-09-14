import React from 'react';
import './SourceList.css';

function SourceList({ sources, selectedSource, onSourceChange }) {
  return (
    <div className="sources-container">
      <button
        className={`source-btn ${selectedSource === 'todos' ? 'active' : ''}`}
        onClick={() => onSourceChange('todos')}
      >
        Todos
      </button>

      {sources && sources.length > 0 && sources.map((source) => (
        <button
          key={source}
          className={`source-btn ${selectedSource === source ? 'active' : ''}`}
          onClick={() => onSourceChange(source)}
        >
          {source}
        </button>
      ))}
    </div>
  );
}

export default SourceList;
