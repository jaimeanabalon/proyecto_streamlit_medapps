import streamlit as st
import pandas as pd


def calculadora_carbo(auc=6, edad=40, peso=70, crea=1, sexo='hombre'):
    clearance = ((140 - edad) * peso) / (crea * 72)
    if sexo == 'mujer':
        clearance = clearance * 0.85
    if clearance >= 125:
        clearance = 125
    dosis = auc * (clearance + 25)
    return dosis

auc_input = st.number_input("AUC Deseada", min_value=1, step=1)
edad_input = st.number_input("Edad", min_value=18, step=1)
peso_input = st.number_input("Peso", min_value=30.0, step=0.1)
crea_input = st.number_input("Creatinina en mg/dL", min_value=0.1, step=0.1)
sexo_input = st.radio("Sexo", ["Masculino", "Femenino"])

if sexo_input == "Femenino":
    sexo_logica = "mujer"
else:
    sexo_logica = "hombre"

if st.button("Calcular la dosis"):
      dosis_final = calculadora_carbo(auc_input,edad_input,peso_input,crea_input,sexo_logica)
      st.write(f"La dosis total es: {dosis_final} mg")