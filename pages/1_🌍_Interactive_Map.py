import streamlit as st
import leafmap.foliumap as leafmap

st.sidebar.title("About")
st.sidebar.info("Visualizador con WMS de Madrid")
st.sidebar.image("https://i.imgur.com/UbOXYAU.png")

st.title("Mapa interactivo con WMS de Madrid")

# Bounding box aproximado de la ciudad de Madrid
bounds_madrid = [-3.889, 40.312, -3.517, 40.643]  # [minx, miny, maxx, maxy]

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
    m = leafmap.Map(
        locate_control=True,
        latlon_control=True,
        draw_export=True,
        minimap_control=True
        # No se incluye ningún mapa base
    )

    # Centrar el mapa sobre Madrid
    m.set_bounds(bounds_madrid)

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


