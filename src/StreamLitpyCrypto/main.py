import tab1
import tab2
import tab3
import tab4
import tab5
import streamlit as st
# Désolé je vais rajouter les commentaires asap
st.set_option('deprecation.showPyplotGlobalUse', False)
PAGES = {
    "DataViz": tab1,
    "Prediction": tab2,
    "Trading": tab3,
    "Volatilty": tab4,
    "cashback": tab5
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()