import streamlit as st

st.title("T Stager")
t2_invasion = ['pleura visceral','lobulo adyacente','bronquio principal, no carina','atelectasia y/o neumonía postobstructiva','hilio pulmonar']

t3_invasion = ['pleura parietal','pared torácica','pericardio','nervio frenico','vena azigos','raíces nerviosas torácicas','ganglio estrellado']
#t4_invasion = ['timo','traquea','carina','nv. laringeo recurrente','nv.vago','esofago','diafragma','corazón','vena cava inferior','vena cava superior','art venas pulmonares intrapericardicas','arterias supraaorticas','venas braquiocefalicas','vasos subclavios','cuerpo vertebral','lamina vertebral','canal medular','raices nerviosas cervicales','plexo braquial']

t4_invasion = ['timo','traquea','carina',['nv. laringeo recurrente','nv.vago','raices nerviosas cervicales','plexo braquial'],'esofago','diafragma',['corazón','vena cava inferior','vena cava superior','art venas pulmonares intrapericardicas','arterias supraaorticas','venas braquiocefalicas','vasos subclavios'],['cuerpo vertebral','lamina vertebral','canal medular'],]

st.radio("Lateralidad del tumor", ["Izquierdo", "Derecho",], index=0, key="lateralidad")

diametro = st.number_input("Diámetro máximo del tumor (mm)", min_value=5, max_value=100, step=1, value="min", key="diametro")

st.radio("¿Son tumores separados?", ["Sí", "No"], index=1, key="tumores_separados")
st.checkbox("¿En el mismo lóbulo?", key="tumor_multiples_segmentos")
st.checkbox("¿En el mismo pulmón?", key="tumor_mismo_pulmon")
st.checkbox("¿En el pulmón contralateral?", key="tumor_contralateral")
# invasion = st.multiselect("Invasión de estructuras adyacentes", t2_invasion, key="invasion")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Invasión T2")
    for i in t2_invasion:
        if isinstance(i, list):
            for j in i:
                st.checkbox(str(j).capitalize(), key=f"t2_{str(j)}")
        else:
            st.checkbox(str(i).capitalize(), key=f"t2_{str(i)}")


with col2:
    st.subheader("Invasión T3")
    for i in t3_invasion:
        if isinstance(i, list):
            for j in i:
                st.checkbox(str(j).capitalize(), key=f"t3_{str(j)}")
        else:   
            st.checkbox(str(i).capitalize(), key=f"t3_{str(i)}")

with col3:
    st.subheader("Invasión T4")
    for i in t4_invasion:
        if isinstance(i, list):
            for j in i:
                st.checkbox(str(j).capitalize(), key=f"t4_{str(j)}")
        else:   
            st.checkbox(str(i).capitalize(), key=f"t4_{str(i)}")


