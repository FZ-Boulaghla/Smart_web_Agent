from transformers import pipeline
import json

# Charge le modèle préentraîné pour la classification
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

def load_index(path="index.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def annotate_relevance(index, threshold=0.85):
    results = {}
    for key, entry in index.items():
        text = entry.get("title", "") + " " + entry.get("description", "") + " " + entry.get("ocr_text", "")
        prediction = classifier(text[:512])[0]  # BERT limited to 512 tokens
        label = prediction['label']
        score = prediction['score']
        
        entry["bert_label"] = label
        entry["bert_score"] = score
        entry["relevant"] = label == "POSITIVE" and score > threshold
        results[key] = entry
    return results

def save_annotated(results, path="annotated_index.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    index = load_index()
    annotated = annotate_relevance(index)
    save_annotated(annotated)
    print("Annotation terminée. Résultats enregistrés dans annotated_index.json")
