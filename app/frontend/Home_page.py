import streamlit as st

def show():
    st.title("Bienvenue sur PulmoScanAI !")
    
    # Ajouter une première image
    st.image("style/images/4.jpg", use_column_width=True)
    
    # Ajouter une zone de texte pour la première image
    st.text_area(" ","PulmoScanAI vous propose une aide professionnelle pour l'analyse de vos images médicales. Notre application est basée sur des modèles de deep learning qui permettent de détecter et de classifier les pathologies pulmonaires.")
    
    # Ajouter une deuxième image
    st.image("style/images/5.jpg", use_column_width=True)
    
    # Ajouter une zone de texte pour la deuxième image
    st.text_area(" ", "Nous vous offrons la possibilité de télécharger vos images médicales et de les analyser en quelques secondes. Vous pouvez également consulter les résultats de vos analyses réalisées sur le site.")

