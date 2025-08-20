import streamlit as st
import leafmap.foliumap as leafmap
import bcrypt

# ================= Configuración página =================
st.set_page_config(layout="wide")

# ================= Leer secretos =================
ADMIN_USERNAME = st.secrets.get("ADMIN_USERNAME")
ADMIN_PASSWORD_HASH = st.secrets.get("ADMIN_PASSWORD_HASH").strip()  # limpiar espacios
hash_bytes = ADMIN_PASSWORD_HASH.encode()

users_db = {ADMIN_USERNAME: hash_bytes}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "usuario" not in st.session_state:
    st.session_state.usuario = ""

# función de verificación
def verificar_login(usuario, contraseña):
    if usuario not in users_db:
        return False
    return bcrypt.checkpw(contraseña.encode(), users_db[usuario])

# ================= Login =================
def login():
    st.title("🔐 Acceso al Sistema de Tickets")

    with st.form("login_form"):
        usuario_input = st.text_input("Usuario", placeholder="Tu usuario").strip()
        contraseña_input = st.text_input("Contraseña", type="password", placeholder="Tu contraseña").strip()
        submit = st.form_submit_button("Iniciar sesión")

    # ===== Debug temporal =====
    with st.expander("🔎 Debug Secrets (temporal)"):
        st.write("Usuario esperado:", f"`{ADMIN_USERNAME}`")
        st.write("Hash esperado (longitud):", len(ADMIN_PASSWORD_HASH))
        st.write("Primeros 10 chars del hash:", ADMIN_PASSWORD_HASH[:10])

    # ===== Verificación login =====
    if submit:
        if verificar_login(usuario_input, contraseña_input):
            st.session_state.logged_in = True
            st.session_state.usuario = usuario_input
            st.success(f"✅ Bienvenido/a, {usuario_input}")
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



