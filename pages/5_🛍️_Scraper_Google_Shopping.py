import streamlit as st
import requests
from bs4 import BeautifulSoup

# Sécurité
if "connecte" not in st.session_state or st.session_state.connecte is False:
    st.error("⛔ Accès refusé. Veuillez activer votre licence.")
    st.stop()

st.title("🛍️ Scraper Google Shopping")
st.write("Récupère les prix, vendeurs et titres des produits Google Shopping.")

mot_cle = st.text_input("Produit à rechercher :")

if st.button("Rechercher"):
    if mot_cle.strip() == "":
        st.error("Veuillez entrer un mot-clé.")
    else:
        st.info("⏳ Recherche Google Shopping en cours...")

        query = mot_cle.replace(" ", "+")
        url = f"https://www.google.com/search?tbm=shop&q={query}"

        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")

        produits = soup.select(".sh-dgr__content")

        if not produits:
            st.error("Aucun résultat trouvé.")
        else:
            for p in produits[:5]:
                titre = p.select_one(".tAxDx").text if p.select_one(".tAxDx") else "Sans titre"
                prix = p.select_one(".a8Pemb").text if p.select_one(".a8Pemb") else "N/A"
                vendeur = p.select_one(".aULzUe").text if p.select_one(".aULzUe") else "N/A"

                st.subheader(titre)
                st.write(f"💰 Prix : {prix}")
                st.write(f"🏪 Vendeur : {vendeur}")
                st.markdown("---")
