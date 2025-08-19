import streamlit as st
import leafmap.foliumap as leafmap
import bcrypt
import jwt
import datetime

# ================= Configuración página =================
st.set_page_config(layout="wide")  # Solo una vez al inicio

# ================= Configuración JWT y usuarios =================
SECRET = st.secrets.get("COOKIE_SECRET", "default_secret_key_32_chars_long_1234")
ADMIN_USERNAME = st.secrets["ADMIN_USERNAME"]
ADMIN_PASSWORD_HASH = st.secrets["ADMIN_PASSWORD_HASH"].encode("utf-8")  

users_db = {ADMIN_USERNAME: ADMIN_PASSWORD_HASH}


# ================= Inicializar session_state =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "usuario" not in st.session_state:
    st.session_state.usuario = ""
if "token" not in st.session_state:
    st.session_state.token = ""

# ================= Funciones =================
def verificar_login(usuario, contraseña):
    # Comprobar usuario y password
    if usuario == ADMIN_USERNAME:
        return bcrypt.checkpw(contraseña.encode("utf-8"), ADMIN_PASSWORD_HASH)
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

# ================= Login =================
def login():
    st.title("🔐 Login")

    usuario = st.text_input("Usuario")
    contraseña = st.text_input("Contraseña", type="password")

    if st.button("Iniciar sesión"):
        if verificar_login(usuario, contraseña):
            st.success("✅ Acceso concedido")
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
        st.session_state.token = ""
        st.experimental_rerun()

# ================= Lógica principal =================
if st.session_state.logged_in:
    usuario_valido = verificar_token(st.session_state.token)
    if usuario_valido:
        st.session_state.usuario = usuario_valido
        home()
    else:
        st.session_state.logged_in = False
        login()
else:
    login()

