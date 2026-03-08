import streamlit as st
import pdfplumber
import re
import io
import pandas as pd

# ─── Configuración de página ────────────────────────────────────────────────
st.set_page_config(
    page_title="Extractor de Párrafos PDF",
    page_icon="📄",
    layout="wide",
)

# ─── CSS personalizado ───────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', sans-serif;
    }

    .stApp {
        background-color: #0f1117;
        color: #e0e0e0;
    }

    .titulo-principal {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 2rem;
        font-weight: 600;
        color: #00d4aa;
        border-bottom: 2px solid #00d4aa33;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }

    .parrafo-card {
        background: #1a1d26;
        border-left: 3px solid #00d4aa;
        border-radius: 0 8px 8px 0;
        padding: 0.8rem 1.2rem;
        margin-bottom: 0.6rem;
        font-size: 0.92rem;
        line-height: 1.7;
        color: #d0d0d0;
    }

    .numero-parrafo {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.72rem;
        color: #00d4aa;
        font-weight: 600;
        letter-spacing: 0.08em;
        margin-bottom: 0.3rem;
    }

    .stat-box {
        background: #1a1d26;
        border: 1px solid #00d4aa33;
        border-radius: 8px;
        padding: 0.8rem 1.2rem;
        text-align: center;
    }

    .stat-value {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1.8rem;
        color: #00d4aa;
        font-weight: 600;
    }

    .stat-label {
        font-size: 0.78rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .filtro-info {
        font-size: 0.8rem;
        color: #888;
        margin-top: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

# ─── Funciones ───────────────────────────────────────────────────────────────

def extraer_texto_pdf(archivo_pdf) -> list[str]:
    """Extrae texto del PDF página por página usando pdfplumber."""
    paginas_texto = []
    with pdfplumber.open(archivo_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            if texto:
                paginas_texto.append(texto)
    return paginas_texto

def limpiar_y_segmentar_parrafos(paginas_texto: list[str], min_palabras: int = 5) -> list[dict]:
    """
    Limpia el texto y segmenta en párrafos numerados.
    Filtra líneas muy cortas (encabezados, números de página, etc.).
    """
    texto_total = "\n".join(paginas_texto)

    # Dividir en bloques separados por líneas en blanco
    bloques = re.split(r'\n\s*\n', texto_total)

    parrafos = []
    numero = 1

    for bloque in bloques:
        # Limpiar espacios y saltos internos
        bloque_limpio = " ".join(bloque.split())

        # Filtrar si tiene menos de N palabras (líneas de encabezado, pies de página)
        palabras = bloque_limpio.split()
        if len(palabras) < min_palabras:
            continue

        parrafos.append({
            "N°": numero,
            "Párrafo": bloque_limpio,
            "Palabras": len(palabras),
            "Caracteres": len(bloque_limpio),
        })
        numero += 1

    return parrafos

def generar_txt(parrafos: list[dict]) -> str:
    """Genera texto plano numerado para descarga."""
    lineas = []
    for p in parrafos:
        lineas.append(f"[{p['N°']:04d}] {p['Párrafo']}\n")
    return "\n".join(lineas)

# ─── Interfaz ────────────────────────────────────────────────────────────────

st.markdown('<div class="titulo-principal">📄 Extractor de Párrafos PDF</div>', unsafe_allow_html=True)
st.markdown("Sube un PDF, extrae el texto y numera cada párrafo automáticamente.")

st.divider()

# Sidebar con opciones
with st.sidebar:
    st.markdown("### ⚙️ Configuración")
    min_palabras = st.slider(
        "Mínimo de palabras por párrafo",
        min_value=1, max_value=30, value=5,
        help="Párrafos con menos palabras que este umbral serán descartados (encabezados, números de página, etc.)"
    )
    mostrar_estadisticas = st.checkbox("Mostrar estadísticas por párrafo", value=True)
    modo_tabla = st.checkbox("Ver como tabla (DataFrame)", value=False)

    st.markdown("---")
    st.markdown("**Formatos de descarga disponibles:**")
    st.markdown("- `.txt` numerado  \n- `.csv` con metadatos")

# Carga del archivo
archivo = st.file_uploader("Selecciona un archivo PDF", type=["pdf"])

if archivo is not None:
    with st.spinner("Extrayendo texto del PDF..."):
        try:
            paginas = extraer_texto_pdf(archivo)
            parrafos = limpiar_y_segmentar_parrafos(paginas, min_palabras=min_palabras)
        except Exception as e:
            st.error(f"Error al procesar el PDF: {e}")
            st.stop()

    if not parrafos:
        st.warning("No se encontraron párrafos válidos. Intenta reducir el mínimo de palabras.")
        st.stop()

    # ── Estadísticas globales ──
    df = pd.DataFrame(parrafos)
    total_palabras = df["Palabras"].sum()
    total_chars = df["Caracteres"].sum()
    promedio_palabras = df["Palabras"].mean()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="stat-box"><div class="stat-value">{len(paginas)}</div><div class="stat-label">Páginas</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-box"><div class="stat-value">{len(parrafos)}</div><div class="stat-label">Párrafos</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-box"><div class="stat-value">{total_palabras:,}</div><div class="stat-label">Palabras</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="stat-box"><div class="stat-value">{promedio_palabras:.0f}</div><div class="stat-label">Palabras/párrafo</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Búsqueda ──
    busqueda = st.text_input("🔍 Filtrar párrafos por palabra o frase", placeholder="ej: inmunoterapia, supervivencia...")
    if busqueda:
        parrafos_filtrados = [p for p in parrafos if busqueda.lower() in p["Párrafo"].lower()]
        st.markdown(f'<div class="filtro-info">Mostrando {len(parrafos_filtrados)} de {len(parrafos)} párrafos que contienen "<b>{busqueda}</b>"</div>', unsafe_allow_html=True)
    else:
        parrafos_filtrados = parrafos

    # ── Visualización ──
    if modo_tabla:
        df_filtrado = pd.DataFrame(parrafos_filtrados)
        st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
    else:
        for p in parrafos_filtrados:
            texto_mostrar = p["Párrafo"]
            # Resaltar búsqueda
            if busqueda:
                texto_mostrar = re.sub(
                    f"({re.escape(busqueda)})",
                    r'<mark style="background:#00d4aa33; color:#00d4aa; padding:0 2px;">\1</mark>',
                    texto_mostrar,
                    flags=re.IGNORECASE
                )

            extra = f" · {p['Palabras']} palabras · {p['Caracteres']} chars" if mostrar_estadisticas else ""

            st.markdown(
                f"""
                <div class="parrafo-card">
                    <div class="numero-parrafo">PÁRRAFO {p['N°']:04d}{extra}</div>
                    {texto_mostrar}
                </div>
                """,
                unsafe_allow_html=True
            )

    # ── Descargas ──
    st.markdown("---")
    st.markdown("### 💾 Descargar resultados")

    col_a, col_b = st.columns(2)

    txt_content = generar_txt(parrafos_filtrados)
    with col_a:
        st.download_button(
            label="⬇️ Descargar como .txt numerado",
            data=txt_content.encode("utf-8"),
            file_name="parrafos_numerados.txt",
            mime="text/plain",
        )

    csv_content = pd.DataFrame(parrafos_filtrados).to_csv(index=False).encode("utf-8")
    with col_b:
        st.download_button(
            label="⬇️ Descargar como .csv (con metadatos)",
            data=csv_content,
            file_name="parrafos_numerados.csv",
            mime="text/csv",
        )

else:
    st.info("☝️ Sube un archivo PDF para comenzar.")