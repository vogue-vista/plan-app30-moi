import streamlit as st

# 🔒 Sécurité : bloque l'accès si pas connecté
if "connecte" not in st.session_state or st.session_state.connecte is False:
    st.error("⛔ Accès refusé. Veuillez activer votre licence pour utiliser cet outil.")
    st.stop()

import pandas as pd

st.title("🤖 Robot Comparateur de Prix")

st.write("Comparez rapidement plusieurs fournisseurs pour un même produit.")

produit = st.text_input("Nom du produit :")
col1, col2, col3 = st.columns(3)

with col1:
    f1_nom = st.text_input("Fournisseur 1")
    f1_prix = st.number_input("Prix fournisseur 1", min_value=0.0, step=0.01)
with col2:
    f2_nom = st.text_input("Fournisseur 2")
    f2_prix = st.number_input("Prix fournisseur 2", min_value=0.0, step=0.01)
with col3:
    f3_nom = st.text_input("Fournisseur 3")
    f3_prix = st.number_input("Prix fournisseur 3", min_value=0.0, step=0.01)

if st.button("Comparer"):
    data = []
    if f1_nom: data.append([f1_nom, f1_prix])
    if f2_nom: data.append([f2_nom, f2_prix])
    if f3_nom: data.append([f3_nom, f3_prix])

    if not data:
        st.error("Ajoutez au moins un fournisseur.")
    else:
        df = pd.DataFrame(data, columns=["Fournisseur", "Prix"])
        st.subheader(f"Résultats pour : {produit}")
        st.dataframe(df.sort_values("Prix"))

        meilleur = df.sort_values("Prix").iloc[0]
        st.success(f"✅ Meilleur prix : {meilleur['Fournisseur']} à {meilleur['Prix']} $")
