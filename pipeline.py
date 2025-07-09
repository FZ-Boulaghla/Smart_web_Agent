from main import run_scraping
from bert_classifier import annotate_relevance, save_annotated, load_index
from thematic_classifier import classify_index as classify_themes
from thematic_clustered import cluster_index 
from deduplicate_smart import deduplicate_best 
from summarizer import summarize_index 
from scoring import score_articles
from email_alert import send_alert

def pipeline(query, user_email=None):
    print("\n Étape 1 : Scraping intelligent")
    index = run_scraping(query)
    print(f"Index généré avec {len(index)} entrées")

    print("\n Étape 2 : Classification de pertinence avec BERT")
    index = load_index("index.json")
    annotated = annotate_relevance(index, threshold=0.85)
    save_annotated(annotated, "annotated_index.json")
    save_annotated(annotated, "filtered_bert.json")

    print("\n Étape 3 : Classification thématique supervisée")
    classify_themes("filtered_bert.json", "classified_index.json")

    print("\n Étape 4 : Clustering thématique non supervisé")
    cluster_index("classified_index.json", "clustered_index.json")

    print("\n Étape 5 : Détection et suppression des doublons intelligents")
    deduplicate_best("clustered_index.json", "deduplicated_best.json")

    print("\n Étape 6 : Résumé automatique des articles")
    summarize_index("deduplicated_best.json", "summarized_index.json")

    print("\n Étape 7 : Évaluation qualitative (grammaire, lisibilité, originalité)")
    final_results = score_articles("summarized_index.json", "scored_index.json")

    if user_email:
        print("\n Étape 8 : Envoi de l'alerte par email")
        send_alert(user_email, query, "scored_index.json")
    else:
        print("\n Aucune adresse email fournie. Résultats enregistrés dans scored_index.json")

    print("\n  Pipeline terminé avec succès !\n")

    #  Afficher la liste des articles finaux
    print(" Résultats finaux :\n")
    for idx, article in enumerate(final_results.values(), 1):
        print(f"{idx}. {article.get('title', 'Sans titre')}")
        print(f"   ➤ Résumé : {article.get('summary', '')[:200]}...")
        print(f"   ➤ Thème : {article.get('theme', 'Non défini')} | Score : {round(article.get('theme_score', 0), 2)}")
        print(f"   ➤ Originalité : {round(article.get('originality_score', 0), 2)} | Lisibilité : {round(article.get('readability_score', 0), 2)}\n")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True, help="Sujet de recherche (ex: cybersécurité, IA, etc.)")
    parser.add_argument("--email", required=False, help="Adresse email pour recevoir les résultats")
    args = parser.parse_args()

    pipeline(args.query, args.email)
