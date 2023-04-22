import streamlit as st
import pandas as pd


# Pestaña de análisis
with st.container():
    st.title("Proyecto de recomendación de ocio")

    st.write("El **objetivo** del proyecto es proporcionar una herramienta útil y fácil de usar que permita a las personas explorar nuevas opciones de ocio y disfrutar de su tiempo libre de una manera más divertida y gratificante..")

    st.write("Para este proyecto se plantea el objetivo de generar alternativas de ocio para momentos en los que no se tenga una idea clara de qué hacer, a través de la recopilación de datos y la generación de un algoritmo de recomendación. Para ello, se han seleccionado como fuentes de datos iniciales las plataformas de Groupon, Fever y TripAdvisor. Estas plataformas ofrecen una amplia variedad de opciones de ocio en Madrid (que inicialmente será el área en la que nos centraremos en este proyecto), lo que permitirá una exploración exhaustiva y una recopilación de datos representativa. El objetivo final es crear una herramienta que ayude a los usuarios a encontrar opciones de ocio personalizadas y adecuadas a sus intereses y preferencias, utilizando tecnología de algoritmos de recomendación y aprovechando la gran cantidad de datos disponibles en estas plataformas.")

    st.write('')
    st.write('')
    st.write("**Gráfico 1**: En el gráfico podemos apreciar la cantidad de información procedente de cada una de las 3 fuentes")
    st.write('')
    st.image("../images/1.PNG", width=700)
    

    st.write('')
    st.write('')
    st.write('')
    st.write("**Gráfico 2**: Comparativa de número de planes por categoría con su precio medio")
    st.write('')
    st.image("../images/2.PNG", width=700)
    
    st.write('')
    st.write('')
    st.write('')
    st.write("**Gráfico 3**: Comparativa del posicionamiento de cada subcategoría en función de media de precio y valoraciones")
    st.write('')
    st.image("../images/3.PNG", width=700)
    


