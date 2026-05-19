import streamlit as st
import os
from groq import Groq

# 🔒 Sécurité
if "connecte" not in st.session_state or st.session_state.connecte is False:
    st.error("⛔ Accès refusé. Veuillez activer votre licence.")
    st.stop()

st.title("📈 Analyseur de Produits e‑Commerce (IA PRO)")

st.write("Analyse intelligente basée sur l’IA : demande, concurrence, potentiel, viralité et recommandation.")

# Vérification clé API
if "api_key" not in st.session_state or not st.session_state.api_key:
    st.warning("⚠️ Entrez votre clé API IA dans la page principale pour activer l'analyse IA.")
    st.stop()

# Charger la clé API Groq
os.environ["GROQ_API_KEY"] = st.session_state.api_key
client = Groq(api_key=os.environ["GROQ_API_KEY"])

mot_cle = st.text_input("Nom du produit à analyser :")

if st.button("Analyser avec IA"):
    if mot_cle.strip() == "":
        st.error("Veuillez entrer un mot-clé.")
    else:
        st.info("⏳ Analyse IA en cours...")

        prompt = f"""
        Analyse ce produit pour un e-commerce : {mot_cle}

        Donne-moi :
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
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4
            )

            reponse = completion.choices[0].message.content

            st.subheader("📊 Résultats IA")
            st.code(reponse)

        except Exception as e:
            st.error(f"Erreur IA : {e}")
