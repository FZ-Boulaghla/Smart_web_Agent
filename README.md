# 🧠 Agent Intelligent de Veille Web Automatisée

Un système complet de veille web automatisée intégrant du scraping, de l’analyse NLP, de la classification par BERT, du clustering thématique, du résumé automatique,et un système de notification par e-mail.

---

## 📌 Fonctionnalités principales

- 🔍 Recherche Google Custom Search (API)
- 🧹 Nettoyage des liens et scraping (HTML + OCR visuel avec Selenium)
- 🤖 Classification de pertinence (BERT)
- 🏷️ Classification thématique (Zero-shot avec BART)
- 🧠 Clustering sémantique (KMeans + SentenceTransformer)
- 🧼 Suppression intelligente des doublons
- ✂️ Résumé automatique des contenus
- 📊 Scoring linguistique (lisibilité, grammaire, originalité)
- 📬 Notification automatique par e-mail
- 🌐 API FastAPI pour déclencher l’analyse depuis une interface web

---

## ⚙️ Installation

### 1. Cloner le projet

```bash
git clone https://github.com/FZ-Boulaghla/Smart_web_Agent.git
```
 ### 2. En ligne de commande (CLI)
 ```
python pipeline.py --query "cybersecurity" --email "destinataire@example.com"
```
### 3. Via l’API (FastAPI)
```
python -m uvicorn backend:app --reload --host 0.0.0.0
POST → http://localhost:8000/run-pipeline

Payload JSON :
{
  "query": "cybersecurity",
  "email": "destinataire@example.com"
}
```
