import streamlit as st
import leafmap.foliumap as leafmap

st.sidebar.title("About")
st.sidebar.info("Visualizador con WMS de Madrid")
st.sidebar.image("https://i.imgur.com/UbOXYAU.png")

st.title("Mapa interactivo con WMS de Madrid")

# Columnas para controles y mapa
col1, col2 = st.columns([4, 1])

# Diccionario con tus WMS
wms_layers = {
    "Cartografía General de Madrid": {
        "url": "https://sigma.madrid.es/vector/services/MAPAS_BASE/CARTOBASE_LINEAS_WGS84/MapServer/WMSServer",
        "layers": "0"  # En algunos casos se puede usar "0" como identificador simple
    },
    "Mapa de Vegetación (2022)": {
        "url": "https://georaster.madrid.es/ApolloCatalogWMSpublic/service.svc/get",
        "layers": "ESTRATOS_VEGETALES_VR2022"
    }
}

# Lista de nombres visibles para el selector
wms_names = list(wms_layers.keys())

with col2:
    selected_wms = st.selectbox("Selecciona una capa WMS:", wms_names)

with col1:
    # Crear el mapa interactivo
    m = leafmap.Map(
        locate_control=True,
        latlon_control=True,
        draw_export=True,
        minimap_control=True
    )

    # Extraer la info del WMS seleccionado
    wms_info = wms_layers[selected_wms]
    m.add_wms_layer(
        url=wms_info["url"],
        layers=wms_info["layers"],
        name=selected_wms,
        format="image/png",
        transparent=True
    )

    # Renderizar el mapa en Streamlit
    m.to_streamlit(height=700)

