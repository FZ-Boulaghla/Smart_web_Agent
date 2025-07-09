from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
import json
import os
from pipeline import pipeline
from fastapi.middleware.cors import CORSMiddleware
import traceback

app = FastAPI()

# Autoriser le frontend (port 5173) à accéder à l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestData(BaseModel):
    query: str
    email: Optional[EmailStr] = None
@app.post("/run-pipeline")
def run_pipeline(data: RequestData):
    try:
        # Exécution de la pipeline
        pipeline(data.query, data.email)

        # Lecture du fichier de résultats
        results_file = "scored_index.json"
        if not os.path.exists(results_file):
            raise HTTPException(status_code=500, detail="Fichier de résultats introuvable")

        with open(results_file, "r", encoding="utf-8") as f:
            scored_data = json.load(f)

        # Construction de la liste des résultats à envoyer au frontend
        results_list = []

        for item in scored_data.values():
            title = item.get("title")
            url = item.get("url")
            snippet = item.get("summary") or item.get("description")

            # Vérifier que les trois champs sont présents et non vides
            if title and url and snippet:
                results_list.append({
                    "title": title,
                    "snippet": snippet,
                    "url": url,
                    "date": item.get("date", ""),
                    "source": item.get("source", ""),
                    "score": item.get("theme_score", 0)  # Optionnel pour trier ensuite
                })

        # Trier par score (facultatif)
        sorted_results = sorted(results_list, key=lambda x: x["score"], reverse=True)
        top_results = sorted_results[:13]  # ou [:10]

        # Supprimer le champ 'score' s’il n’est pas nécessaire côté frontend
        for r in top_results:
            r.pop("score", None)

        return {"results": top_results}

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
