import React, { useState } from "react";
import SearchBar from "./components/SearchBar";
import EmailModal from "./components/EmailModal";
import ResultsList from "./components/ResultsList";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState(null);
  const [showEmailModal, setShowEmailModal] = useState(false);
  const [email, setEmail] = useState("");

  const handleSearch = async () => {
    if (!query.trim()) return alert("Veuillez entrer un sujet de recherche");

    // Demander si l'utilisateur veut recevoir un email
    const wantsEmail = window.confirm("Voulez-vous recevoir les résultats par email ?");
    if (wantsEmail) {
      setShowEmailModal(true);
    } else {
      // Appeler backend sans email
      await callPipelineApi(query);
    }
  };

  const callPipelineApi = async (searchQuery, userEmail = "") => {
    try {
      const res = await fetch("http://localhost:8000/run-pipeline", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: searchQuery, email: userEmail }),
      });
      const data = await res.json();
      setResults(data.results);
      setShowEmailModal(false);
    } catch (err) {
      alert("Erreur serveur : " + err.message);
    }
  };

  const handleEmailSubmit = async (userEmail) => {
    setEmail(userEmail);
    await callPipelineApi(query, userEmail);
  };

  return (
    <div className="app-container">
      <div className="main-card">
        <h1>Agent de Veille Intelligent</h1>
        <SearchBar query={query} setQuery={setQuery} onSearch={handleSearch} />
        {results && <ResultsList results={results} />}
        {showEmailModal && <EmailModal onSubmit={handleEmailSubmit} onClose={() => setShowEmailModal(false)} />}
      </div>
    </div>
  );
}

export default App;
