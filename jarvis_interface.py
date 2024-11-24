import streamlit as st
import jarvis as jv
# Titre de l'application
st.title("Jarvis")
# Champ de saisie de texte
user_input = st.text_input("Parlez à Jarvis :")

# Bouton pour afficher le texte
if st.button("Entrer"):
    output = jv.interact_w_jarvis(user_input)
    output = output["agent_outcome"].return_values["output"]
    st.write(f"Jarvis a dit {output}")
if st.button("Parler 🎙️"):
    st.write("Enregistrement...")
    st.write("🛠️😅Working on it...   sorry😅🛠️")
