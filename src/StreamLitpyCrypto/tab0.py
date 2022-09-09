import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import yahoofinance as yf
import re
# Désolé je vais rajouter les commentaires asap
def app():


    ### Create Title
    st.title("Présentation du projet PyCrypto")
    ### Add a picture
    st.image("assets/logoPyCrypto.png")
    st.header("Contexte")
    st.subheader("Du point de vue technique")
    st.write("Nous avons utilisé un package nommé Universal portfolio comme base pour notre démonstration." )
    st.write("Ce “framework” nous permet de consommer les algorithmes les plus courants, de les tester sur les périodes passées et d’ensuite de focaliser nos efforts dans le but de trouver le modèle le plus performant sur des périodes à venir.")  
    st.subheader("Du point de vue économique")  
    st.write("L’utilisation des algorithmes de trading peut intervenir dans le monde de la finance pour générer des gains lors des opérations dans les marchés financiers.")
    st.write("Dans notre cas, nous l’utilisons sur les marchés des nouvelles technologies telles que le NASDAQ et les cryptomonnaies, car ces deux types de marchés sont liés entre eux.")
    st.subheader("Du point de vue scientifique")
    st.write("Ce projet met en œuvre des techniques d'acquisition, de préparation et d’analyse des données, dans le but de développer un modèle de machine learning pour le choix d’un algorithme pertinent et efficace d’allocation de portefeuille.")

    st.title("Objectifs")
    st.subheader("Problématique")
    st.write("Étant donné une allocation du portefeuille à un instant t, on peut représenter un portefeuille sous la forme d'un vecteur d’une allocation d’actifs.")
    st.write("Notre problématique est de trouver les meilleurs poids associés à ses actifs pour l’instant t+1.")
    st.write("Nous utiliserons les algorithmes existant dans le répertoire Github que nous sélectionnerons en fonction des prédictions déterminées par les variables indicatrices choisies. Nous pourrons ainsi en déduire l’algorithme optimal à utiliser sur la période future.") 
    st.subheader("Niveau d’expertise") 
    st.write("Ahmed :  Ayant déjà traité du signal aléatoire tel que les séries temporelles")
    st.write("Pierre :  Technicien supérieur consultant (Autodidacte en machine learning)")
    st.write("Sofiane : Architecte SI/Web/Logiciel, développeur web fullstack et blockchain, exploitant et administrateur de site web.")