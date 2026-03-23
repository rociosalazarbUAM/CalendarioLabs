import streamlit as st
from datetime import datetime, time
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Reserva de Laboratorio", page_icon="🧪")

# Estética personalizada con CSS
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧪 Sistema de Reserva de Laboratorio")
st.write("Completa los datos para agendar tu espacio.")

with st.form("reserva_form"):
    nombre = st.text_input("Nombre completo")
    email = st.text_input("Tu correo electrónico")
    
    col1, col2 = st.columns(2)
    with col1:
        laboratorio = st.selectbox("Selecciona el Laboratorio", 
                                  ["Lab. Pavimentos", "Lab. Topografía", "Lab. Suelos"])
        fecha = st.date_input("Fecha de reserva", min_value=datetime.now())
    
    with col2:
        hora_inicio = st.time_input("Hora de inicio", time(9, 0))
        hora_fin = st.time_input("Hora de finalización", time(11, 0))

    proyecto = st.text_area("Descripción corta del proyecto/práctica")
    
    submit = st.form_submit_button("Enviar Solicitud de Reserva")

if submit:
    if not nombre or not email:
        st.error("Por favor, llena todos los campos obligatorios.")
    elif hora_inicio >= hora_fin:
        st.error("La hora de inicio debe ser menor a la de fin.")
    else:
        # AQUÍ CONECTARÍAS CON TU DB O ENVIARÍAS EL MAIL
        st.success(f"¡Gracias {nombre}! Solicitud enviada a los responsables.")
        st.balloons()
        
        # Simulación de aviso a responsables
        # Para enviar correos reales desde Python usa la librería 'smtplib'