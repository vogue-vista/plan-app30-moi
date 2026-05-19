import streamlit as st
from bs4 import BeautifulSoup
from groq import Groq

# 🔒 Sécurité
if "connecte" not in st.session_state or st.session_state.connecte is False:
    st.error("⛔ Accès refusé. Veuillez activer votre licence.")
    st.stop()

st.title("🧪 Analyse HTML IA (Version PRO)")
st.write("Colle du HTML et laisse l'IA analyser automatiquement le contenu.")

# 🔑 Clé IA sécurisée
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=GROQ_API_KEY)
except:
    st.error("❌ Clé GROQ_API_KEY manquante dans les secrets Streamlit.")
    st.stop()

html_input = st.text_area("Colle ton HTML ici :", height=300)

def extract_basic_info(html):
    soup = BeautifulSoup(html, "html.parser")

    # Titre
    titre = soup.find(["h1", "h2", "h3"])
    titre = titre.text.strip() if titre else "Non trouvé"

    # Prix
    prix = soup.find(string=lambda x: "$" in x if x else False)
    prix = prix.strip() if prix else "Non trouvé"

    # Vendeur
    vendeur = soup.find(string=lambda x: any(v in x for v in ["Walmart", "Amazon", "Best Buy", "Etsy"]) if x else False)
    vendeur = vendeur.strip() if vendeur else "Non trouvé"

    # Paragraphes
    paragraphs = [p.text.strip() for p in soup.find_all("p") if p.text.strip()][:5]

    # Images
    images = [img.get("src") for img in soup.find_all("img") if img.get("src")][:5]

    return titre, prix, vendeur, paragraphs, images

def analyse_ia(titre, prix, vendeur, paragraphs):
    texte = "\n".join(paragraphs)

    prompt = f"""
Analyse ce code HTML et génère une analyse complète.

Données extraites :
- Titre : {titre}
- Prix : {prix}
- Vendeur : {vendeur}
- Contenu : {texte}

Donne :
1. Un résumé clair du produit ou de la page
2. Une analyse e-commerce (prix, crédibilité, vendeur)
3. Une analyse SEO rapide
4. Une recommandation pour améliorer la page
5. Une estimation du type de page (fiche produit, article, blog, etc.)
"""

    chat = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Tu es un expert en analyse web, SEO et e-commerce."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=600
    )

    return chat.choices[0].message.content

if st.button("Analyser"):
    if not html_input.strip():
        st.error("❌ Colle du HTML d'abord.")
    else:
        titre, prix, vendeur, paragraphs, images = extract_basic_info(html_input)

        st.subheader("📌 Informations extraites automatiquement")
        st.write(f"**Titre :** {titre}")
        st.write(f"**Prix :** {prix}")
        st.write(f"**Vendeur :** {vendeur}")

        st.write("**Paragraphes détectés :**")
        for p in paragraphs:
            st.write("- " + p)

        if images:
            st.write("**Images détectées :**")
            for img in images:
                st.write(img)

        st.markdown("---")
        st.subheader("🧠 Analyse IA complète")

        try:
            analyse = analyse_ia(titre, prix, vendeur, paragraphs)
            st.write(analyse)
        except Exception as e:
            st.error(f"Erreur IA : {e}")

