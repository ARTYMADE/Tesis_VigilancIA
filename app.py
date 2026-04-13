import streamlit as st
import pandas as pd
import os
from streamlit_gsheets import GSheetsConnection

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="VigilancIA Carab. - Oficina MICC", 
    page_icon="👮‍♂️", 
    layout="wide"
)

# --- 2. DISEÑO TÁCTICO: FONDO VERDE, LETRAS BLANCAS, SIDEBAR NEGRO ---
st.markdown("""
    <style>
        .stApp { background-color: #004D40; }
        [data-testid="stSidebar"] {
            background-color: #000000 !important;
            border-right: 1px solid #D4AF37;
        }
        h1, h2, h3, p, span, label, .stMarkdown { color: #FFFFFF !important; }
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            background-color: #002D20 !important;
            color: #FFFFFF !important;
            border: 1px solid #D4AF37 !important;
            border-radius: 4px !important;
        }
        label {
            font-weight: bold !important;
            text-transform: uppercase;
            font-size: 0.9em !important;
        }
        .stButton>button {
            background-color: #D4AF37; color: #000000; font-weight: bold;
            border: none; border-radius: 5px; padding: 12px 20px; width: 100%;
        }
        .stButton>button:hover { background-color: #B8952E; color: #FFFFFF; }
        .stSelectbox div[data-baseweb="select"] { background-color: #1A1A1A !important; color: #FFFFFF !important; }
        .footer {
            position: fixed; left: 0; bottom: 0; width: 100%;
            background-color: transparent; color: #CCCCCC !important;
            text-align: center; font-size: 0.7em; padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. ENCABEZADO ---
col1, col2 = st.columns([1, 6])
with col1:
    if os.path.exists("LogoCarabineros.png"):
        st.image("LogoCarabineros.png", width=110)

with col2:
    st.title("VigilancIA Carabineros")
    st.subheader("Plataforma de Integración Comunitaria - Oficina MICC")

st.divider()

# --- LÓGICA FUNCIONAL (SOLO NUBE) ---
CLAVE_ADMIN = "MICC2026" 
URL_PLANILLA = "https://docs.google.com/spreadsheets/d/16lLBrbvViyNMa6cQFQgDqr6UP5He0NhG40YslkSSoVg/edit?gid=0#gid=0"

# Conexión con Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def categorizar_con_ia(texto):
    texto = texto.lower()
    muy_alto = ["arma", "pistola", "disparo", "balacera", "homicidio"]
    alto = ["droga", "trafico", "robo", "asalto", "vif"]
    if any(p in texto for p in muy_alto): return "1. MUY ALTO"
    if any(p in texto for p in alto): return "2. ALTO"
    return "3. OTROS"

def guardar_datos(nombre, apellido, rut, descripcion, comuna, prioridad):
    nuevo_df = pd.DataFrame([{
        "Nombre": nombre, "Apellido": apellido, "RUT": rut,
        "Requerimiento": descripcion, "Comuna": comuna, "Prioridad_IA": prioridad
    }])
    try:
        df_existente = conn.read(spreadsheet=URL_PLANILLA)
        df_final = pd.concat([df_existente, nuevo_df], ignore_index=True)
        conn.update(spreadsheet=URL_PLANILLA, data=df_final)
    except:
        conn.update(spreadsheet=URL_PLANILLA, data=nuevo_df)

# --- INTERFAZ ---
st.sidebar.markdown("<h2 style='color:#D4AF37; text-align:center;'>CONTROL MICC</h2>", unsafe_allow_html=True)
opcion = st.sidebar.selectbox("Seleccione Función:", ["Inicio", "Ingresar Requerimiento", "Panel Administrativo MICC"])

if opcion == "Inicio":
    st.write("### Bienvenido al Sistema de Gestión Territorial")
    st.success("✅ Sistema conectado exitosamente a la nube de Google.")

elif opcion == "Ingresar Requerimiento":
    st.write("### Formulario Institucional")
    c1, c2 = st.columns(2)
    with c1:
        nombre = st.text_input("Nombre")
        apellido = st.text_input("Apellido")
    with c2:
        rut = st.text_input("RUT")
        comuna = st.text_input("Comuna")
    descripcion = st.text_area("Relato del Requerimiento")
    
    if st.button("PROCESAR REGISTRO"):
        if rut and descripcion:
            prioridad = categorizar_con_ia(descripcion)
            guardar_datos(nombre or "S/N", apellido or "S/A", rut, descripcion, comuna, prioridad)
            st.success(f"REGISTRO GUARDADO EN LA NUBE: {prioridad}")
        else:
            st.error("ERROR: RUT y Relato son obligatorios.")

elif opcion == "Panel Administrativo MICC":
    st.write("### Mando Administrativo")
    password = st.text_input("Clave Institucional", type="password")
    if st.button("INGRESAR AL PANEL"):
        if password == CLAVE_ADMIN:
            try:
                df = conn.read(spreadsheet=URL_PLANILLA)
                st.dataframe(df, use_container_width=True)
            except:
                st.info("Aún no hay datos registrados en la planilla.")
        else:
            st.error("Clave Incorrecta.")

st.markdown('<div class="footer">VigilancIA - Carabineros de Chile - Oficina MICC</div>', unsafe_allow_html=True)
