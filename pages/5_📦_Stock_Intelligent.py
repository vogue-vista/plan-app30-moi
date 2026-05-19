import streamlit as st
import pandas as pd
import requests

# 🔒 Sécurité
if "connecte" not in st.session_state or st.session_state.connecte is False:
    st.error("⛔ Accès refusé. Veuillez activer votre licence.")
    st.stop()

st.title("📦 Gestionnaire de Stock Intelligent (Version PRO)")
st.write("Stock persistant via Google Sheets — parfait pour un SaaS.")

# 🔑 Récupération sécurisée du Google Sheet
try:
    SHEET_URL = st.secrets["GOOGLE_SHEET_URL"]
except:
    st.error("❌ GOOGLE_SHEET_URL manquant dans les secrets Streamlit.")
    st.stop()

def charger_stock():
    try:
        df = pd.read_csv(SHEET_URL)
        return df
    except Exception as e:
        st.error(f"Erreur chargement Google Sheet : {e}")
        return pd.DataFrame(columns=["produit", "quantite", "seuil"])

def sauvegarder_stock(df):
    st.warning("⚠️ Sauvegarde manuelle requise : copie/colle le CSV dans ton Google Sheet.")
    st.code(df.to_csv(index=False))

# --- Interface ---
st.subheader("➕ Ajouter un produit")
nom = st.text_input("Nom du produit")
quantite = st.number_input("Quantité", min_value=0, step=1)
seuil = st.number_input("Seuil d’alerte", min_value=0, step=1)

df_stock = charger_stock()

if st.button("Ajouter au stock"):
    if not nom:
        st.error("Le nom du produit est obligatoire.")
    else:
        nouveau = pd.DataFrame([{
            "produit": nom,
            "quantite": int(quantite),
            "seuil": int(seuil)
        }])
        df_stock = pd.concat([df_stock, nouveau], ignore_index=True)
        st.success("Produit ajouté !")
        sauvegarder_stock(df_stock)

# --- Affichage ---
st.subheader("📋 Stock actuel")
df_stock = charger_stock()

if df_stock.empty:
    st.info("Aucun produit en stock.")
else:
    st.dataframe(df_stock)

    st.subheader("⚠️ Alertes automatiques")
    alertes = df_stock[df_stock["quantite"] <= df_stock["seuil"]]

    if len(alertes) > 0:
        st.error("Produits à réapprovisionner :")
        st.dataframe(alertes)
    else:
        st.success("Aucune alerte.")

