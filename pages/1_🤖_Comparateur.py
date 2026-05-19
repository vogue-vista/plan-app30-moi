import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup
from groq import Groq

# 🔒 Sécurité : accès réservé aux sessions activées
if "connecte" not in st.session_state or st.session_state.connecte is False:
    st.error("⛔ Accès refusé. Veuillez activer votre licence pour utiliser cet outil.")
    st.stop()

st.title("🤖 Comparateur de Prix Ultra PRO")
st.write("Entrez un produit, je vais comparer automatiquement plusieurs sites et l'IA vous donnera la meilleure option.")

# 🔑 Clés API depuis les secrets (à configurer dans Streamlit Cloud)
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    SCRAPEDO_API_KEY = st.secrets["SCRAPEDO_API_KEY"]
except Exception:
    st.error("❌ Clés API manquantes dans les secrets Streamlit (GROQ_API_KEY, SCRAPEDO_API_KEY).")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

produit = st.text_input("Nom du produit à comparer (ex: brosse lissante, air fryer, chaise gaming) :")

def scrape_with_scrapedo(url: str) -> str:
    """Retourne le HTML d'une URL via Scrape.do."""
    try:
        r = requests.get(
            "https://api.scrape.do",
            params={"token": SCRAPEDO_API_KEY, "url": url},
            timeout=30
        )
        return r.text
    except Exception as e:
        st.warning(f"Erreur Scrape.do pour {url} : {e}")
        return ""

def extract_google_shopping(query: str):
    results = []
    search_url = f"https://www.google.ca/search?tbm=shop&q={query.replace(' ', '+')}"
    html = scrape_with_scrapedo(search_url)
    if not html:
        return results

    soup = BeautifulSoup(html, "html.parser")
    items = soup.select("div.sh-dgr__grid-result, div.sh-pr__product-results > div")

    for item in items[:5]:
        titre_el = item.select_one("h4, .tAxDx")
        prix_el = item.select_one(".a8Pemb, .T14wmb")
        vendeur_el = item.select_one(".aULzUe, .aULzUe span")
        lien_el = item.select_one("a")

        titre = titre_el.text.strip() if titre_el else "Sans titre"
        prix = prix_el.text.strip() if prix_el else "N/A"
        vendeur = vendeur_el.text.strip() if vendeur_el else "N/A"
        lien = "https://www.google.ca" + lien_el.get("href") if lien_el and lien_el.get("href") else ""

        results.append({
            "Source": "Google Shopping",
            "Titre": titre,
            "Prix": prix,
            "Vendeur": vendeur,
            "Lien": lien
        })
    return results

def extract_amazon_ca(query: str):
    results = []
    search_url = f"https://www.amazon.ca/s?k={query.replace(' ', '+')}"
    html = scrape_with_scrapedo(search_url)
    if not html:
        return results

    soup = BeautifulSoup(html, "html.parser")
    items = soup.select("div.s-result-item")

    for item in items[:5]:
        titre_el = item.select_one("h2 a span")
        prix_whole = item.select_one("span.a-price-whole")
        prix_frac = item.select_one("span.a-price-fraction")
        lien_el = item.select_one("h2 a")

        titre = titre_el.text.strip() if titre_el else "Sans titre"
        if prix_whole:
            prix = prix_whole.text.strip().replace(",", "") + ("," + prix_frac.text.strip() if prix_frac else "")
            prix = prix + " $"
        else:
            prix = "N/A"

        vendeur = "Amazon.ca"
        lien = "https://www.amazon.ca" + lien_el.get("href") if lien_el and lien_el.get("href") else ""

        results.append({
            "Source": "Amazon",
            "Titre": titre,
            "Prix": prix,
            "Vendeur": vendeur,
            "Lien": lien
        })
    return results

def extract_walmart_ca(query: str):
    results = []
    search_url = f"https://www.walmart.ca/search?q={query.replace(' ', '+')}"
    html = scrape_with_scrapedo(search_url)
    if not html:
        return results

    soup = BeautifulSoup(html, "html.parser")
    items = soup.select("div[data-automation='product-card']")

    for item in items[:5]:
        titre_el = item.select_one("a[data-automation='product-title']")
        prix_el = item.select_one("span[data-automation='product-price']")
        vendeur_el = item.select_one("span[data-automation='merchant-name']")
        lien_el = item.select_one("a[data-automation='product-title']")

        titre = titre_el.text.strip() if titre_el else "Sans titre"
        prix = prix_el.text.strip() if prix_el else "N/A"
        vendeur = vendeur_el.text.strip() if vendeur_el else "Walmart"
        lien = "https://www.walmart.ca" + lien_el.get("href") if lien_el and lien_el.get("href") else ""

        results.append({
            "Source": "Walmart",
            "Titre": titre,
            "Prix": prix,
            "Vendeur": vendeur,
            "Lien": lien
        })
    return results

def call_groq_analysis(df: pd.DataFrame, produit: str) -> str:
    """Envoie les résultats à l'IA Groq pour un résumé + recommandation."""
    if df.empty:
        return "Aucune donnée à analyser."

    texte = f"Produit recherché : {produit}\n\nVoici les offres trouvées :\n\n"
    for _, row in df.iterrows():
        texte += f"- Source: {row['Source']}, Titre: {row['Titre']}, Prix: {row['Prix']}, Vendeur: {row['Vendeur']}\n"

    prompt = (
        "Tu es un expert e-commerce. Analyse ces offres et réponds en français.\n"
        "1) Donne un résumé rapide du marché (prix bas, haut, moyen).\n"
        "2) Recommande la meilleure offre (en expliquant pourquoi).\n"
        "3) Donne un conseil pour un vendeur qui veut être compétitif.\n\n"
        + texte
    )

    chat = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Tu es un expert en pricing e-commerce."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=600
    )

    return chat.choices[0].message.content

if st.button("Lancer la comparaison") and produit.strip():
    with st.spinner("🔎 Recherche des meilleures offres en cours..."):
        query = produit.strip()

        all_results = []
        all_results += extract_google_shopping(query)
        all_results += extract_amazon_ca(query)
        all_results += extract_walmart_ca(query)

        if not all_results:
            st.error("Aucune offre trouvée. Essaie avec un autre mot-clé ou vérifie les sites.")
        else:
            df = pd.DataFrame(all_results)

            st.subheader("📊 Résultats comparés")
            st.dataframe(df)

            # Affichage du meilleur prix (si possible)
            def prix_to_float(p):
                try:
                    p = p.replace("$", "").replace("CA", "").replace(" ", "").replace(",", ".")
                    return float(p)
                except:
                    return None

            df["Prix_num"] = df["Prix"].apply(prix_to_float)
            df_valid = df.dropna(subset=["Prix_num"])

            if not df_valid.empty:
                best = df_valid.sort_values("Prix_num").iloc[0]
                st.success(
                    f"✅ Meilleur prix trouvé : {best['Prix']} chez {best['Vendeur']} ({best['Source']})"
                )
                if best["Lien"]:
                    st.markdown(f"[🔗 Voir le produit]({best['Lien']})")
            else:
                st.info("Impossible de déterminer un meilleur prix (formats de prix non reconnus).")

            st.markdown("---")
            st.subheader("🧠 Analyse IA du marché")

            try:
                analyse = call_groq_analysis(df, produit)
                st.write(analyse)
            except Exception as e:
                st.error(f"Erreur lors de l'appel à l'IA : {e}")

elif st.button("Lancer la comparaison") and not produit.strip():
    st.error("Entre un nom de produit avant de lancer la comparaison.")
