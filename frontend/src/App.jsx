import React, { useState, useEffect } from 'react';
import './App.css';
import Header from './components/Header';
import SourceList from './components/SourceList';
import NewsFeed from './components/NewsFeed';
import NewsDetail from './components/NewsDetail';

function App() {
  const API_BASE = 'https://notitotal-backend.onrender.com';

  const [news, setNews] = useState([]);
  const [filteredNews, setFilteredNews] = useState([]);
  const [sources, setSources] = useState([]);
  const [selectedSource, setSelectedSource] = useState('todos');
  const [selectedNews, setSelectedNews] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [darkMode, setDarkMode] = useState(localStorage.getItem('darkMode') === 'true');
  const [loading, setLoading] = useState(false);

  // Cargar noticias desde la API
  const fetchNews = async (source = 'all') => {
    try {
      setLoading(true);
      const url = source && source !== 'todos' 
        ? `${API_BASE}/api/news?source=${source}`
        : `${API_BASE}/api/news?source=all`;

      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // IMPORTANTE: Limpiar y establecer nuevas noticias
      const newsList = Array.isArray(data.news) ? data.news : [];
      setNews(newsList);
      
      // Filtrar según búsqueda actual
      filterNews(newsList, searchTerm);
      
    } catch (error) {
      console.error('Error fetching news:', error);
      setNews([]);
      setFilteredNews([]);
    } finally {
      setLoading(false);
    }
  };

  // Cargar fuentes disponibles
  const fetchSources = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/sources`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const sourceList = Array.isArray(data.sources) ? data.sources : [];
      setSources(sourceList);
      
    } catch (error) {
      console.error('Error fetching sources:', error);
      setSources([]);
    }
  };

  // Función para filtrar noticias
  const filterNews = (newsArray = news, search = '') => {
    let filtered = newsArray;

    // Filtrar por fuente
    if (selectedSource && selectedSource !== 'todos') {
      filtered = filtered.filter(item => 
        item.source && item.source.toLowerCase() === selectedSource.toLowerCase()
      );
    }

    // Filtrar por búsqueda
    if (search) {
      const searchLower = search.toLowerCase();
      filtered = filtered.filter(item =>
        (item.title && item.title.toLowerCase().includes(searchLower)) ||
        (item.description && item.description.toLowerCase().includes(searchLower))
      );
    }

    setFilteredNews(filtered);
  };

  // Actualizar cuando cambia la fuente
  useEffect(() => {
    filterNews();
  }, [selectedSource]);

  // Actualizar cuando cambia la búsqueda
  useEffect(() => {
    filterNews(news, searchTerm);
  }, [searchTerm]);

  // Actualizar tema oscuro
  useEffect(() => {
    if (darkMode) {
      document.body.classList.add('dark-mode');
    } else {
      document.body.classList.remove('dark-mode');
    }
    localStorage.setItem('darkMode', darkMode);
  }, [darkMode]);

  // Cargar datos iniciales
  useEffect(() => {
    fetchSources();
    fetchNews();

    // Auto-refresh cada 10 minutos
    const interval = setInterval(() => {
      fetchNews();
    }, 10 * 60 * 1000);

    return () => clearInterval(interval);
  }, []);

  // Cuando hace refresh
  const handleRefresh = async () => {
    setSelectedNews(null);
    await fetchNews();
  };

  // Manejar cambio de fuente
  const handleSourceChange = (source) => {
    setSelectedSource(source);
    setSelectedNews(null);
  };

  // Manejar cambio de búsqueda
  const handleSearch = (term) => {
    setSearchTerm(term);
    setSelectedNews(null);
  };

  // Manejar selección de noticia
  const handleSelectNews = (newsItem) => {
    setSelectedNews(newsItem);
  };

  return (
    <div className="app">
      <Header
        newsCount={filteredNews.length}
        onRefresh={handleRefresh}
        onToggleDarkMode={() => setDarkMode(!darkMode)}
        onSearch={handleSearch}
        searchTerm={searchTerm}
        loading={loading}
      />

      <div className="main-container">
        <div className="column column-1">
          <div className="column-title">FUENTES</div>
          <SourceList
            sources={sources}
            selectedSource={selectedSource}
            onSourceChange={handleSourceChange}
          />
        </div>

        <div className="column column-2">
          <div className="column-title">NOTICIAS ({filteredNews.length})</div>
          <NewsFeed
            news={filteredNews}
            selectedNews={selectedNews}
            onSelectNews={handleSelectNews}
            loading={loading}
          />
        </div>

        <div className="column column-3">
          {selectedNews ? (
            <NewsDetail selectedNews={selectedNews} />
          ) : (
            <div className="empty-detail">
              <p>AL DARLE CLICK A LA NOTICIA</p>
              <p>SE MOSTRARA LA NOTICIA ACA EN SOLO TEXTO</p>
              <p>(NO IMAGENES, VIDEOS, NI PUBLICIDADES)</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
