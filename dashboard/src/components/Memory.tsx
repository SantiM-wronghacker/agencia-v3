import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { searchMemory, MemoryResult } from '../services/dashboardApi';

const Memory: React.FC = () => {
  const [input, setInput] = useState('');
  const [query, setQuery] = useState('');

  const { data: results, isLoading, isFetching, error } = useQuery<MemoryResult[]>({
    queryKey: ['memory', query],
    queryFn: () => searchMemory(query),
    enabled: query.length > 0,
    staleTime: 10000,
  });

  const handleSearch = () => {
    const trimmed = input.trim();
    if (trimmed) setQuery(trimmed);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') handleSearch();
  };

  const formatTimestamp = (ts: string): string => {
    try {
      return new Date(ts).toLocaleString('es-MX', {
        year: 'numeric', month: 'short', day: 'numeric',
        hour: '2-digit', minute: '2-digit',
      });
    } catch {
      return ts;
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
        Memoria histórica
      </h1>
      <p className="text-sm text-gray-500 dark:text-gray-400 mb-6">
        Busca en los outputs de runs anteriores usando búsqueda de texto completo.
      </p>

      {/* Search bar */}
      <div className="flex gap-3 mb-8">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Buscar en observaciones..."
          className="flex-1 rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
        <button
          onClick={handleSearch}
          disabled={!input.trim() || isLoading || isFetching}
          className="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 disabled:cursor-not-allowed text-white text-sm font-medium rounded-md transition-colors flex items-center gap-2"
        >
          {(isLoading || isFetching) ? (
            <>
              <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              Buscando...
            </>
          ) : (
            'Buscar'
          )}
        </button>
      </div>

      {/* Results */}
      {error && (
        <div className="text-red-500 text-sm">
          Error al buscar. ¿Está el servidor corriendo?
        </div>
      )}

      {query && !isLoading && !isFetching && results && results.length === 0 && (
        <div className="text-center py-12 text-gray-400 dark:text-gray-500">
          <p className="text-4xl mb-3">🔍</p>
          <p className="text-sm">Sin resultados para «{query}»</p>
        </div>
      )}

      {results && results.length > 0 && (
        <div className="space-y-4">
          <p className="text-xs text-gray-500 dark:text-gray-400">
            {results.length} resultado{results.length !== 1 ? 's' : ''} para «{query}»
          </p>
          {results.map((item, idx) => (
            <div
              key={idx}
              className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-100 dark:border-gray-700 p-4"
            >
              <div className="flex flex-wrap items-center gap-3 mb-3">
                <span className="text-xs font-medium bg-indigo-50 dark:bg-indigo-900/40 text-indigo-700 dark:text-indigo-300 px-2 py-0.5 rounded font-mono">
                  {item.group_name}
                </span>
                <span className="text-xs text-gray-500 dark:text-gray-400 font-mono">
                  {item.agent_role}
                </span>
                <span className="text-xs text-gray-400 dark:text-gray-500 ml-auto">
                  {formatTimestamp(item.timestamp)}
                </span>
              </div>
              <p className="text-sm text-gray-700 dark:text-gray-300 leading-relaxed">
                {item.content.length > 200
                  ? item.content.slice(0, 200) + '...'
                  : item.content}
              </p>
              <p className="text-xs text-gray-400 dark:text-gray-600 font-mono mt-2">
                run: {item.run_id.slice(0, 8)}...
              </p>
            </div>
          ))}
        </div>
      )}

      {!query && (
        <div className="text-center py-16 text-gray-400 dark:text-gray-500">
          <p className="text-4xl mb-3">🧠</p>
          <p className="text-sm">Escribe un término para buscar en el historial de runs.</p>
        </div>
      )}
    </div>
  );
};

export default Memory;
