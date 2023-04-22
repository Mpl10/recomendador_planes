import streamlit as st
import pandas as pd
import textwrap
from streamlit_folium import folium_static
import folium
import webbrowser

import sys 
sys.path.append("src")
import src.soporte_streamlit as sp



df_cat = pd.read_csv("../data/CATEGORIAS.csv")
df_princ = pd.read_csv("../data/PRINCIPAL.csv")
df_todo = pd.merge(df_princ, df_cat, on="id")
pd.set_option('display.max_colwidth', 1000)

# Pestaña de recomendaciones




# crear un panel de selección para la columna "categoria"
categorias = df_todo["categoria"].unique()

emoji_dict = {
    "Arte y cultura":                       ":art:",
    "Vida nocturna":                        ":sparkles:",
    "Gastronomía":                          ":knife_fork_plate:",
    "Deporte y actividad física":           ":runner:",
    "Planes al aire libre":                 ":woman-mountain-biking:",
    "Relax y bienestar":                    ":person_in_lotus_position:",
    "Entretenimiento":                      ":ferris_wheel:"
}
selected_categoria = st.sidebar.selectbox("Seleccione una categoría", categorias)

# filtrar el dataframe original por la selección del usuario
df_filtrado = df_todo[df_todo["categoria"] == selected_categoria]

#obtener los valores únicos de la columna "nombre"
nombres_unicos = df_filtrado["nombre"].unique()

# crear un segundo panel de selección para la columna "nombre" usando los valores únicos obtenidos
selected_nombre = st.sidebar.selectbox("Seleccione un plan", nombres_unicos)

# mostrar los resultados
st.title(f"{selected_nombre}")
st.write('')
st.write(f"{emoji_dict[selected_categoria]} Categoría:", selected_categoria)
#st.text( f"{selected_nombre}")


st.write('')
st.write('')
plan = df_todo[df_todo["nombre"] == selected_nombre]["id"].iloc[0]
imagen = df_todo[df_todo["id"] == plan]["imagen"].iloc[0]
st.image(imagen, width=300)
st.write('')
st.write('')




df_plan = df_filtrado[df_filtrado["id"] == plan]

# obtener el elemento correspondiente al nombre seleccionado
selected_plan = df_filtrado[df_filtrado["nombre"] == selected_nombre].iloc[0]
# obtener la información del plan seleccionado
precio = selected_plan["precio"]
if precio == 0:
    precio = "¡:fireworks: nuevo!"
rating = selected_plan["rating"]
if rating == 0:
    rating = "¡nuevo!"
url = selected_plan["url"]

# mostrar la información
st.write("#### **Detalles del plan:**")
st.write('')
st.write(":money_with_wings: Precio:", f"{str(precio)} €")
st.write(":star: Rating:", f"{str(rating)} ")
st.write(":speech_balloon: Información y compra de ticktets o reserva:", url)
st.write('')
st.write('')
st.write("**Ubicación:**")
direccion = selected_plan["direccion"]
st.write(f":pushpin: {direccion}")
st.write('')

# obtener la latitud y longitud del plan seleccionado
latitud = df_filtrado[df_filtrado["nombre"] == selected_nombre]["latitud"].values[0]
longitud = df_filtrado[df_filtrado["nombre"] == selected_nombre]["longitud"].values[0]
m = folium.Map(location=[latitud, longitud], zoom_start=15)
folium.Marker([latitud, longitud]).add_to(m)
folium_static(m, width=700, height=300)


st.write('')
st.write('')
st.write("#### **Planes similares:**")
st.write('')
df_similares= sp.planes_similares(plan)

df_similares = df_similares[['nombre', 'imagen','url']].head(3)

# Mostrar cada elemento con su respectiva imagen
for i, row in df_similares.iterrows():
    col1, col2 = st.columns(2)
    with col1:
        st.image(row['imagen'], width=250)

    with col2:
        #st.write("**" + row['url'] + "**")
        if st.button(f"Saber más acerca de ➜ {row['nombre']}"):        
            webbrowser.open(row['url'])




