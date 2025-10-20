import streamlit as st
import leafmap.foliumap as leafmap

# Usar ancho completo
st.set_page_config(layout="wide")

# Sidebar
markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""
st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://cdn.pixabay.com/photo/2012/04/01/18/38/park-23939_960_720.png"
st.sidebar.image(logo)

# Page title
st.title("Streamlit for Geospatial Applications")

st.markdown(
    """
    This multipage app template demonstrates various interactive web apps 
    created using [streamlit](https://streamlit.io) and [leafmap](https://leafmap.org).
    """
)

st.header("Instructions")
markdown = """
1. Visit the [GitHub repository](https://github.com/opengeos/streamlit-map-template)
2. Customize the sidebar text and logo in each Python file.
3. Find your favorite emoji from https://emojipedia.org.
4. Add a new app to the `pages/` directory.
"""
st.markdown(markdown)

# Mapa ancho completo
m = leafmap.Map(minimap_control=True)
m.add_basemap("CartoDB.Positron")
m.to_streamlit(height=500, width=1400)  # Fuerza ancho más grande

