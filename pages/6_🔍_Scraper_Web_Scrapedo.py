import streamlit as st

groq_key = st.secrets["GROQ_API_KEY"]
scrapedo_key = st.secrets["SCRAPEDO_API_KEY"]
import streamlit as st
import requests

# Sécurité
if "connecte" not in st.session_state or st.session_state.connecte is False:
    st.error("⛔ Accès refusé. Veuillez activer votre licence.")
    st.stop()

st.title("🔍 Scraper Web (Scrape.do)")
st.write("Scrape n'importe quelle page web facilement grâce à Scrape.do.")

# Clé API Scrape.do
scrapedo_key = st.text_input("Clé API Scrape.do :", type="password")

# URL à scraper
url = st.text_input("URL à scraper :")

if st.button("Scraper"):
    if not scrapedo_key:
        st.error("Veuillez entrer votre clé Scrape.do.")
        st.stop()

    if url.strip() == "":
        st.error("Veuillez entrer une URL.")
        st.stop()

    st.info("⏳ Scraping en cours...")

    api_url = "https://api.scrape.do"
    params = {
        "token": scrapedo_key,
        "url": url
    }

    try:
        r = requests.get(api_url, params=params)
        html = r.text

        st.subheader("📄 Résultat HTML brut")
        st.code(html[:5000])  # on limite l'affichage

    except Exception as e:
        st.error(f"Erreur scraping : {e}")
