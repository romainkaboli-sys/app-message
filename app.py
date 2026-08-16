from flask import Flask, render_template_string, request
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

EXPEDITEUR_EMAIL = "romainkaboli@gmail.com"
MOT_DE_PASSE = "rftk eyku osew xysu" # Ton mot de passe d'application Google à 16 lettres

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Messagerie PC</title>
    <style>
        body { font-family: Arial, sans-serif; background: #121212; color: white; padding: 20px; text-align: center; }
        textarea { width: 90%; height: 120px; border-radius: 8px; border: 1px solid #333; padding: 10px; background: #1e1e1e; color: white; font-size: 16px; }
        button { background: #007bff; color: white; border: none; padding: 12px 20px; font-size: 16px; border-radius: 8px; margin-top: 15px; width: 95%; cursor: pointer; }
    </style>
</head>
<body>
    <h2>💬 Envoyer un message</h2>
    <form method="POST">
        <textarea name="message" placeholder="Écris ton message ici..."></textarea><br>
        <button type="submit">Envoyer</button>
    </form>
    <p>{{ status }}</p>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    status = ""
    if request.method == 'POST':
        msg_text = request.form.get('message')
        if msg_text:
            msg = MIMEText(msg_text, _charset='utf-8')
            msg['Subject'] = "💬 Nouveau Message Web"
            msg['From'] = EXPEDITEUR_EMAIL
            msg['To'] = EXPEDITEUR_EMAIL
            try:
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.login(EXPEDITEUR_EMAIL, MOT_DE_PASSE)
                server.sendmail(EXPEDITEUR_EMAIL, [EXPEDITEUR_EMAIL], msg.as_string())
                server.quit()
                status = "✅ Message envoyé !"
            except Exception as e:
                status = f"❌ Erreur : {e}"
    return render_template_string(HTML_TEMPLATE, status=status)

if __name__ == '__main__':
    app.run()
