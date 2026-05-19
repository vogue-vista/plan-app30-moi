import streamlit as st

st.set_page_config(page_title="Le coeur de TOUTE grande entreprise", page_icon="🎛️", layout="wide")

st.markdown("""
    <style>
    div.stButton > button:first-child {
        height: 120px; font-size: 20px; font-weight: bold; border-radius: 15px;
        background-color: #1E1E1E; color: #FFFFFF; border: 2px solid #333333; transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #FF4B4B; color: white; border-color: #FF4B4B; transform: translateY(-5px);
    }
    </style>
""", unsafe_allow_html=True)

if "connecte" not in st.session_state:
    st.session_state.connecte = False

st.title("🎛️ Stark Enterprise Suite")

# --- PAYWALL ---
if not st.session_state.connecte:
    st.subheader("💳 Activation de votre Licence Professionnelle (30$ / mois)")
    st.write("Accédez à la boîte à outils ultime automatisée pour votre e-commerce.")
    st.link_button("🟡 S'abonner via PayPal", "https://paypal.com", type="primary")
    st.markdown("---")

    with st.form("activation_hub"):
        st.subheader("🔑 Déjà abonné ? Activez votre session")
        cle_client = st.text_input("Entrez votre clé d'activation client :", type="password")
        bouton_valider = st.form_submit_button("Déverrouiller la suite de logiciels")

        cles_valides = ["Client_Alex94", "Client_BoutiquePro", "FleuristeMontreal", "MonPremierTest", "Paypal_User_2026"]

        if bouton_valider:
            if cle_client in cles_valides:
                st.session_state.connecte = True
                st.success("🔓 Session activée avec succès ! Chargement...")
                st.rerun()
            else:
                st.error("❌ Clé invalide ou abonnement non vérifié.")
    st.stop()

# --- HUB ---
st.success("🔓 Mode Professionnel Activé. Bienvenue sur votre Hub.")
if st.button("🔴 Fermer la session / Se déconnecter"):
    st.session_state.connecte = False
    st.rerun()

st.markdown("---")
row1_col1, row1_col2, row1_col3 = st.columns(3)
row2_col1, row2_col2, row2_col3 = st.columns(3)

with row1_col1:
    if st.button("🤖\n\nRobot Comparateur\nde Prix", use_container_width=True):
        st.switch_page("pages/1_🤖_Comparateur.py")
with row1_col2:
    if st.button("✍️\n\nGénérateur de\nFiches IA", use_container_width=True):
        st.switch_page("pages/2_✍️_Generateur_IA.py")
with row1_col3:
    if st.button("📊\n\nCalculateur de\nMarge & Profits", use_container_width=True):
        st.switch_page("pages/3_📊_Calculateur_Marge.py")
with row2_col1:
    if st.button("📈\n\nAnalyseur de\nProduits e‑Commerce", use_container_width=True):
        st.switch_page("pages/4_📈_Analyse_eCommerce_PRO.py")
with row2_col2:
    if st.button("📦\n\nGestionnaire de\nStock Intelligent", use_container_width=True):
        st.switch_page("pages/5_📦_Stock_Intelligent.py")
with row2_col3:
    if st.button("💼\n\nRéponses Client\nPro IA", use_container_width=True):
        st.switch_page("pages/6_💼_Reponses_Pro_IA.py")
