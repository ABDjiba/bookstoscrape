import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


st.set_page_config(
    page_title="Bookstoscrapedash",
    layout="wide"
)

data=pd.read_csv("base_finale.csv")
data=pd.DataFrame(data)

filtre = st.sidebar.multiselect("Sélectionnez des catégorie", data["Catégorie"].unique())

# Filtrer les données en fonction des catégories sélectionnée
data = data[data["Catégorie"].isin(filtre)]


st.title("Données bookstoscrape")

if st.button("Exécuter les tâches"):
    if not data.empty:
            cadre1, cadre2, cadre3 = st.columns(3)

            with cadre1 :
                st.markdown("### Nombre de livres")
                value=f"{len(data)} Livres"
                st.markdown(f"## {value}")


            data=data.sort_values(by="Prix_euro")


            with cadre2:
                st.markdown("### 3 livres les plus chères")
                for i in range(3):
                    prix=data.loc[i,"Prix"]
                    titre=data.loc[i,"Titre"]
                    value=f"{titre} : {prix} "
                    st.write(value)

            max=pd.DataFrame(data["Catégorie"].value_counts())

            with cadre3:
                st.markdown("### Catégorie avec le plus de livres")
                st.markdown(f"## {max.iloc[0,0]}")


            st.markdown("### médianes des prix en fonction des catégories")

            data['Note'] = data['Note'].astype(int)
            medianes_par_categorie = data.groupby('Catégorie')['Note'].median().reset_index()

            # Créer l'histogramme des médianes des notes pour chaque catégorie avec Plotly Express
            fig = px.bar(medianes_par_categorie, x='Catégorie', y='Note', color='Catégorie',
                         color_discrete_sequence=px.colors.qualitative.Dark2)

            # Ajouter des labels et un titre
            fig.update_layout(xaxis_title='Catégorie', yaxis_title='Médiane des Notes')

            # Mettre les labels en position verticale
            fig.update_xaxes(tickangle=90)

            st.write(fig)


            st.markdown("Boxplot des prix en fonction des catégories")

            fig1 = px.box(data, x='Catégorie', y='Prix_euro', color='Catégorie',
                         color_discrete_sequence=px.colors.qualitative.Dark2)

            # Ajouter des labels et un titre
            fig1.update_layout(xaxis_title='Catégorie', yaxis_title='Prix (en euros)'
                              )

            # Mettre les labels en position verticale
            fig1.update_xaxes(tickangle=90)

            st.write(fig1)

