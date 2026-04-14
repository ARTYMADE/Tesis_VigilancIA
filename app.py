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
            letter-spacing: 1px;
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
    try:
        st.image("LogoCarabineros.png", width=110)
    except:
        st.error("Archivo LogoCarabineros.png no encontrado.")

with col2:
    st.title("VigilancIA Carabineros")
    st.subheader("Plataforma de Integración Comunitaria - Oficina MICC")

st.divider()

# --- LÓGICA FUNCIONAL (CONEXIÓN GOOGLE SHEETS) ---
CLAVE_ADMIN = "MICC2026" 
CARPETA_RESPALDOS = "respaldos"
URL_PLANILLA = "https://docs.google.com/spreadsheets/d/16lLBrbvViyNMa6cQFQgDqr6UP5He0NhG40YslkSSoVg/edit?gid=0#gid=0"

# Crear carpeta de fotos si no existe para la sesión actual
if not os.path.exists(CARPETA_RESPALDOS):
    os.makedirs(CARPETA_RESPALDOS)

# Conexión con la nube
conn = st.connection("gsheets", type=GSheetsConnection)

def categorizar_con_ia(texto):
    texto = texto.lower()
    muy_alto = ["arma", "pistola", "disparo", "balacera", "escopeta", "armamento", "fuego", "homicidio"]
    alto = ["droga", "trafico", "pasta base", "marihuana", "venta", "robo", "asalto", "vif", "violencia"]
    medio = ["luz", "iluminacion", "foco", "oscuro", "sitio eriazo", "eriazo", "plaza", "baldío"]
    bajo = ["basura", "perro", "escombros", "ruido", "feria", "patente"]
    for palabra in muy_alto:
        if palabra in texto: return "1. MUY ALTO"
    for palabra in alto:
        if palabra in texto: return "2. ALTO"
    for palabra in medio:
        if palabra in texto: return "3. MEDIO"
    for palabra in bajo:
        if palabra in texto: return "4. BAJO"
    return "5. SIN CATEGORIZAR"

def guardar_datos(nombre, apellido, rut, descripcion, direccion, comuna, prioridad, ruta_foto):
    nuevo_registro = pd.DataFrame([{
        "Nombre": nombre, "Apellido": apellido, "RUT": rut,
        "Requerimiento": descripcion, "Direccion": direccion,
        "Comuna": comuna, "Prioridad_IA": prioridad, "Foto_Evidencia": ruta_foto
    }])
    try:
        df_existente = conn.read(spreadsheet=URL_PLANILLA, worksheet="Hoja 1")
        df_final = pd.concat([df_existente, nuevo_registro], ignore_index=True)
        conn.update(spreadsheet=https://docs.google.com/spreadsheets/d/16lLBrbvViyNMa6cQFQgDqr6UP5He0NhG40YslkSSoVg/edit?usp=sharing, worksheet="Hoja 1", data=df_final) # Línea 99 corregida
    except:
        conn.update(spreadsheet=https://docs.google.com/spreadsheets/d/16lLBrbvViyNMa6cQFQgDqr6UP5He0NhG40YslkSSoVg/edit?usp=sharing, worksheet="Hoja 1", data=nuevo_registro) # Línea 101 corregida

# --- INTERFAZ ---
st.sidebar.markdown("<h2 style='color:#D4AF37; text-align:center;'>CONTROL MICC</h2>", unsafe_allow_html=True)
menu = ["Inicio", "Ingresar Requerimiento", "Panel Administrativo MICC"]
opcion = st.sidebar.selectbox("Seleccione Función:", menu)

if opcion == "Inicio":
    st.write("### Bienvenido al Sistema de Gestión Territorial")
    st.markdown('<div style="background-color: #002D20; padding: 20px; border-radius: 10px; border: 1px solid #D4AF37;">Terminal de procesamiento de datos modelo MICC. Conectado a la nube.</div>', unsafe_allow_html=True)

elif opcion == "Ingresar Requerimiento":
    st.write("### Formulario Institucional")
    c1, c2 = st.columns(2)
    with c1:
        nombre = st.text_input("Nombre (Opcional)")
        apellido = st.text_input("Apellido (Opcional)")
    with c2:
        rut = st.text_input("RUT (Obligatorio)")
        comuna = st.text_input("Comuna")
    direccion = st.text_input("Dirección / Intersección")
    descripcion = st.text_area("Relato del Requerimiento (Obligatorio)")
    foto = st.file_uploader("Adjuntar Fotografía", type=["jpg", "png", "jpeg"])
    
    if st.button("PROCESAR REGISTRO"):
        if rut and descripcion:
            ruta_foto_final = "Sin Registro"
            if foto:
                nombre_archivo = f"{rut}_{foto.name}".replace(" ", "_")
                ruta_foto_final = os.path.join(CARPETA_RESPALDOS, nombre_archivo)
                with open(ruta_foto_final, "wb") as f:
                    f.write(foto.getbuffer())
            prioridad = categorizar_con_ia(descripcion)
            guardar_datos(nombre or "S/N", apellido or "S/A", rut, descripcion, direccion, comuna, prioridad, ruta_foto_final)
            st.success(f"REGISTRO EXITOSO: {prioridad}")
        else:
            st.error("ERROR: RUT y Relato son obligatorios.")

elif opcion == "Panel Administrativo MICC":
    st.write("### Mando Administrativo")
    password = st.text_input("Clave Institucional", type="password")
    if st.button("INGRESAR AL PANEL"):
        if password == CLAVE_ADMIN:
            try:
                df = conn.read(spreadsheet=URL_PLANILLA)
                st.dataframe(df.sort_values(by="Prioridad_IA"), use_container_width=True)
                st.write("### Visor de Evidencias")
                for index, row in df.iterrows():
                    if 'Foto_Evidencia' in df.columns and str(row['Foto_Evidencia']) != "Sin Registro":
                        if os.path.exists(str(row['Foto_Evidencia'])):
                            with st.expander(f"Evidencia: {row['RUT']}"):
                                st.image(row['Foto_Evidencia'])
            except Exception as e:
                st.error(f"Error al cargar datos o visor: {e}")
        else:
            st.error("Clave Incorrecta.")

# --- 4. FOOTER ---
st.markdown('<div class="footer">App desarrollada solo con fines academicos, y funciona como Beta</div>', unsafe_allow_html=True)
