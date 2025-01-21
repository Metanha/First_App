import streamlit as st
import pandas as pd


st.markdown("<h1 style='text-align: center; color: black;'>MY DATA APP</h1>", unsafe_allow_html=True)

st.markdown("""
This app allows you to download scraped data on motocycles from expat-dakar 
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Expat-Dakar](https://www.expat-dakar.com/).
""")


# Fonction de loading des données
def load_(dataframe, title, key) :
    st.markdown("""
    <style>
    div.stButton {text-align:center}
    </style>""", unsafe_allow_html=True)

    if st.button(title,key):
      
        st.subheader('Display data dimension')
        st.write('Data dimension: ' + str(dataframe.shape[0]) + ' rows and ' + str(dataframe.shape[1]) + ' columns.')
        st.dataframe(dataframe)

# définir quelques styles liés aux box
st.markdown('''<style> .stButton>button {
    font-size: 12px;
    height: 3em;
    width: 25em;
}</style>''', unsafe_allow_html=True)

          
# Charger les données 
load_(pd.read_csv('data/motos_scooters1.csv'), 'Motocycles data 1', '1')
load_(pd.read_csv('data/motos_scooters2.csv'), 'Motocycles data 2', '2')
load_(pd.read_csv('data/motos_scooters3.csv'), 'Motocycles data 3', '3')
load_(pd.read_csv('data/motos_scooters4.csv'), 'Motocycles data 4', '4')
load_(pd.read_csv('data/motos_scooters5.csv'), 'Motocycles data 5', '5')




 


