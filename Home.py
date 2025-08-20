import streamlit as st
import leafmap.foliumap as leafmap
import bcrypt

# ================= Configuración página =================
st.set_page_config(layout="wide")  # Solo una vez al inicio


# ================= Configuración usuarios =================
ADMIN_USERNAME = st.secrets.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD_HASH = st.secrets.get("ADMIN_PASSWORD_HASH", "")

# Aseguramos que siempre sea bytes (bcrypt lo exige)
if isinstance(ADMIN_PASSWORD_HASH, str):
    ADMIN_PASSWORD_HASH = ADMIN_PASSWORD_HASH.encode()

users_db = {ADMIN_USERNAME: ADMIN_PASSWORD_HASH}

# ================= Función de verificación =================
def verificar_login(usuario, contraseña):
    if usuario in users_db and users_db[usuario]:
        try:
            return bcrypt.checkpw(contraseña.encode(), users_db[usuario])
        except ValueError:
            # Por si el hash está corrupto o vacío
            return False
    return False

# ================= Login =================
def login():
    st.title("🔐 Acceso al Sistema de Tickets")
    with st.form("login_form"):
        usuario = st.text_input("Usuario")
        contraseña = st.text_input("Contraseña", type="password")
        if st.form_submit_button("Iniciar sesión"):
            if verificar_login(usuario, contraseña):
                st.session_state.logged_in = True
                st.session_state.usuario = usuario
                st.success(f"✅ Bienvenido/a, {usuario}")
                st.balloons()
                st.experimental_rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos")

# ================= Home =================
def home():
    st.title("🏠 Home")
    st.write(f"Bienvenido/a {st.session_state.usuario}!")

    # Sidebar
    st.sidebar.title("About")
    st.sidebar.info("A Streamlit map template\n<https://github.com/opengeos/streamlit-map-template>")
    st.sidebar.image("https://cdn.pixabay.com/photo/2012/04/01/18/38/park-23939_960_720.png")

    # Mapa
    m = leafmap.Map(minimap_control=True)
    m.add_basemap("OpenTopoMap")
    m.to_streamlit(height=500, width=1400)

    # Sistema de Tickets (ejemplo)
    st.subheader("🎫 Sistema de Tickets")
    st.write("Aquí puedes gestionar tus tickets...")

    # Logout
    if st.button("Cerrar sesión"):
        st.session_state.logged_in = False
        st.session_state.usuario = ""
        st.experimental_rerun()

# ================= Lógica principal =================
if st.session_state.logged_in:
    home()
else:
    login()

