import streamlit as st
import leafmap.foliumap as leafmap

st.sidebar.title("About")
st.sidebar.info("Visualizador con WMS de Madrid")
st.sidebar.image("https://i.imgur.com/UbOXYAU.png")

st.title("Mapa interactivo con WMS de Madrid")

# Centro aproximado de la ciudad de Madrid
center_madrid = [40.4168, -3.7038]
zoom_madrid = 11

# Diccionario de servicios WMS
wms_layers = {
    "Cartografía General de Madrid": {
        "url": "https://sigma.madrid.es/vector/services/MAPAS_BASE/CARTOBASE_LINEAS_WGS84/MapServer/WMSServer",
        "layers": "0"
    },
    "Mapa de Vegetación (2022)": {
        "url": "https://georaster.madrid.es/ApolloCatalogWMSpublic/service.svc/get",
        "layers": "ESTRATOS_VEGETALES_VR2022"
    }
}

col1, col2 = st.columns([4, 1])
wms_names = list(wms_layers.keys())

with col2:
    selected_wms = st.selectbox("Selecciona una capa WMS:", wms_names)

with col1:
    # Crear el mapa centrado en Madrid sin basemap
    m = leafmap.Map(
        center=center_madrid,
        zoom=zoom_madrid,
        locate_control=True,
        latlon_control=True,
        draw_export=True,
        minimap_control=True
    )

    # Añadir la capa WMS seleccionada
    wms_info = wms_layers[selected_wms]
    m.add_wms_layer(
        url=wms_info["url"],
        layers=wms_info["layers"],
        name=selected_wms,
        format="image/png",
        transparent=True
    )

    m.to_streamlit(height=700)



