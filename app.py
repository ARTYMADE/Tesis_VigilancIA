import streamlit as st
import pandas as pd
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="VigilancIA Carab. - Oficina MICC", 
    page_icon="👮‍♂️", 
    layout="wide"
)

# --- 2. DISEÑO TÁCTICO: FONDO VERDE, LETRAS BLANCAS, SIDEBAR NEGRO ---
st.markdown("""
    <style>
        /* Fondo Principal Verde Institucional */
        .stApp {
            background-color: #004D40;
        }
        
        /* Barra lateral Negra */
        [data-testid="stSidebar"] {
            background-color: #000000 !important;
            border-right: 1px solid #D4AF37;
        }
        
        /* TODO EL TEXTO EN BLANCO */
        h1, h2, h3, p, span, label, .stMarkdown {
            color: #FFFFFF !important;
        }

        /* DISEÑO DE CAMPOS DE ENTRADA (Fondo oscuro, borde dorado) */
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            background-color: #002D20 !important;
            color: #FFFFFF !important;
            border: 1px solid #D4AF37 !important;
            border-radius: 4px !important;
        }
        
        /* Etiquetas de los campos resaltadas */
        label {
            font-weight: bold !important;
            text-transform: uppercase;
            font-size: 0.9em !important;
            letter-spacing: 1px;
        }

        /* Botón Institucional Resaltado */
        .stButton>button {
            background-color: #D4AF37; /* Dorado para destacar en el fondo verde */
            color: #000000;
            font-weight: bold;
            border: none;
            border-radius: 5px;
            padding: 12px 20px;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #B8952E;
            color: #FFFFFF;
        }

        /* Estilo para el Menú Desplegable (Selectbox) */
        .stSelectbox div[data-baseweb="select"] {
            background-color: #1A1A1A !important;
            color: #FFFFFF !important;
        }
        
        /* Estilo para las métricas */
        [data-testid="stMetricValue"] {
            color: #D4AF37 !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. ENCABEZADO ---
col1, col2 = st.columns([1, 6])
with col1:
    # Logo de Carabineros
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Logo_de_Carabineros_de_Chile.svg/1024px-Logo_de_Carabineros_de_Chile.svg.png", width=110)
with col2:
    st.title("VigilancIA Carabineros")
    st.subheader("Plataforma de Integración Comunitaria - Oficina MICC")

st.divider()

# --- LÓGICA FUNCIONAL (MANTENIDA) ---
CLAVE_ADMIN = "MICC2026" 

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

def guardar_datos(nombre, apellido, rut, descripcion, direccion, comuna, prioridad):
    archivo = "datos_micc.csv"
    nuevo_registro = {
        "Nombre": [nombre], "Apellido": [apellido], "RUT": [rut],
        "Requerimiento": [descripcion], "Direccion": [direccion],
        "Comuna": [comuna], "Prioridad_IA": [prioridad]
    }
    df_nuevo = pd.DataFrame(nuevo_registro)
    if not os.path.isfile(archivo):
        df_nuevo.to_csv(archivo, index=False, encoding="utf-8")
    else:
        df_nuevo.to_csv(archivo, mode='a', index=False, header=False, encoding="utf-8")

# --- INTERFAZ ---
st.sidebar.markdown("<h2 style='color:#D4AF37; text-align:center;'>CONTROL MICC</h2>", unsafe_allow_html=True)
menu = ["Inicio", "Ingresar Requerimiento", "Panel Administrativo MICC"]
opcion = st.sidebar.selectbox("Seleccione Función:", menu)

if opcion == "Inicio":
    st.write("### Bienvenido al Sistema de Gestión Territorial")
    st.markdown("""
        <div style="background-color: #002D20; padding: 20px; border-radius: 10px; border: 1px solid #D4AF37;">
            <p>Esta terminal permite el ingreso y procesamiento de datos comunitarios bajo el modelo MICC.</p>
            <p>La <b>Inteligencia Artificial</b> categoriza la información para una respuesta eficiente.</p>
        </div>
    """, unsafe_allow_html=True)

elif opcion == "Ingresar Requerimiento":
    st.write("### Formulario Institucional")
    c1, c2 = st.columns(2)
    with c1:
        nombre = st.text_input("Nombres")
        apellido = st.text_input("Apellidos")
    with c2:
        rut = st.text_input("RUT")
        comuna = st.text_input("Comuna")
        
    direccion = st.text_input("Dirección / Intersección")
    descripcion = st.text_area("Relato del Requerimiento")
        
    if st.button("PROCESAR REGISTRO"):
        if nombre and apellido and rut and descripcion:
            prioridad_detectada = categorizar_con_ia(descripcion)
            guardar_datos(nombre, apellido, rut, descripcion, direccion, comuna, prioridad_detectada)
            st.success(f"REGISTRO EXITOSO: {prioridad_detectada}")
        else:
            st.error("ERROR: Complete los datos.")

elif opcion == "Panel Administrativo MICC":
    st.write("### Mando Administrativo")
    password = st.text_input("Clave Institucional", type="password")
    
    if password == CLAVE_ADMIN:
        st.success("AUTORIZADO")
        if os.path.isfile("datos_micc.csv"):
            df = pd.read_csv("datos_micc.csv")
            df_ordenado = df.sort_values(by="Prioridad_IA").reset_index(drop=True)
            # Aplicamos estilo a la tabla para que se vea bien en fondo oscuro
            st.dataframe(df_ordenado, use_container_width=True)
        else:
            st.info("Sin registros.")
    elif password != "":
        st.error("Clave Incorrecta.")