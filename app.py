import streamlit as st
import pandas as pd
from helpers import fetch_and_save_assignments

st.set_page_config(page_title="Visualizador de tareas", page_icon=":pencil:")
st.write("Para visualizar tus tareas del mes, ingresa tu usuario (matrícula) y contraseña con la que ingresas a la plataforma Moodle de UANE.",)
username = st.text_input("Matrícula")
password = st.text_input("Contraseña", type='password')

# Moodle URLs and headers
login_url = 'https://aula.uane.mx/login/index.php'
calendar_url = 'https://aula.uane.mx/calendar/view.php?view=month'
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'es-US,es;q=0.9,es-419;q=0.8,en;q=0.7',
    'referer': 'https://aula.uane.mx/my/',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}

if st.button("Ver tareas"):
    if username and password:
        assignments = fetch_and_save_assignments(username, password, login_url, calendar_url, headers)

        if assignments:
            df = pd.DataFrame(assignments)
            st.write("### Tus tareas actuales:")
            st.dataframe(df.drop(columns=['course']))
        else:
            st.error("Error al obtener las tareas. Verifica tus credenciales de acceso.")
    else:
        st.error("Nombre de usuario y contraseña necesarios.")