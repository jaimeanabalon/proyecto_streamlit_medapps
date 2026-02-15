import streamlit as st
from datetime import date

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Generador de Notas Oncológicas", page_icon="🧬", layout="wide")

# --- FUNCIONES DE SOPORTE (Lógica Médica) ---
def calcular_bsa(peso, talla):
    """
    Calcula la Superficie Corporal usando la fórmula de DuBois & DuBois.
    Peso en kg, Talla en cm.
    """
    if peso > 0 and talla > 0:
        # Fórmula: 0.007184 * weight^0.425 * height^0.725
        bsa = 0.007184 * (peso ** 0.425) * (talla ** 0.725)
        return round(bsa, 2)
    return 0.0

def generar_encabezado_paciente(nombre, edad, ecog, peso, talla):
    bsa = calcular_bsa(peso, talla)
    return f"""**Paciente:** {nombre} | **Edad:** {edad} años | **ECOG:** {ecog}
**Antropometría:** Peso: {peso}kg | Talla: {talla}cm | **SC (DuBois): {bsa} m²**
---"""

# --- BARRA LATERAL (Navegación) ---
st.sidebar.title("🧬 Onco-Notes")
st.sidebar.info("Herramienta de generación rápida de registros clínicos.")
tipo_nota = st.sidebar.radio(
    "Seleccione tipo de nota:",
    ["1. Ingreso / Primera Consulta", 
     "2. Control Quimioterapia", 
     "3. Toxicidad Inmunoterapia (irAE)",
     "4. Checklist Seguridad"]
)

# --- ÁREA PRINCIPAL ---
st.title(f"📝 {tipo_nota}")

# Datos comunes (siempre visibles arriba para no reingresar si cambias de nota rapido)
with st.expander("Datos Basales del Paciente (Click para desplegar)", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        nombre = st.text_input("Nombre / Iniciales", "Paciente Anónimo")
        edad = st.number_input("Edad", min_value=1, max_value=120, value=60)
    with col2:
        peso = st.number_input("Peso (kg)", value=70.0)
        talla = st.number_input("Talla (cm)", value=170.0)
    with col3:
        ecog = st.selectbox("ECOG Performance Status", [0, 1, 2, 3, 4])

# --- LÓGICA SEGÚN TIPO DE NOTA ---

if "Ingreso" in tipo_nota:
    st.subheader("Detalles del Caso")
    diag_principal = st.text_input("Diagnóstico Principal (Ej: Adenocarcioma Pulmonar)")
    estadio = st.text_input("Estadío (TNM 8va)", "IVB")
    bio_mol = st.text_area("Biología Molecular (Mutaciones, PD-L1, MSI)", "PD-L1: <1%, EGFR: WT, ALK: Negativo")
    
    plan_tto = st.text_input("Esquema Propuesto", "Carboplatino / Pemetrexed")
    
    # Botón Generador
    if st.button("Generar Nota de Ingreso"):
        texto_final = f"""# INGRESO ONCOLOGÍA MÉDICA
{generar_encabezado_paciente(nombre, edad, ecog, peso, talla)}

**Diagnóstico:** {diag_principal}
**Estadío:** {estadio}
**Biología Molecular:** {bio_mol}

## Historia Resumida
Paciente de {edad} años, con ECOG {ecog}. Se presenta para evaluación de tratamiento sistémico.

## Plan
1. **Esquema:** {plan_tto}
2. **Consentimiento Informado:** Discutido y explicado.
3. **Soporte:** Se ajustan analgésicos y antieméticos.
"""
        st.code(texto_final, language="markdown")


elif "Control Quimioterapia" in tipo_nota:
    st.subheader("Evaluación del Ciclo")
    col_a, col_b = st.columns(2)
    with col_a:
        ciclo_n = st.number_input("Número de Ciclo a recibir", value=2)
        tolerancia_prev = st.selectbox("Tolerancia Ciclo Anterior", ["Buena", "Regular", "Mala"])
    
    st.markdown("### Toxicidades (CTCAE v5.0)")
    # Usamos sliders para graduar rápido
    col_tox1, col_tox2, col_tox3 = st.columns(3)
    nau_vom = col_tox1.slider("Náuseas/Vómitos (Grado)", 0, 4, 0)
    diarrea = col_tox2.slider("Diarrea (Grado)", 0, 4, 0)
    neuro = col_tox3.slider("Neuropatía (Grado)", 0, 4, 0)
    
    laboratorio = st.text_input("Labs Relevantes (ANC / Plq / Crea)", "ANC > 1500, Plq > 100k, Crea Normal")
    
    if st.button("Generar Control de Quimio"):
        texto_final = f"""# CONTROL PRE-QUIMIOTERAPIA (Ciclo #{ciclo_n})
{generar_encabezado_paciente(nombre, edad, ecog, peso, talla)}

**Subjetivo:**
* **Tolerancia Ciclo Anterior:** {tolerancia_prev}
* **Toxicidad Aguda:**
    * Náuseas: G{nau_vom}
    * Diarrea: G{diarrea}
    * Neuropatía: G{neuro}

**Laboratorio:** {laboratorio}

**Plan:**
1. Autorizar Ciclo #{ciclo_n} ({'100% Dosis' if ecog <= 2 else 'Evaluar ajuste'}).
2. Premedicación estándar.
"""
        st.code(texto_final, language="markdown")


elif "Toxicidad Inmunoterapia" in tipo_nota:
    st.warning("⚠️ Checklist para Inhibidores de Checkpoint (ICI)")
    
    st.markdown("Marque **SÍ** presenta síntomas nuevos:")
    col_i1, col_i2 = st.columns(2)
    with col_i1:
        resp = st.checkbox("Respiratorio (Tos/Disnea) - Neumonitis?")
        dig = st.checkbox("Digestivo (Diarrea/Colitis)")
        derm = st.checkbox("Piel (Rash/Prurito)")
    with col_i2:
        endo = st.checkbox("Endocrino (Fatiga/Tiroides)")
        hep = st.checkbox("Hepático (Ictericia/Coluria)")
        neuro_ir = st.checkbox("Neurológico/Reumatológico")
        
    conducta = st.selectbox("Conducta Clínica", ["Continuar Tratamiento", "Suspender Temporalmente", "Suspender Definitivo", "Iniciar Corticoides"])

    if st.button("Generar Nota irAE"):
        # Lógica simple para construir la lista de positivos
        hallazgos = []
        if resp: hallazgos.append("Respiratorio (Sospecha Neumonitis)")
        if dig: hallazgos.append("Digestivo (Sospecha Colitis)")
        if derm: hallazgos.append("Dermatológico")
        if endo: hallazgos.append("Endocrino")
        if hep: hallazgos.append("Hepático")
        
        texto_hallazgos = ", ".join(hallazgos) if hallazgos else "Sin síntomas de alarma actuales."

        texto_final = f"""# SCREENING TOXICIDAD INMUNOMEDIADA
{generar_encabezado_paciente(nombre, edad, ecog, peso, talla)}

**Revisión por Sistemas (irAEs):**
* **Hallazgos positivos:** {texto_hallazgos}

**Conducta:**
* {conducta}
* Educación sobre signos de alarma entregada.
"""
        st.code(texto_final, language="markdown")

elif "Checklist Seguridad" in tipo_nota:
    st.subheader("Pausa de Seguridad")
    c1 = st.checkbox("Consentimiento Informado Firmado")
    c2 = st.checkbox("Comité Oncológico Concordante")
    c3 = st.checkbox("Receta Quimioterapia + Premedicación")
    c4 = st.checkbox("Receta Soporte Domiciliario")
    
    if st.button("Generar Cierre"):
        texto_final = f"""# CHECKLIST DE SEGURIDAD
- [ {'x' if c1 else ' '} ] Consentimiento Informado
- [ {'x' if c2 else ' '} ] Comité Oncológico
- [ {'x' if c3 else ' '} ] Receta Quimio
- [ {'x' if c4 else ' '} ] Receta Soporte
"""
        st.code(texto_final, language="markdown")

