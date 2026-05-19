import streamlit as st

# 🔒 Sécurité : bloque l'accès si pas connecté
if "connecte" not in st.session_state or st.session_state.connecte is False:
    st.error("⛔ Accès refusé. Veuillez activer votre licence pour utiliser cet outil.")
    st.stop()

import pandas as pd
import sqlite3
from pathlib import Path

st.title("📦 Gestionnaire de Stock Intelligent")

st.write("Suivez vos stocks, seuils d’alerte et réapprovisionnements.")

DB_PATH = Path("stock.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS stock (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produit TEXT,
            quantite INTEGER,
            seuil INTEGER
        )
    """)
    conn.commit()
    conn.close()

def ajouter_produit(produit, quantite, seuil):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO stock (produit, quantite, seuil) VALUES (?, ?, ?)", (produit, quantite, seuil))
    conn.commit()
    conn.close()

def charger_stock():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM stock", conn)
    conn.close()
    return df

init_db()

st.subheader("➕ Ajouter un produit")
nom = st.text_input("Nom du produit")
quantite = st.number_input("Quantité", min_value=0, step=1)
seuil = st.number_input("Seuil d’alerte", min_value=0, step=1)

if st.button("Ajouter au stock"):
    if not nom:
        st.error("Le nom du produit est obligatoire.")
    else:
        ajouter_produit(nom, int(quantite), int(seuil))
        st.success("Produit ajouté au stock !")

st.subheader("📋 Stock actuel")
df_stock = charger_stock()
if df_stock.empty:
    st.info("Aucun produit en stock pour le moment.")
else:
    st.dataframe(df_stock[["produit", "quantite", "seuil"]])

    st.subheader("⚠️ Alertes automatiques")
    alertes = df_stock[df_stock["quantite"] <= df_stock["seuil"]]
    if len(alertes) > 0:
        st.error("Certains produits nécessitent un réapprovisionnement :")
        st.dataframe(alertes[["produit", "quantite", "seuil"]])
    else:
        st.success("Aucune alerte pour le moment.")
