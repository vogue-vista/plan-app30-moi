import streamlit as st
from groq import Groq

# 🔒 Sécurité : accès réservé aux sessions activées
if "connecte" not in st.session_state or st.session_state.connecte is False:
    st.error("⛔ Accès refusé. Veuillez activer votre licence pour utiliser cet outil.")
    st.stop()

st.title("💼 Générateur de Réponses Professionnelles (IA PRO)")
st.write("Générez automatiquement des réponses professionnelles, personnalisées et adaptées au contexte du message client.")

# 🔑 Clé IA sécurisée
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=GROQ_API_KEY)
except:
    client = None
    st.error("❌ Clé GROQ_API_KEY manquante dans les secrets Streamlit.")
    st.stop()

# --- Interface ---
message = st.text_area("Message reçu du client :")
ton = st.selectbox("Ton de la réponse", ["Professionnel", "Amical", "Empathique", "Ferme mais poli", "Luxe", "SAV Premium"])

if st.button("Générer une réponse professionnelle"):
    if message.strip() == "":
        st.error("Veuillez entrer un message.")
    else:
        prompt = f"""
Tu es un expert du service client e-commerce.

Analyse ce message client et génère une réponse professionnelle, claire et adaptée.

Message du client :
\"\"\"{message}\"\"\"

Ton demandé : {ton}

Ta réponse doit :
- être polie et professionnelle
- rassurer le client
- proposer une action concrète (ex : vérifier commande, demander numéro, etc.)
- être courte et efficace
- ne jamais inventer d'informations
- rester 100% réaliste

Donne uniquement la réponse finale, pas d'explications.
"""

        try:
            chat = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "Tu es un expert en service client e-commerce."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=400
            )

            reponse = chat.choices[0].message.content

            st.subheader("✉️ Réponse générée")
            st.code(reponse)

        except Exception as e:
            st.error(f"Erreur IA : {e}")

