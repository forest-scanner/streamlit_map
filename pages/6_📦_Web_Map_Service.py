import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

markdown = """
Una plantilla de mapa de Streamlit.
"""

st.sidebar.title("Sobre la aplicación")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

# La nueva URL del servicio WMS y el nombre de la capa
WMS_URL = "https://georaster.madrid.es/ApolloCatalogWMSpublic/service.svc/get"
WMS_LAYER = "ORTO_2023_10_90"

st.title("Servicio de Mapas Web (WMS) - Ortofoto Madrid")
st.markdown(
    """
Esta aplicación carga el servicio WMS de la ortofoto de Madrid de 2023.
La URL del servicio y la capa ya están preconfiguradas.
"""
)

row1_col1, row1_col2 = st.columns([3, 1.3])
width = None
height = 600

with row1_col2:
    # Mostramos la URL del WMS en un cuadro de texto, ya preconfigurado
    url = st.text_input(
        "URL del servicio WMS:", value=WMS_URL
    )
    # Mostramos la capa WMS que se va a cargar
    st.markdown(f"**Capa WMS a cargar:** `{WMS_LAYER}`")
    
with row1_col1:
    # Inicializamos el mapa con una vista centrada en Madrid
    m = leafmap.Map(center=(40.4168, -3.7038), zoom=12)

    # Añadimos la capa WMS directamente, ya que está predefinida
    m.add_wms_layer(
        url, layers=WMS_LAYER, name=WMS_LAYER, attribution="Ayuntamiento de Madrid", transparent=True
    )
    
    # El código de la leyenda se ha eliminado ya que no es necesario para esta capa específica
    
    # Mostramos el mapa en la interfaz de Streamlit
    m.to_streamlit(width, height)
