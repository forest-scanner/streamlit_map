import streamlit as st
import leafmap.foliumap as leafmap



# Page title
st.title("Streamlit for Geospatial Applications")

# Mapa ancho completo
m = leafmap.Map(minimap_control=True)
m.add_basemap("CartoDB.Positron")
m.to_streamlit(height=500, width=1400)  # Fuerza ancho más grande 

