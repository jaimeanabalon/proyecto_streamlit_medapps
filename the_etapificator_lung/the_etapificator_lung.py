import streamlit as st
import pandas as pd

# Aplicación pequeña para determinar el estadío del cáncer de pulmón según la clasificación TNM 7,8 y 9 edición

def etapificator_lung(t, n, m, edition=8):
    if edition == 7:
        if m == 1:
            return "IV"
        elif n == 3:
            return "IIIB"
        elif n == 2:
            if t in [3, 4]:
                return "IIIA"
            else:
                return "IIIB"
        elif n == 1:
            if t in [3, 4]:
                return "IIA"
            else:
                return "IB"
        else:  # n == 0
            if t == 4:
                return "IB"
            elif t == 3:
                return "IA"
            else:
                return "IA"
    elif edition == 8:
        if m == 1:
            return "IV"
        elif n == 3:
            return "IIIC"
        elif n == 2:
            if t in [3, 4]:
                return "IIIA"
            else:
                return "IIIB"
        elif n == 1:
            if t in [3, 4]:
                return "IIA"
            else:
                return "IB"
        else:  # n == 0
            if t == 4:
                return "IB"
            elif t == 3:
                return "IA2"
            else:
                return "IA1"
    else:  # edition == 9
        if m == 1:
            return "IV"
        elif n == 3:
            return "IIIC"
        elif n == 2:
            if t in [3, 4]:
                return "IIIA"
            else:
                return "IIIB"
        elif n == 1:
            if t in [3, 4]:
                return "IIA"
            else:
                return "IB"
        else:  # n == 0
            if t == 4:
                return "IB"
            elif t == 3:
                return "IA2"
            else:
                return "IA1"
            
st.title("Etapificador de Cáncer de Pulmón")
t_input = st.number_input("Ingrese el valor de T (1-4)", min_value=1, max_value=4, step=1)
n_input = st.number_input("Ingrese el valor de N (0-3)", min_value=0, max_value=3, step=1)
m_input = st.number_input("Ingrese el valor de M (0-1)", min_value=0, max_value=1, step=1)
edition_input = st.selectbox("Seleccione la edición de TNM", [7, 8, 9])

if st.button("Calcular"):
    result = etapificator_lung(t_input, n_input, m_input, edition_input)
    st.write(f"El estadío del cáncer de pulmón es: {result}")           