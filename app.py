import streamlit as st
from datetime import datetime, time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIGURACIÓN DE LOS RESPONSABLES ---
# Sustituye con los correos reales
CORREOS_RESPONSABLES = [
    "responsable1@gmail.com",
    "responsable2@gmail.com",
    "responsable3@gmail.com",
    "responsable4@gmail.com"
]

# --- CONFIGURACIÓN DEL EMISOR (Tu cuenta de despacho) ---
# Se recomienda usar una cuenta de Gmail secundaria
EMAIL_EMISOR = "tu_correo_de_envio@gmail.com"
EMAIL_PASSWORD = "tu_password_de_aplicacion" # No es tu contraseña normal, ver paso 2 abajo.

def enviar_correo(datos):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_EMISOR
        msg['To'] = ", ".join(CORREOS_RESPONSABLES)
        msg['Subject'] = f"🚨 NUEVA RESERVA: {datos['espacio']}"

        cuerpo = f"""
        Se ha recibido una nueva solicitud de reserva de laboratorio:
        
        - Solicitante: {datos['nombre']}
        - Correo: {datos['email']}
        - Espacio: {datos['espacio']}
        - Fecha: {datos['fecha']}
        - Horario: de {datos['h_inicio']} a {datos['h_fin']}
        - Proyecto: {datos['proyecto']}
        
        Por favor, ingresa a Notion para aprobar o rechazar esta solicitud.
        """
        msg.attach(MIMEText(cuerpo, 'plain'))

        # Servidor SMTP de Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_EMISOR, EMAIL_PASSWORD)
        server.sendmail(EMAIL_EMISOR, CORREOS_RESPONSABLES, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"Error al enviar correo: {e}")
        return False

# --- INTERFAZ DE STREAMLIT ---
st.set_page_config(page_title="Reserva de Lab", page_icon="🧪")

st.title("🧪 Reserva de Espacios")

laboratorios = ["Selecciona...", "Lab. Pavimentos", "Lab. Topografía", "Lab. Suelos"]

with st.form("form_reserva"):
    nombre = st.text_input("Nombre completo")
    email = st.text_input("Tu correo")
    espacio = st.selectbox("Espacio", laboratorios)
    
    col1, col2 = st.columns(2)
    fecha = col1.date_input("Fecha", min_value=datetime.now())
    h_inicio = col2.time_input("Desde", time(8, 0))
    h_fin = col2.time_input("Hasta", time(10, 0))
    
    proyecto = st.text_area("Descripción del proyecto")
    
    btn_enviar = st.form_submit_button("Confirmar Reserva")

if btn_enviar:
    if espacio == "Selecciona..." or not nombre or not email:
        st.warning("Por favor completa los campos obligatorios.")
    else:
        datos_reserva = {
            "nombre": nombre,
            "email": email,
            "espacio": espacio,
            "fecha": fecha,
            "h_inicio": h_inicio,
            "h_fin": h_fin,
            "proyecto": proyecto
        }
        
        with st.spinner("Enviando aviso a responsables..."):
            exito = enviar_correo(datos_reserva)
            
        if exito:
            st.success("¡Reserva enviada! Los responsables han sido notificados por correo.")
            st.balloons()