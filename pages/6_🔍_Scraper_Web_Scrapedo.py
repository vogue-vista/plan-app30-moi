import streamlit as st
import requests
from bs4 import BeautifulSoup
from groq import Groq

# 🔒 Sécurité
if "connecte" not in st.session_state or st.session_state.connecte is False:
    st.error("⛔ Accès refusé. Veuillez activer votre licence.")
    st.stop()

st.title("🔍 Scraper Web PRO (Scrape.do + IA)")
st.write("Scrape n'importe quelle page web et laisse l'IA analyser automatiquement le contenu.")

# 🔑 Clés API sécurisées
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    SCRAPEDO_API_KEY = st.secrets["SCRAPEDO_API_KEY"]
except:
    st.error("❌ Clés API manquantes dans les secrets Streamlit.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# --- Interface ---
url = st.text_input("URL à scraper :")

def scrape_url(url):
    """Scrape via Scrape.do"""
    try:
        r = requests.get(
            "https://api.scrape.do",
            params={"token": SCRAPEDO_API_KEY, "url": url},
            timeout=30
        )
        return r.text
    except Exception as e:
        st.error(f"Erreur Scrape.do : {e}")
        return ""

def extract_info(html):
    """Extraction automatique du contenu"""
    soup = BeautifulSoup(html, "html.parser")

    titre = soup.title.text.strip() if soup.title else "Aucun titre trouvé"
    paragraphs = [p.text.strip() for p in soup.find_all("p") if p.text.strip()]
    images = [img.get("src") for img in soup.find_all("img") if img.get("src")]

    return titre, paragraphs[:5], images[:5]

def analyse_ia(titre, paragraphs):
    """Analyse IA via Groq"""
    texte = "\n".join(paragraphs)

    prompt = f"""
Analyse cette page web et résume-la en français.

Titre : {titre}

Contenu :
{texte}

Donne :
1. Un résumé clair
2. Les points importants
3. Le type de page (blog, fiche produit, article, etc.)
4. Une recommandation SEO
"""

    chat = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Tu es un expert en analyse web et SEO."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=600
    )

    return chat.choices[0].message.content

# --- Action ---
if st.button("Scraper la page"):
    if not url.strip():
        st.error("Veuillez entrer une URL.")
        st.stop()

    st.info("⏳ Scraping en cours...")

    html = scrape_url(url)

    if html:
        st.subheader("📄 HTML brut")
        st.code(html[:5000])

        titre, paragraphs, images = extract_info(html)

        st.subheader("📝 Informations extraites automatiquement")
        st.write(f"**Titre détecté :** {titre}")

        st.write("**Paragraphes détectés :**")
        for p in paragraphs:
            st.write("- " + p)

        if images:
            st.write("**Images détectées :**")
            for img in images:
                st.write(img)

        st.markdown("---")
        st.subheader("🧠 Analyse IA de la page")

        try:
            analyse = analyse_ia(titre, paragraphs)
            st.write(analyse)
        except Exception as e:
            st.error(f"Erreur IA : {e}")

