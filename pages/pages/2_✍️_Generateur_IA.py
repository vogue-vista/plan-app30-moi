import streamlit as st

st.title("✍️ Générateur de Fiches Produits IA")

st.write("Générez des fiches produits complètes à partir de quelques informations.")

nom = st.text_input("Nom du produit")
benefices = st.text_area("Bénéfices / caractéristiques principales")
public = st.text_input("Public cible (ex : femmes 25–35, sportifs, etc.)")
ton = st.selectbox("Ton du texte", ["Professionnel", "Amical", "Luxe", "Fun"])

if st.button("Générer la fiche produit"):
    if not nom or not benefices:
        st.error("Nom du produit et bénéfices sont obligatoires.")
    else:
        # Ici tu peux brancher une vraie IA (OpenAI, Groq, etc.)
        # Exemple pseudo :
        # import openai
        # openai.api_key = "TA_CLE"
        # prompt = f"..."
        # response = openai.chat.completions.create(...)
        # texte = response.choices[0].message.content

        texte = f"""
Titre : {nom}

Description ({ton}) :

{nom} est conçu pour {public}. 
Voici pourquoi il se démarque :

- {benefices.replace('.', '.\n- ')}

Idéal pour celles et ceux qui recherchent une solution fiable, efficace et adaptée à leurs besoins.
"""

        st.subheader("📝 Fiche générée")
        st.code(texte)
