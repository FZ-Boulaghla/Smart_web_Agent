import json
import textstat
import language_tool_python
from sentence_transformers import SentenceTransformer, util
from tqdm import tqdm

# Charger modèles
#tool = language_tool_python.LanguageTool('en-US') 
model = SentenceTransformer('all-MiniLM-L6-v2')

def score_articles(input_file="summarized_index.json", output_file="scored_index.json"):
    # Chargement du fichier
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    all_texts = [item.get("summary", "") for item in data.values()]
    print(f"Total de résumés : {len(all_texts)}")

    # Pré-calcul des embeddings
    print("Encodage des textes...")
    embeddings = {
        text: model.encode(text, convert_to_tensor=True)
        for text in tqdm(all_texts, desc="Encodage")
    }

    # Traitement avec barre de progression
    for key, item in tqdm(data.items(), desc="Évaluation"):
        summary = item.get("summary", "")
        if not summary.strip():
            continue

        # Score lisibilité
        readability = textstat.flesch_reading_ease(summary)

        # Optionnel : vérifier la grammaire
        try:
            grammar_issues = len(tool.check(summary)) 
        except Exception:
            grammar_issues = -1  # Erreur silencieuse

        # Originalité : calcul de similarité avec les autres résumés
        emb = embeddings[summary]
        other_embs = [e for t, e in embeddings.items() if t != summary]

        similarities = [util.cos_sim(emb, other).item() for other in other_embs]
        originality_score = 1 - max(similarities) if similarities else 1

        # Ajouter les scores
        item["readability_score"] = readability
        item["grammar_issues"] = grammar_issues
        item["originality_score"] = originality_score

    # Sauvegarde des résultats
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f" Scoring terminé : résultats dans {output_file}")
    
    # Retourner la liste des articles traités
    return data

if __name__ == "__main__":
    # Récupérer les articles finaux
    final_articles = score_articles()

    # Si tu veux les afficher ou les utiliser après
    print(final_articles[:5])  # Affiche les 5 premiers articles traités
