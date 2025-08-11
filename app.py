import os
import streamlit as st
import pandas as pd
import io

from processor import procesar_archivos_xml
from openai_helper import preguntar_a_openai
from ui import configurar_estilo, mostrar_encabezado, mostrar_footer

st.set_page_config(page_title="Lector XML Ingefix", layout="wide", initial_sidebar_state="collapsed")
configurar_estilo()
mostrar_encabezado()

# --- Chequeo de API key (para que el asistente no rompa si falta) ---
has_api_key = ("OPENAI_API_KEY" in st.secrets) or bool(os.getenv("OPENAI_API_KEY"))
if not has_api_key:
    st.warning("⚠️ No encuentro **OPENAI_API_KEY**. El lector de XML funciona, pero el asistente contable estará deshabilitado.")

# Subida de archivos
st.markdown("### Subir archivos XML")
uploaded_files = st.file_uploader("Selecciona uno o más archivos XML:", type="xml", accept_multiple_files=True)

datos_finales = procesar_archivos_xml(uploaded_files)

if datos_finales:
    df = pd.DataFrame(datos_finales)
    st.markdown("### Resultado del procesamiento")
    st.success(f"✅ {len(df)} líneas procesadas.")
    st.dataframe(df, use_container_width=True)

    # Descarga
    excel = io.BytesIO()
    df.to_excel(excel, index=False, engine='openpyxl')
    st.download_button("Descargar Excel", data=excel.getvalue(),
                       file_name="facturas_sii.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Asistente
    st.markdown("###  Consulta al Asistente Contable Ingefix")
    with st.form("formulario_pregunta"):
        pregunta = st.text_input("Escribe tu pregunta sobre el o los XML:")
        enviar = st.form_submit_button("Preguntar", disabled=not has_api_key)

    if pregunta and enviar:
        with st.spinner("Consultando al asistente contable Ingefix..."):
            try:
                respuesta = preguntar_a_openai(df, pregunta)
                st.markdown("#### ✅ Respuesta del asistente:")
                st.markdown(
                    f"<div style='background-color:#f9f9f9; padding:15px; border-radius:10px; border:1px solid #ddd;'>{respuesta}</div>",
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.error(f"⚠️ Error al consultar al asistente contable Ingefix: {e}")
else:
    st.info("📂 Esperando que subas uno o más archivos XML para procesar...")

mostrar_footer()

