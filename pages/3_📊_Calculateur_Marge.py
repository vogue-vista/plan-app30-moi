import streamlit as st

st.title("📊 Calculateur de Marge & Profits")

st.write("Calculez automatiquement votre marge en tenant compte des frais.")

prix_vente = st.number_input("Prix de vente", min_value=0.0, step=0.01)
prix_achat = st.number_input("Prix d'achat", min_value=0.0, step=0.01)
frais_plateforme = st.number_input("Frais plateforme (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.5)
frais_pub = st.number_input("Coût pub par vente", min_value=0.0, step=0.01)

if st.button("Calculer"):
    if prix_vente == 0 or prix_achat == 0:
        st.error("Prix de vente et prix d'achat doivent être > 0.")
    else:
        frais_plateforme_val = prix_vente * (frais_plateforme / 100)
        profit = prix_vente - prix_achat - frais_plateforme_val - frais_pub
        marge = (profit / prix_vente) * 100

        st.subheader("Résultats")
        st.write(f"💰 Profit par vente : {profit:.2f} $")
        st.write(f"📈 Marge : {marge:.2f} %")

        if profit > 0:
            st.success("Produit rentable ✅")
        else:
            st.error("Produit non rentable ❌")
