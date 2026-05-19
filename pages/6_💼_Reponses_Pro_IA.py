import streamlit as st

# 🔒 Sécurité : bloque l'accès si pas connecté
if "connecte" not in st.session_state or st.session_state.connecte is False:
    st.error("⛔ Accès refusé. Veuillez activer votre licence pour utiliser cet outil.")
    st.stop()


st.title("💼 Générateur de Réponses Professionnelles (IA)")

st.write("Outil destiné aux entreprises pour répondre automatiquement aux messages clients.")

message = st.text_area("Message reçu du client :")

st.caption("💡 Idée : ce module peut être branché à une vraie IA (OpenAI, Claude, Groq) pour des réponses encore plus intelligentes.")

if st.button("Générer une réponse professionnelle"):
    if message.strip() == "":
        st.error("Veuillez entrer un message.")
    else:
        if "rembourse" in message.lower():
            categorie = "Demande de remboursement"
            reponse = (
                "Bonjour,\n\n"
                "Merci pour votre message. Nous comprenons votre demande de remboursement. "
                "Pouvez-vous nous fournir votre numéro de commande afin que nous puissions traiter cela rapidement ?\n\n"
                "Cordialement,\nService Client"
            )
        elif "retard" in message.lower() or "livraison" in message.lower():
            categorie = "Problème de livraison"
            reponse = (
                "Bonjour,\n\n"
                "Nous sommes désolés pour le retard de votre livraison. "
                "Nous vérifions immédiatement l’état de votre colis et revenons vers vous sous peu.\n\n"
                "Merci de votre patience."
            )
        elif "merci" in message.lower():
            categorie = "Message positif"
            reponse = (
                "Bonjour,\n\n"
                "Merci beaucoup pour votre retour positif ! "
                "Nous sommes ravis que vous soyez satisfait.\n\n"
                "Belle journée à vous."
            )
        else:
            categorie = "Demande générale"
            reponse = (
                "Bonjour,\n\n"
                "Merci pour votre message. Nous revenons vers vous avec plus d'informations dans les plus brefs délais.\n\n"
                "Cordialement."
            )

        st.write(f"📌 **Type détecté :** {categorie}")
        st.subheader("✉️ Réponse générée")
        st.code(reponse)
