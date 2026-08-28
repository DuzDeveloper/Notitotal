import React, { useState, useEffect } from 'react';
import './App.css';
import Header from './components/Header';
import SourceList from './components/SourceList';
import NewsFeed from './components/NewsFeed';
import NewsDetail from './components/NewsDetail';

function App() {
  // Estados principales
  const [news, setNews] = useState([]);
  const [filteredNews, setFilteredNews] = useState([]);
  const [selectedSource, setSelectedSource] = useState('Todos');
  const [selectedNews, setSelectedNews] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [darkMode, setDarkMode] = useState(localStorage.getItem('darkMode') === 'true');
  const [loading, setLoading] = useState(false);
  const [sources, setSources] = useState(['Todos']);
  const [newsCount, setNewsCount] = useState(0);

  const API_BASE = 'https://notitotal-backend.onrender.com';

  // Cargar noticias al montar y cuando cambia el filtro
  useEffect(() => {
    fetchNews();
    fetchSources();
    
    // Refresh automático cada 2 minutos
    const interval = setInterval(fetchNews, 120000);
    return () => clearInterval(interval);
  }, []);

  // Aplicar filtros cuando cambien
  useEffect(() => {
    applyFilters();
  }, [selectedSource, searchTerm, news]);

  // Guardar preferencia de tema
  useEffect(() => {
    localStorage.setItem('darkMode', darkMode);
    document.body.classList.toggle('dark-mode', darkMode);
  }, [darkMode]);

  // Fetch de noticias
  const fetchNews = async () => {
    setLoading(true);
    try {
      const url = new URL(`${API_BASE}/api/news`);
      url.searchParams.append('source', selectedSource === 'Todos' ? 'all' : selectedSource);
      
      const response = await fetch(url);
      const data = await response.json();
      
      if (data.status === 'success') {
        setNews(data.news);
        setNewsCount(data.count);
      }
    } catch (error) {
      console.error('Error fetching news:', error);
    } finally {
      setLoading(false);
    }
  };

  // Fetch de fuentes
  const fetchSources = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/sources`);
      const data = await response.json();
      
      if (data.status === 'success') {
        setSources(data.sources);
      }
    } catch (error) {
      console.error('Error fetching sources:', error);
    }
  };

  // Aplicar filtros de búsqueda
  const applyFilters = () => {
    let filtered = [...news];

    // Filtro por fuente
    if (selectedSource !== 'Todos') {
      filtered = filtered.filter(item => item.source === selectedSource);
    }

    // Filtro por búsqueda
    if (searchTerm) {
      const searchLower = searchTerm.toLowerCase();
      filtered = filtered.filter(item =>
        item.title.toLowerCase().includes(searchLower) ||
        item.description?.toLowerCase().includes(searchLower)
      );
    }

    setFilteredNews(filtered);
  };

  // Refresh manual
  const handleRefresh = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/api/refresh`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      
      if (response.ok) {
        await fetchNews();
      }
    } catch (error) {
      console.error('Error refreshing news:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`app ${darkMode ? 'dark-mode' : 'light-mode'}`}>
      <Header
        newsCount={newsCount}
        onRefresh={handleRefresh}
        onToggleDarkMode={() => setDarkMode(!darkMode)}
        onSearch={setSearchTerm}
        searchTerm={searchTerm}
        loading={loading}
      />

      <div className="main-container">
        {/* Columna 1: Fuentes */}
        <SourceList
          sources={sources}
          selectedSource={selectedSource}
          onSourceSelect={(source) => {
            setSelectedSource(source);
            setSelectedNews(null);
          }}
        />

        {/* Columna 2: Feed de Noticias */}
        <NewsFeed
          news={filteredNews}
          selectedNews={selectedNews}
          onSelectNews={setSelectedNews}
          loading={loading}
        />

        {/* Columna 3: Detalle de Noticia */}
        <NewsDetail
          news={selectedNews}
          darkMode={darkMode}
        />
      </div>
    </div>
  );
}

export default App;
