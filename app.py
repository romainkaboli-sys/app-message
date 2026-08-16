import streamlit as st
from client import send_message, send_push_notification

SERVER_URL = "ws://localhost:8765"

st.set_page_config(page_title="Mon Chat App", page_icon="💬", layout="wide")

# Initialisation des variables de session
if "my_username" not in st.session_state:
    st.session_state.my_username = "Romain"

if "messages" not in st.session_state:
    st.session_state.messages = {}

# Choix de l'interlocuteur
selected_name = st.sidebar.text_input("Contact destinataire :", "Alice")

if selected_name not in st.session_state.messages:
    st.session_state.messages[selected_name] = []

st.title(f"💬 Chat avec {selected_name}")

# Affichage des messages
for msg in st.session_state.messages[selected_name]:
    with st.chat_message(msg["role"]):
        st.write(msg["text"])

# Saisie d'un nouveau message
chat_input = st.chat_input(f"Envoyer un message à {selected_name}...")

if chat_input:
    # 1. Ajout local
    st.session_state.messages[selected_name].append({"role": "user", "text": chat_input})

    # 2. Envoi sur le serveur WebSocket
    send_message(SERVER_URL, st.session_state.my_username, selected_name, chat_input)

    # 3. Déclenchement de la notification Push sur le téléphone
    send_push_notification(st.session_state.my_username, chat_input)

    st.rerun()