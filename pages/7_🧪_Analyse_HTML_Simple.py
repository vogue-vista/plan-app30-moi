import streamlit as st
from bs4 import BeautifulSoup

st.title("🧪 Analyse HTML Simple")
st.write("Colle ici du HTML et je vais essayer d'extraire le titre, le prix et le vendeur.")

html_input = st.text_area("Colle ton HTML ici :", height=300)

if st.button("Analyser"):
    if not html_input.strip():
        st.error("❌ Colle du HTML d'abord.")
    else:
        soup = BeautifulSoup(html_input, "html.parser")

        # Extraction simple
        titre = soup.find(["h1", "h2", "h3"])
        prix = soup.find(string=lambda x: "$" in x if x else False)
        vendeur = soup.find(string=lambda x: "Walmart" in x or "Amazon" in x or "Best Buy" in x if x else False)

        st.subheader("📌 Résultats trouvés")

        st.write("**Titre :**", titre.text.strip() if titre else "Non trouvé")
        st.write("**Prix :**", prix.strip() if prix else "Non trouvé")
        st.write("**Vendeur :**", vendeur.strip() if vendeur else "Non trouvé")
