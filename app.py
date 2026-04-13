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

        /* DISEÑO DE CAMPOS DE ENTRADA */
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
            background-color: #D4AF37;
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

        .stSelectbox div[data-baseweb="select"] {
            background-color: #1A1A1A !important;
            color: #FFFFFF !important;
        }
        
        [data-testid="stMetricValue"] {
            color: #D4AF37 !important;
        }

        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: transparent;
            color: #CCCCCC !important;
            text-align: center;
            font-size: 0.7em;
            padding: 10px;
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

# --- LÓGICA FUNCIONAL ---
CLAVE_ADMIN = "MICC2026" 
CARPETA_RESPALDOS = "respaldos"
ARCHIVO_CSV = "datos_micc.csv"

if not os.path.exists(CARPETA_RESPALDOS):
    os.makedirs(CARPETA_RESPALDOS)

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
    nuevo_registro = {
        "Nombre": [nombre], "Apellido": [apellido], "RUT": [rut],
        "Requerimiento": [descripcion], "Direccion": [direccion],
        "Comuna": [comuna], "Prioridad_IA": [prioridad], "Foto_Evidencia": [ruta_foto]
    }
    df_nuevo = pd.DataFrame(nuevo_registro)
    if not os.path.isfile(ARCHIVO_CSV):
        df_nuevo.to_csv(ARCHIVO_CSV, index=False, encoding="utf-8")
    else:
        df_nuevo.to_csv(ARCHIVO_CSV, mode='a', index=False, header=False, encoding="utf-8")

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
        nombre = st.text_input("Nombre (Opcional)")
        apellido = st.text_input("Apellido (Opcional)")
    with c2:
        rut = st.text_input("RUT (Obligatorio)")
        comuna = st.text_input("Comuna")
        
    direccion = st.text_input("Dirección / Intersección")
    descripcion = st.text_area("Relato del Requerimiento (Obligatorio)")
    foto = st.file_uploader("Adjuntar Fotografía de Respaldo (Opcional)", type=["jpg", "png", "jpeg"])
        
    if st.button("PROCESAR REGISTRO"):
        if rut and descripcion:
            ruta_foto_final = "Sin Registro"
            if foto is not None:
                nombre_archivo = f"{rut}_{foto.name}".replace(" ", "_")
                ruta_foto_final = os.path.join(CARPETA_RESPALDOS, nombre_archivo)
                with open(ruta_foto_final, "wb") as f:
                    f.write(foto.getbuffer())
            
            final_nombre = nombre if nombre else "S/N"
            final_apellido = apellido if apellido else "S/A"
            prioridad_detectada = categorizar_con_ia(descripcion)
            guardar_datos(final_nombre, final_apellido, rut, descripcion, direccion, comuna, prioridad_detectada, ruta_foto_final)
            st.success(f"REGISTRO EXITOSO: {prioridad_detectada}")
        else:
            st.error("ERROR: El RUT y el Relato son campos obligatorios.")

elif opcion == "Panel Administrativo MICC":
    st.write("### Mando Administrativo")
    password = st.text_input("Clave Institucional", type="password")
    if st.button("INGRESAR AL PANEL"):
        if password == CLAVE_ADMIN:
            if os.path.isfile(ARCHIVO_CSV):
                try:
                    df = pd.read_csv(ARCHIVO_CSV, on_bad_lines='skip', encoding="utf-8")
                    df_ordenado = df.sort_values(by="Prioridad_IA").reset_index(drop=True)
                    st.dataframe(df_ordenado, use_container_width=True)
                    
                    st.write("### Visor de Evidencias Fotográficas")
                    for index, row in df_ordenado.iterrows():
                        if 'Foto_Evidencia' in row and str(row['Foto_Evidencia']) != "Sin Registro":
                            ruta_img = str(row['Foto_Evidencia'])
                            if os.path.exists(ruta_img):
                                with st.expander(f"Evidencia: {row['Nombre']} (RUT: {row['RUT']})"):
                                    st.image(ruta_img, use_container_width=True)
                except Exception as e:
                    st.error(f"Error crítico en base de datos: {e}")
            else:
                st.info("Sin registros en la base de datos.")
        else:
            st.error("Clave Incorrecta.")

# --- 4. FOOTER ---
st.markdown('<div class="footer">Esta App es desarrollada solo con fines academicos, y funciona como Beta</div>', unsafe_allow_html=True)
