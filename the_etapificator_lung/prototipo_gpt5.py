import streamlit as st

# Tu diccionario (ejemplo abreviado; usa el tuyo completo)
tnm9_definiciones_t_clinico = {
    "cTX": "El tumor primario no puede ser evaluado...",
    "cT0": "Sin evidencia de tumor primario",
    # ...
}

T2_FEATURES = [
    "Invade pleura visceral",
    "Invade un lóbulo adyacente",
    "Involucra bronquio principal (hasta pero sin incluir carina)",
    "Atelectasia/neumonitis obstructiva… hasta hilio, parte o todo el pulmón",
]

T3_FEATURES = [
    "Invade pleura parietal o pared torácica",
    "Invade pericardio, nervio frénico o vena ácigos",
    "Invade raíces nerviosas torácicas (T1, T2) o ganglio estrellado",
    "Nódulos separados en el mismo lóbulo",
]

T4_FEATURES = [
    "Invade mediastino (excepto estructuras T3), timo, tráquea, carina, NLR, vago, esófago o diafragma",
    "Invade corazón o grandes vasos…",
    "Invade vasos subclavios, cuerpo vertebral, lámina, canal espinal, raíces cervicales o plexo braquial…",
    "Nódulos separados en lóbulo ipsilateral diferente",
]

def clasificar_ct(evaluable: bool, hay_tumor: bool, tam_cm: float,
                  t2_sel: list[str], t3_sel: list[str], t4_sel: list[str]) -> str:
    if not evaluable:
        return "cTX"
    if not hay_tumor:
        return "cT0"

    # Precedencia por criterios
    if t4_sel:
        return "cT4"
    if t3_sel:
        return "cT3"

    # T2 por criterios (cuando aplica) o por tamaño
    if tam_cm <= 4 and t2_sel:
        # si <=4 y tiene features, es T2 (a si >3, si no, T2 igualmente por criterio, pero tu set usa T2/T2a/T2b)
        # aquí puedes decidir devolver cT2 o cT2a según tu preferencia operacional; lo más consistente:
        if tam_cm > 3:
            return "cT2a"
        else:
            return "cT2"  # porque tu definición general permite ≤4 con features
    # Por tamaño puro
    if tam_cm > 7:
        return "cT4"
    if tam_cm > 5:
        return "cT3"
    if tam_cm > 4:
        return "cT2b"
    if tam_cm > 3:
        return "cT2a"
    # <=3: subcategorías
    if tam_cm <= 1:
        return "cT1a"
    if tam_cm <= 2:
        return "cT1b"
    return "cT1c"

st.title("TNM9 – Clasificación rápida del T clínico")

col1, col2 = st.columns([1, 1])

with col1:
    evaluable_str = st.selectbox("¿Tumor primario evaluable por imágenes/broncoscopía?", ["Sí", "No"])
    evaluable = (evaluable_str == "Sí")

    if evaluable:
        hay_tumor_str = st.selectbox("¿Hay evidencia de tumor primario?", ["Sí", "No"])
        hay_tumor = (hay_tumor_str == "Sí")
    else:
        hay_tumor = False

    if evaluable and hay_tumor:
        tam_cm = st.number_input("Tamaño máximo (cm)", min_value=0.0, max_value=20.0, step=0.1, value=0.0)
    else:
        tam_cm = 0.0

with col2:
    t2_sel, t3_sel, t4_sel = [], [], []

    if evaluable and hay_tumor:
        # Mostrar solo lo necesario según tamaño (divulgación progresiva)
        if tam_cm <= 4:
            t2_sel = st.multiselect("Características (posible T2 por criterios)", T2_FEATURES)

        if tam_cm <= 7:
            t3_sel = st.multiselect("Características (posible T3)", T3_FEATURES)
            t4_sel = st.multiselect("Características (posible T4)", T4_FEATURES)
        # Si >7, no preguntar T4: ya es T4 por tamaño

ct = clasificar_ct(evaluable, hay_tumor, tam_cm, t2_sel, t3_sel, t4_sel)

st.divider()
st.metric("Resultado (cT)", ct)

with st.expander("Ver definición del cT calculado"):
    st.write(tnm9_definiciones_t_clinico.get(ct, "Definición no disponible en el diccionario actual."))