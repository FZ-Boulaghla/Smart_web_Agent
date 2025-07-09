from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
import json
import os
from pipeline import pipeline
from fastapi.middleware.cors import CORSMiddleware
import traceback

app = FastAPI()
#Autoriser le frontend à accéder à l'API
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
        pipeline(data.query, data.email)
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
def run_pipeline(data: RequestData):
    # Lancer la pipeline
    try:
        pipeline(data.query, data.email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Après pipeline, charger résultats depuis scored_index.json
    results_file = "scored_index.json"
    if not os.path.exists(results_file):
        raise HTTPException(status_code=500, detail="Fichier de résultats introuvable")

    with open(results_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Transformer en liste simplifiée
    results_list = []
    for item in data.values():
        results_list.append({
            "title": item.get("title", "Sans titre"),
            "summary": item.get("summary", item.get("description", "")),
            "url": item.get("url", "")
        })

    return {"results": results_list}
