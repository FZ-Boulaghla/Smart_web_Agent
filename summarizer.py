import json
from transformers import pipeline

def summarize_index(input_path="deduplicated_best.json", output_path="summarized_index.json"):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for key, article in data.items():
        text = article.get("content", "")
        if len(text.strip()) > 30:
            try:
                summary = summarizer(text[:1024])[0]['summary_text']
                article["summary"] = summary
            except Exception as e:
                print(f"Erreur de résumé pour {key} : {e}")
                article["summary"] = "Résumé échoué."
        else:
            article["summary"] = "Texte trop court pour résumé."

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Résumés générés et enregistrés dans", output_path)


if __name__ == "__main__":
    summarize_index()
