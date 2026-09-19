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
      
      // Construir URL correctamente
      let url = `${API_BASE}/api/news`;
      if (source && source !== 'todos' && source !== 'all') {
        url += `?source=${encodeURIComponent(source)}`;
      } else {
        url += '?source=all';
      }

      console.log('Fetching from:', url); // Debug

      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        console.error('HTTP error! status:', response.status);
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('API Response:', data); // Debug
      
      // Asegurarse de que news es un array
      const newsList = Array.isArray(data.news) ? data.news : (data || []);
      
      console.log('Setting news array with', newsList.length, 'items'); // Debug
      
      setNews(newsList);
      setSelectedNews(null);
      
      // Filtrar con los nuevos datos
      applyFilters(newsList, selectedSource, searchTerm);
      
    } catch (error) {
      console.error('Error fetching news:', error);
      setNews([]);
      setFilteredNews([]);
    } finally {
      setLoading(false);
    }
  };

  // Nueva función para aplicar filtros
  const applyFilters = (newsArray, sourceFilter = selectedSource, searchFilter = searchTerm) => {
    let filtered = newsArray;

    console.log('Applying filters - Total news:', newsArray.length);

    // Filtrar por fuente
    if (sourceFilter && sourceFilter !== 'todos') {
      filtered = filtered.filter(item => {
        const itemSource = item.source ? item.source.toLowerCase() : '';
        const filterSource = sourceFilter.toLowerCase();
        return itemSource === filterSource || itemSource.includes(filterSource);
      });
      console.log('After source filter:', filtered.length);
    }

    // Filtrar por búsqueda
    if (searchFilter && searchFilter.trim()) {
      const searchLower = searchFilter.toLowerCase();
      filtered = filtered.filter(item =>
        (item.title && item.title.toLowerCase().includes(searchLower)) ||
        (item.description && item.description.toLowerCase().includes(searchLower))
      );
      console.log('After search filter:', filtered.length);
    }

    console.log('Final filtered count:', filtered.length);
    setFilteredNews(filtered);
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
          <NewsDetail selectedNews={selectedNews} />
        </div>
          ) : (
            <div className="empty-detail">
              <p>VACIO</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
