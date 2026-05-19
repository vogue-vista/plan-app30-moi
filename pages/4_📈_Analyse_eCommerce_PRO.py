import streamlit as st
from groq import Groq

# 🔒 Sécurité
if "connecte" not in st.session_state or st.session_state.connecte is False:
    st.error("⛔ Accès refusé. Veuillez activer votre licence.")
    st.stop()

st.title("📈 Analyseur de Produits e‑Commerce (IA PRO)")
st.write("Analyse intelligente basée sur l’IA : demande, concurrence, potentiel, viralité et recommandation.")

# 🔑 Clé IA sécurisée
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except:
    st.error("❌ Clé GROQ_API_KEY manquante dans les secrets Streamlit.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# --- Interface ---
mot_cle = st.text_input("Nom du produit à analyser :")

if st.button("Analyser avec IA"):
    if mot_cle.strip() == "":
        st.error("Veuillez entrer un mot-clé.")
    else:
        st.info("⏳ Analyse IA en cours...")

        prompt = f"""
Analyse ce produit pour un e-commerce : {mot_cle}

Donne-moi une analyse complète en format JSON strict :

- Demande estimée (0 à 100)
- Niveau de concurrence (0 à 100)
- Prix moyen du marché
- Niveau de viralité (TikTok, Google Trends)
- Analyse des risques
- Recommandation finale (lancer / tester / éviter)
- Résumé en 3 lignes

Format JSON :
{{
    "demande": "",
    "concurrence": "",
    "prix_moyen": "",
    "viralite": "",
    "risques": "",
    "recommandation": "",
    "resume": ""
}}
"""

        try:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "Tu es un expert en analyse e-commerce."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=600
            )

            reponse = completion.choices[0].message.content

            st.subheader("📊 Résultats IA")
            st.code(reponse)

        except Exception as e:
            st.error(f"Erreur IA : {e}")
