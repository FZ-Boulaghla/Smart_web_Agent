import smtplib
from email.message import EmailMessage
import json

def send_alert(email, topic="IA", articles_file="scored_index.json"):
    with open(articles_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    msg = EmailMessage()
    msg['Subject'] = f"Nouveaux articles pertinents sur le thème : {topic}"
    msg['From'] = 'f4632749@gmail.com'
    msg['To'] = email

    # Construction de la liste comme dans le frontend
    results_list = []

    for item in data.values():
        title = item.get("title")
        url = item.get("url")
        snippet = item.get("summary") or item.get("description")

        if title and url and snippet:
            results_list.append({
                "title": title,
                "snippet": snippet,
                "url": url,
                "score": item.get("theme_score", 0)
            })

    # Trier par score décroissant et prendre les 3 meilleurs
    sorted_results = sorted(results_list, key=lambda x: x["score"], reverse=True)[:3]

    # Préparation du contenu de l’email
    body = "Voici les 3 articles les plus pertinents :\n\n"
    for item in sorted_results:
        body += f"- {item['title']}\n  {item['snippet']}\n  🔗 {item['url']}\n\n"

    msg.set_content(body)

    # Envoi via Gmail SMTP
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("f4632749@gmail.com", "lhmyklgypewlefmv")  # Utilise un mot de passe d'application sécurisé
        smtp.send_message(msg)

    print(f"📬 Email envoyé à {email} avec {len(sorted_results)} articles.")
