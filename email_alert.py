import smtplib
from email.message import EmailMessage
import json

def send_alert(email, topic="IA", articles_file="scored_index.json"):
    with open(articles_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    msg = EmailMessage()
    msg['Subject'] = f"[Veille IA] Nouveaux articles pertinents sur le thème : {topic}"
    msg['From'] = 'tf4632749@gmail.com'
    msg['To'] = email

    body = "Voici les 3 articles les plus pertinents :\n\n"
    count = 0
    for item in list(data.values())[:3]:
        body += f"- {item.get('title', '')}\n  {item.get('summary', '')}\n\n"
        count += 1
    msg.set_content(body)

    # Config SMTP (exemple Gmail)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("f4632749@gmail.com", "lhmyklgypewlefmv")  # mot de passe application
        smtp.send_message(msg)

    print(f"Email envoyé à {email} avec {count} articles.")

# Appel exemple :
# send_alert("destinataire@example.com")
