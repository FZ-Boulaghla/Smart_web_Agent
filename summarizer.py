import json
from transformers import pipeline

def summarize_index(input_path="deduplicated_best.json", output_path="summarized_index.json"):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for key, article in data.items():
        # Prendre en priorité le champ le plus complet
        text = article.get("ocr_text") or article.get("description") or article.get("title") or ""
        text = text.strip()
        
        if not text:
            article["summary"] = "Aucun contenu disponible pour générer un résumé."
            continue

        try:
            # Découpe le texte si trop long
            chunk = text[:1024] if len(text) > 1024 else text
            summary = summarizer(chunk)[0]['summary_text']
            article["summary"] = summary
        except Exception as e:
            print(f"Erreur de résumé pour {key} : {e}")
            article["summary"] = "Résumé échoué."

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Résumés générés et enregistrés dans", output_path)


if __name__ == "__main__":
    summarize_index()
