import os
import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt
import plotly.express as px
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
import requests
from requests import get

# 🛠️ Installer Chromium et ChromeDriver (pour Streamlit Cloud)
#os.system("apt update && apt install -y chromium-chromedriver")
os.system("apt update && apt install -y chromium-driver")

# mise en format
st.markdown(
    """

    <h1 id="dynamic-title";color=:#ffa500>APPLICATION DE SCRAPING DE DONNEES</h1>

    <style>
        /* Changer la couleur de fond */
        body {
            background-color: #F0F2F6; /* Bleu clair */
        }

        /* Changer la couleur de la barre latérale */
        section[data-testid="stSidebar"] {
            background-color: #ADD8E6; /* Bleu pastel */
        }

        /* Changer la couleur des boutons */
        div.stButton > button {
            background-color: #FF4B4B; /* Rouge */
            color: white;
            border-radius: 5px;
        }
       
        /* Changer la couleur des titres */
        h1 {
            color: #007BFF; /* Bleu */
        }
       
        /* Changer la couleur des sous-titres */
        h2 {
            color: #333333; /* Gris foncé */
        }

    </style>

    <script>

    var title = document.getElementById("dynamic-title");
    var text = title.innerHTML;
    var i = 0;
    function scrollTitle() {
        title.innerHTML = text.substring(i) + " " + text.substring(0, i);
        i = (i + 1) % text.length;
    }
    setInterval(scrollTitle, 200);
    </script>
    """,
    unsafe_allow_html=True
)



#st.title("POJET: APPLICATION DE SCRAPING DE DONNEES")

try:
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    driver.quit()
except Exception as e:
    st.error(f"🚨 Erreur WebDriver : {e}")

# ✅ Configuration du driver Selenium
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")

    try:
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    except WebDriverException as e:
        st.error(f"Erreur ChromeDriver : {str(e)}")
        return None

# ✅ Scraping avec Selenium
def scrape_ordi(url,pages):
    driver = get_driver()
    if not driver:
        return pd.DataFrame()
    data=[]
    try:
        for i in range(1,pages+1):
            #driver.get(url.replace("page=1",f"page={pages}"))
            driver.get(url+f"{pages}")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "listing-card__content"))
            )
        
            soup = bs(driver.page_source, "html.parser")
            contenairs = soup.find_all("div", class_="listing-card__content")
            
            for content in contenairs:
                if content:
                    try:
                        img_tag = content.find("img", class_="listing-card__image__resource")
                        print("image")
                        Details= content.find("div", class_="listing-card__header__title").get_text(strip=True)
                        print("Detail")
                        Etat= content.find("div", class_="listing-card__header__tags")
                        print("Etat")
                        Prix= content.find("div", class_="listing-card__info-bar__price").find("span", class_="listing-card__price__value").get_text(strip=True).replace("F Cfa", "")
                        print("prix")
                        item = {
                            "Details": Details,
                            "Etat": Etat.find_all("span")[0].text if Etat else None,
                            "Prix":Prix ,
                            "Lien_image": img_tag["src"] if img_tag else "Image non disponible",
                            "Page":i

                            #"Lien_image": content.find("img", class_="listing-card__image__resource")["src"]
                            }
                        data.append(item)
                    except Exception as e:
                        print(f"⚠️ Erreur d'extraction : {str(e)}")
                        #st.warning(f"⚠️ Erreur d'extraction : {str(e)}")

        return pd.DataFrame(data)

    except Exception as e:
        st.error(f"Erreur de scraping: {str(e)}")
        return pd.DataFrame()
    finally:
        driver.quit()

# ✅ Affichage des données
def load_(dataframe, title):
    st.subheader(f'📊 Données : {title}')
    st.write(f'Dimensions: {dataframe.shape[0]} lignes et {dataframe.shape[1]} colonnes')
    st.dataframe(dataframe)

# 🌍 Configuration de la page 
#st.set_page_config(page_title="Web Scraping App", layout="wide")

# 🎛️ Barre latérale pour la navigation
menu = st.sidebar.radio("Navigation", ["📊 Scraper des données", "📈 Dashboard des données", "📝 Formulaire d'évaluation"])

# 📊 **Scraper des données**
if menu == "📊 Scraper des données":
    #st.title("Scraper des données")
    st.markdown("<h2 style='color:orange;'>Scraper des données</h2>",unsafe_allow_html=True)
    
    categorie = st.radio("Choisissez les données à scraper :", ["Ordinateurs", "Téléphones", "Télévision"])
    
    col1, col2 = st.columns(2)
    with col1:
        lance_scrap = st.button("🚀 Lancer le scraping")
    #with col2:
     #   telecharger_donne = st.button("📥 Télécharger les données")     

    url = ""
    nb_page=1
    if categorie == "Ordinateurs":
        url = "https://www.expat-dakar.com/ordinateurs?page="
        nb_page=st.sidebar.selectbox("Choisir le nombre de page à scrapper ",range(1,237+1))
        
    elif categorie == "Téléphones":
        url = "https://www.expat-dakar.com/telephones?page="
        nb_page=st.sidebar.selectbox("Choisir le nombre de page à scrapper ",range(1,195+1))
        
    elif categorie == "Télévision":
        url = "https://www.expat-dakar.com/tv-home-cinema?page="
        nb_page=st.sidebar.selectbox("Choisir le nombre de page à scrapper ",range(1,186+1))
    
    if lance_scrap:
        df = scrape_ordi(url,nb_page)
        if not df.empty:
            csv =df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Télécharger le CSV", csv, "donnees_scrapees.csv", "text/csv")
            st.session_state["scraped_data"] = df
            load_(df, categorie)
        else:
            st.warning("⚠️ Aucune donnée trouvée")
        

# 📈 **Dashboard des Données Scrapées**
elif menu == "📈 Dashboard des données":
    #st.title("📊 Dashboard des Données Scrapées")
    st.markdown("<h2 style='color:orange;'>📊 Dashboard des Données Scrapées</h2>",unsafe_allow_html=True)

    if "scraped_data" in st.session_state and not st.session_state["scraped_data"].empty:
        df = st.session_state["scraped_data"]
        df["Prix"] = pd.to_numeric(df["Prix"].astype(str).str.replace(r"[^\d]", "", regex=True), errors="coerce")
        col3,col4=st.columns([2,2])
        # **Histogramme des Prix**
        #st.write("",df.head())
        #st.write("",df.dtypes)
        with col3:
            #st.subheader("📈 Distribution des Prix",fontsize=12)
            st.markdown("<h3 style='text-align: center; font-size:18px;'>📉 Distribution des Prix</h3>", unsafe_allow_html=True)
            fig, ax = plt.subplots()
            ax.hist(df["Prix"], bins=20, color="blue", alpha=0.7)
            ax.set_xlabel("Prix (F CFA)")
            ax.set_ylabel("Nombre de produits")
            ax.set_title("Distribution des prix",fontsize=12)
            st.pyplot(fig)

        # **Répartition des Marques**
        with col4:
            #fig, ax = plt.subplots(8,10)
            #st.subheader("Répartition des Marques")
            st.markdown("<h3 style='text-align: center; font-size:18px;'>Repartition selon l'etat</h3>", unsafe_allow_html=True)
            fig_pie = px.pie(df, names="Etat", hole=0.3,width=600,height=300)
            st.plotly_chart(fig_pie)

        # **Tableau interactif avec filtres**
        st.subheader("📜 Filtrer les données")
        etat_filter = st.multiselect("Filtrer par état :", df["Etat"].unique())
        if etat_filter:
            df = df[df["Etat"].isin(etat_filter)]
        st.dataframe(df)
    else:
        st.warning("⚠️ Aucune donnée disponible. Faites d'abord un scraping.")

# 📝 **Formulaire d'évaluation**
elif menu == "📝 Formulaire d'évaluation":
    st.markdown("<h2 style='color:orange;'>📝 Formulaire d'évaluation</h2>",unsafe_allow_html=True)
    #st.title("📝 Formulaire d'évaluation")
    kobo_link = '<iframe src="https://ee.kobotoolbox.org/i/TOv0huae" width="800" height="600"></iframe>'
    st.markdown(kobo_link, unsafe_allow_html=True)
