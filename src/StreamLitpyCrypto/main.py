import tab1
import tab2
import tab3
import streamlit as st
st.set_option('deprecation.showPyplotGlobalUse', False)
PAGES = {
    "DataViz": tab1,
    "Prediction": tab2,
    "Trading": tab3
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()
