import streamlit as st
import leafmap.foliumap as leafmap
import bcrypt
import jwt
import datetime


# ================= Configuración JWT y usuarios =================
SECRET = st.secrets.get("COOKIE_SECRET", "default_secret_key_32_chars_long_1234")
ADMIN_USERNAME = st.secrets.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD_HASH = st.secrets.get("ADMIN_PASSWORD_HASH", "").encode()

users_db = {ADMIN_USERNAME: ADMIN_PASSWORD_HASH}


def verificar_login(usuario, contraseña):
    if usuario in users_db:
        return bcrypt.checkpw(contraseña.encode(), users_db[usuario])
    return False


def crear_token(username):
    payload = {"sub": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8)}
    return jwt.encode(payload, SECRET, algorithm="HS256")


def verificar_token(token):
    try:
        data = jwt.decode(token, SECRET, algorithms=["HS256"])
        return data["sub"]
    except jwt.PyJWTError:
        return None


# ================= Interfaz Login =================
def login():
    st.title("🔐 Acceso al Sistema de Tickets")
    with st.form("login_form"):
        usuario = st.text_input("Usuario")
        contraseña = st.text_input("Contraseña", type="password")
        if st.form_submit_button("Iniciar sesión"):
            if verificar_login(usuario, contraseña):
                token = crear_token(usuario)
                st.session_state.token = token
                st.session_state.logged_in = True
                st.session_state.usuario = usuario
                st.success(f"✅ Bienvenido/a, {usuario}")
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos")


# ================= Página principal =================
def app():
    st.title("🎫 Home")
    st.write(f"Bienvenido/a {st.session_state.usuario}")

    # Mapa
    m = leafmap.Map(minimap_control=True)
    m.add_basemap("OpenTopoMap")
    m.to_streamlit(height=500, width=1400)

    # Botón logout SOLO si está logueado
    if st.button("Cerrar sesión"):
        for key in ["token", "logged_in", "usuario"]:
            st.session_state.pop(key, None)
        st.rerun()


# ================= Configuración página =================
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

# ================= Lógica de login =================
if "token" in st.session_state:
    usuario = verificar_token(st.session_state.token)
    if usuario:
        st.session_state.logged_in = True
        st.session_state.usuario = usuario
    else:
        st.session_state.logged_in = False

if st.session_state.get("logged_in") and verificar_token(st.session_state.token):
    app()
else:
    login()




