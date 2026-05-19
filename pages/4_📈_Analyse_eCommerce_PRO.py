import streamlit as st
import random

st.title("📈 Analyseur de Produits e‑Commerce (PRO)")

st.write("Analyse la demande, la concurrence et la rentabilité potentielle d’un produit.")

mot_cle = st.text_input("Nom du produit à analyser :")

if st.button("Analyser le marché"):
    if mot_cle.strip() == "":
        st.error("Veuillez entrer un mot-clé.")
    else:
        st.success(f"Analyse complète du marché pour : **{mot_cle}**")

        # Simulations réalistes (tu pourras remplacer par scraping + IA)
        demande = random.randint(40, 95)
        concurrence = random.randint(20, 90)
        prix_moyen = random.randint(10, 120)
        viralite = random.randint(10, 100)

        st.subheader("📊 Résultats de l'analyse")
        st.write(f"🔎 **Demande estimée :** {demande}/100")
        st.write(f"⚔️ **Concurrence :** {concurrence}/100")
        st.write(f"💰 **Prix moyen du marché :** {prix_moyen} $")
        st.write(f"🔥 **Viralité estimée :** {viralite}/100")

        score_final = demande - concurrence + (viralite // 2)

        st.subheader("🧠 Recommandation IA (logique métier)")
        if score_final > 70:
            st.success("🔥 Excellent produit à lancer ! Forte demande et concurrence raisonnable.")
        elif score_final > 40:
            st.warning("🟡 Produit correct, mais nécessite une stratégie marketing solide.")
        else:
            st.error("❌ Produit risqué : faible potentiel ou marché saturé.")

        st.info("💡 Prochaine étape possible : brancher une vraie IA + données réelles (Amazon, Google Trends, etc.).")
