import streamlit as st

st.title("T Stager")
t2_invasion = ['pleura visceral','lobulo adyacente','bronquio principal, no carina','atelectasia y/o neumonía postobstructiva','hilio pulmonar']
t3_invasion = ['pleura parietal','pared torácica','pericardio','nervio frenico','vena azigos','raíces nerviosas torácicas','ganglio estrellado']
t4_invasion = ['timo','traquea','carina','nv. laringeo recurrente','nv.vago','esofago','diafragma','corazón','vena cava inferior','vena cava superior','art venas pulmonares intrapericardicas','arterias supraaorticas','venas braquiocefalicas','vasos subclavios','cuerpo vertebral','lamina vertebral','canal medular','raices nerviosas cervicales','plexo braquial']

st.radio("Lateralidad del tumor", ["Izquierdo", "Derecho",], index=0, key="lateralidad")

diametro = st.number_input("Diámetro máximo del tumor (mm)", min_value=5, max_value=20, step=1, value="min", key="diametro")

st.checkbox("Invasión de estructuras adyacentes", args = t2_invasion, key="invasion")