from sentence_transformers import SentenceTransformer, util
import json
import tldextract

def deduplicate_best(input_path="clustered_index.json", output_path="deduplicated_best.json"):
    model = SentenceTransformer('all-MiniLM-L6-v2')

    domain_priority = {
        "openai.com": 10,
        "google.com": 9,
        "wikipedia.org": 8,
        "cisa.gov": 7,
        "nasa.gov": 6,
        "reddit.com": 5,
        "blogspot.com": 2
    }

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    keys = list(data.keys())
    texts = []
    for k in keys:
        text = data[k].get("title", "") + " " + data[k].get("description", "") + " " + data[k].get("ocr_text", "")
        texts.append(text.strip())

    embeddings = model.encode(texts, convert_to_tensor=True)

    groups = []
    visited = set()

    for i in range(len(embeddings)):
        if i in visited:
            continue
        group = [i]
        for j in range(i + 1, len(embeddings)):
            if j in visited:
                continue
            sim = util.cos_sim(embeddings[i], embeddings[j]).item()
            if sim > 0.85:
                group.append(j)
                visited.add(j)
        visited.add(i)
        groups.append(group)

    def get_domain_score(url):
        domain = tldextract.extract(url).registered_domain
        return domain_priority.get(domain, 1)

    filtered_data = {}
    for group in groups:
        best_idx = group[0]
        best_score = data[keys[best_idx]].get("bert_score", 0)
        best_domain = get_domain_score(data[keys[best_idx]].get("url", ""))

        for idx in group[1:]:
            entry = data[keys[idx]]
            score = entry.get("bert_score", 0)
            domain_score = get_domain_score(entry.get("url", ""))

            if score > best_score or (score == best_score and domain_score > best_domain):
                best_idx = idx
                best_score = score
                best_domain = domain_score

        filtered_data[keys[best_idx]] = data[keys[best_idx]]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, indent=2, ensure_ascii=False)

    print(f"Doublons filtrés intelligemment : {len(data)} → {len(filtered_data)} textes retenus.")

if __name__ == "__main__":
    deduplicate_best()
