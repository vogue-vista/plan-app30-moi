import streamlit as st
import requests
from bs4 import BeautifulSoup

# Sécurité
if "connecte" not in st.session_state or st.session_state.connecte is False:
    st.error("⛔ Accès refusé. Veuillez activer votre licence.")
    st.stop()

st.title("🛍️ Scraper Google Shopping (Version 2026)")
st.write("Récupère les prix, vendeurs et titres des produits Google Shopping.")

mot_cle = st.text_input("Produit à rechercher :")

if st.button("Rechercher"):
    if mot_cle.strip() == "":
        st.error("Veuillez entrer un mot-clé.")
    else:
        st.info("⏳ Recherche Google Shopping en cours...")

        query = mot_cle.replace(" ", "+")
        url = f"https://www.google.ca/search?tbm=shop&q={query}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept-Language": "fr-CA,fr;q=0.9"
        }

        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")

        # Nouveau sélecteur universel Google Shopping
        produits = soup.select("div.sh-dgr__grid-result, div.sh-pr__product-results > div")

        if not produits:
            st.error("Aucun résultat trouvé. Google a peut-être changé la structure.")
        else:
            for p in produits[:5]:
                titre = p.select_one("h4, .tAxDx")
                prix = p.select_one(".a8Pemb, .T14wmb")
                vendeur = p.select_one(".aULzUe, .aULzUe span")

                titre = titre.text.strip() if titre else "Sans titre"
                prix = prix.text.strip() if prix else "N/A"
                vendeur = vendeur.text.strip() if vendeur else "N/A"

                st.subheader(titre)
                st.write(f"💰 Prix : {prix}")
                st.write(f"🏪 Vendeur : {vendeur}")
                st.markdown("---")
