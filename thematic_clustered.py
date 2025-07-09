from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import json

def cluster_index(input_path="classified_index.json", output_path="clustered_index.json", num_clusters=5):
    model = SentenceTransformer('all-MiniLM-L6-v2')  # Embedding léger
    texts = []

    # Charger les données
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Préparer les textes à encoder
    for item in data.values():
        text = item.get("title", "") + " " + item.get("description", "")
        texts.append(text)

    # Calcul des embeddings
    embeddings = model.encode(texts)

    # Clustering KMeans
    clustering_model = KMeans(n_clusters=num_clusters, random_state=42)
    clustering_model.fit(embeddings)
    cluster_assignment = clustering_model.labels_

    # Ajouter l'attribution des clusters aux données
    for idx, key in enumerate(data.keys()):
        data[key]["cluster"] = int(cluster_assignment[idx])

    # Sauvegarder les résultats
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f" Textes regroupés en {num_clusters} clusters.")

if __name__ == "__main__":
    cluster_index()
