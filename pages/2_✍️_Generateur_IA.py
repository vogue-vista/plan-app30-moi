import streamlit as st
from groq import Groq

# 🔒 Sécurité : accès réservé aux sessions activées
if "connecte" not in st.session_state or st.session_state.connecte is False:
    st.error("⛔ Accès refusé. Veuillez activer votre licence pour utiliser cet outil.")
    st.stop()

st.title("✍️ Générateur de Fiches Produits IA (Version PRO)")
st.write("Générez une fiche produit professionnelle grâce à l'intelligence artificielle.")

# 🔑 Récupération sécurisée des clés API
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error("❌ Clé GROQ_API_KEY manquante dans les secrets Streamlit.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# --- Interface ---
nom = st.text_input("Nom du produit")
benefices = st.text_area("Bénéfices / caractéristiques principales")
public = st.text_input("Public cible (ex : femmes 25–35, sportifs, etc.)")
ton = st.selectbox("Ton du texte", ["Professionnel", "Amical", "Luxe", "Fun", "Persuasif", "Éducatif"])

if st.button("Générer la fiche produit"):
    if not nom or not benefices:
        st.error("Nom du produit et bénéfices sont obligatoires.")
    else:
        prompt = f"""
Tu es un expert en copywriting e-commerce.

Génère une fiche produit complète et optimisée pour les conversions.

Détails :
- Nom du produit : {nom}
- Bénéfices : {benefices}
- Public cible : {public}
- Ton : {ton}

Structure demandée :
1. Un titre accrocheur
2. Une description persuasive
3. Une liste de bénéfices clairs
4. Un paragraphe final qui donne envie d’acheter
"""

        try:
            chat = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "Tu es un expert en rédaction e-commerce."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=600
            )

            texte = chat.choices[0].message.content

            st.subheader("📝 Fiche produit générée")
            st.write(texte)

        except Exception as e:
            st.error(f"Erreur lors de l'appel à l'IA : {e}")

