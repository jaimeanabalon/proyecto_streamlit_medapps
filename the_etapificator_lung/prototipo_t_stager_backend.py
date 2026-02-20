def clasificador_t_Stager_backend():
    if ((diametro >= 70) or isin(t4_invasion) or (diametro < 50)) or st.session_state.t2_pleura_visceral or st.session_state.t2_lobulo_adyacente or st.session_state.t2_bronquio_principal_no_carina or st.session_state.t2_atelectasia_y_o_neumonia_postobstructiva or st.session_state.t2_hilio_pulmonar:
        return "T2"