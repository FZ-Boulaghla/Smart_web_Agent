import React, { useState } from 'react';
import { Search, Sparkles, Mail, X, ExternalLink, Calendar, User } from 'lucide-react';

interface SearchResult {
  title: string;
  url: string;
  snippet: string;
  date: string;
  source: string;
}

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[] | null>(null);
  const [showEmailModal, setShowEmailModal] = useState(false);
  const [email, setEmail] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async () => {
    if (!query.trim()) {
      alert("Veuillez entrer un sujet de recherche");
      return;
    }

    // Demander si l'utilisateur veut recevoir un email
    const wantsEmail = window.confirm("Voulez-vous recevoir les résultats par email ?");
    if (wantsEmail) {
      setShowEmailModal(true);
    } else {
      // Appeler backend sans email
      await callPipelineApi(query);
    }
  };

  const callPipelineApi = async (searchQuery: string, userEmail: string = "") => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch("http://localhost:8000/run-pipeline", {
        method: "POST",
        headers: { 
          "Content-Type": "application/json" 
        },
        body: JSON.stringify({ 
          query: searchQuery, 
          email: userEmail 
        }),
      });

      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }

      const data = await response.json();
      setResults(data.results || []);
      setShowEmailModal(false);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Erreur inconnue";
      setError(`Erreur serveur : ${errorMessage}`);
      console.error("Erreur lors de l'appel API:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleEmailSubmit = async (userEmail: string) => {
    setEmail(userEmail);
    await callPipelineApi(query, userEmail);
  };

  const openEmailModal = () => {
    setShowEmailModal(true);
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-900/20 via-purple-900/10 to-pink-900/20"></div>
      
      {/* Main content */}
      <div className="relative z-10 min-h-screen flex flex-col items-center justify-center p-4">
        <div className="w-full max-w-2xl mx-auto">
          {/* Header */}
          <div className="text-center mb-12">
            <div className="flex items-center justify-center mb-6">
              <div className="p-3 bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl">
                <Sparkles className="w-8 h-8 text-white" />
              </div>
            </div>
            <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-white via-gray-200 to-gray-400 bg-clip-text text-transparent mb-4">
              Agent de Veille Intelligent
            </h1>
            <p className="text-gray-400 text-lg max-w-md mx-auto">
              Découvrez les dernières tendances et informations pertinentes pour votre domaine
            </p>
          </div>

          {/* Search Section */}
          <div className="bg-gray-900/50 backdrop-blur-xl border border-gray-800 rounded-2xl p-8 mb-8 shadow-2xl">
            <div className="space-y-6">
              <div className="relative">
                <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                  placeholder="Entrez votre sujet de recherche..."
                  className="w-full pl-12 pr-4 py-4 bg-gray-800/50 border border-gray-700 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                />
              </div>
              
              <div className="flex gap-3">
                <button
                  onClick={handleSearch}
                  disabled={!query.trim() || isLoading}
                  className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:from-gray-600 disabled:to-gray-700 text-white font-medium py-3 px-6 rounded-xl transition-all duration-200 flex items-center justify-center gap-2 disabled:cursor-not-allowed"
                >
                  {isLoading ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                      Recherche...
                    </>
                  ) : (
                    <>
                      <Search className="w-4 h-4" />
                      Rechercher
                    </>
                  )}
                </button>
                
                <button
                  onClick={openEmailModal}
                  className="bg-gray-800 hover:bg-gray-700 text-white font-medium py-3 px-6 rounded-xl transition-all duration-200 flex items-center gap-2 border border-gray-700"
                >
                  <Mail className="w-4 h-4" />
                  Email
                </button>
              </div>
            </div>
          </div>

          {/* Results Section */}
          {error && (
            <div className="bg-red-900/50 backdrop-blur-xl border border-red-800 rounded-2xl p-6 mb-8 shadow-2xl">
              <div className="flex items-center gap-2 text-red-400">
                <X className="w-5 h-5" />
                <span className="font-medium">Erreur</span>
              </div>
              <p className="text-red-300 mt-2">{error}</p>
              <button
                onClick={() => setError(null)}
                className="mt-4 bg-red-800 hover:bg-red-700 text-white font-medium py-2 px-4 rounded-lg transition-all duration-200"
              >
                Fermer
              </button>
            </div>
          )}

          {results && (
            <div className="bg-gray-900/50 backdrop-blur-xl border border-gray-800 rounded-2xl p-8 shadow-2xl">
              <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
                <Sparkles className="w-6 h-6 text-blue-400" />
                Résultats de recherche
              </h2>
              
              {results.length === 0 ? (
                <div className="text-center py-8">
                  <div className="text-gray-400 mb-2">Aucun résultat trouvé</div>
                  <p className="text-gray-500 text-sm">Essayez avec d'autres mots-clés</p>
                </div>
              ) : (
                <div className="space-y-6">
                  {results.map((result, index) => (
                    <div key={index} className="group p-6 bg-gray-800/30 border border-gray-700/50 rounded-xl hover:bg-gray-800/50 hover:border-gray-600 transition-all duration-200">
                      <div className="flex items-start justify-between mb-3">
                        <h3 className="text-lg font-semibold text-white group-hover:text-blue-400 transition-colors duration-200">
                          <a 
                            href={result.url} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="hover:underline"
                          >
                            {result.title}
                          </a>
                        </h3>
                        <ExternalLink className="w-4 h-4 text-gray-400 group-hover:text-blue-400 transition-colors duration-200 flex-shrink-0 ml-2" />
                      </div>
                      
                      <p className="text-gray-300 mb-4 leading-relaxed">
                        {result.snippet}
                      </p>
                      
                      <div className="flex items-center gap-4 text-sm text-gray-400">
                        {result.source && (
                          <div className="flex items-center gap-1">
                            <User className="w-3 h-3" />
                            {result.source}
                          </div>
                        )}
                        {result.date && (
                          <div className="flex items-center gap-1">
                            <Calendar className="w-3 h-3" />
                            {new Date(result.date).toLocaleDateString('fr-FR')}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Email Modal */}
      {showEmailModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-gray-900 border border-gray-800 rounded-2xl p-8 w-full max-w-md shadow-2xl">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-bold text-white">Recevoir par email</h3>
              <button
                onClick={() => setShowEmailModal(false)}
                className="text-gray-400 hover:text-white transition-colors duration-200"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Adresse email
                </label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="votre@email.com"
                  className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                />
              </div>
              
              <div className="flex gap-3 pt-2">
                <button
                  onClick={() => setShowEmailModal(false)}
                  className="flex-1 bg-gray-800 hover:bg-gray-700 text-white font-medium py-3 px-4 rounded-xl transition-all duration-200 border border-gray-700"
                >
                  Annuler
                </button>
                <button
                  onClick={() => handleEmailSubmit(email)}
                  disabled={!email.trim()}
                  className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:from-gray-600 disabled:to-gray-700 text-white font-medium py-3 px-4 rounded-xl transition-all duration-200 disabled:cursor-not-allowed"
                >
                  Envoyer
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;