import tab0
import tab1
import tab2
import tab3

import tab5
import tab6
import tab7
import streamlit as st
# Désolé je vais rajouter les commentaires asap
st.set_option('deprecation.showPyplotGlobalUse', False)
PAGES = {
    "Présentation": tab0,
    "Analyse exploratoire": tab1,
    "Summarize": tab3,
    "Prédiction": tab2,
    "Wordclouds" : tab6,
    "pyCrypto" : tab7
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()