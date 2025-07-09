from transformers import pipeline
import json
from tqdm import tqdm

# Chargement du modèle zero-shot (restera sur CPU sauf si tu as un GPU et tu précises device=0)
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

candidate_labels = [
    "intelligence artificielle", "cybersecurity", "sante",
    "politique", "ecologie", "finance", "education"
]

def classify_index(input_path="annotated_index.json", output_path="classified_index.json", batch_size=8):
    # Charger les données du fichier JSON
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    keys = list(data.keys())
    texts = [
        data[k].get("title", "") + " " + data[k].get("description", "") + " " + data[k].get("ocr_text", "")
        for k in keys
    ]

    # Classification par batchs
    for i in tqdm(range(0, len(texts), batch_size), desc="Classification thématique"):
        batch_texts = texts[i:i + batch_size]
        batch_keys = keys[i:i + batch_size]

        results = classifier(batch_texts, candidate_labels)

        # Si un seul élément, results sera un dict
        if isinstance(results, dict):
            results = [results]

        for j, result in enumerate(results):
            theme = result["labels"][0]
            confidence = result["scores"][0]
            k = batch_keys[j]
            data[k]["theme"] = theme
            data[k]["theme_score"] = confidence

    # Écrire les résultats dans le fichier de sortie
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    classify_index()
