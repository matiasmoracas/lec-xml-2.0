import streamlit as st
import streamlit.components.v1 as components

def configurar_estilo():
    st.markdown("""
        <style>
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #ffffff;
            color: #000000;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        h1 {
            color: #4B8BBE;
            text-align: center;
        }

        .stDownloadButton button, .stButton button {
            background-color: #4B8BBE;
            color: white;
            border-radius: 8px;
            font-weight: bold;
            padding: 0.6em 1.2em;
            font-size: 10px;
        }

        .footer {
            position: top;
            bottom: 0;
            width: 100%;
            background-color: #f0f2f6;
            text-align: center;
            font-size: 14px;
            color: #6c757d;
            padding: 16px;
            border-top: 2px solid #ddd;
        }
        </style>
    """, unsafe_allow_html=True)

def mostrar_encabezado():
    st.markdown("<h1>Lector de XML Contabilidad</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:bold;'>Sube archivos XML de nuestros proveedores y obtén información clara gracias al asistente contable Ingefix!!</p>", unsafe_allow_html=True)
    st.markdown("---")

def mostrar_footer():
    st.markdown("""
    <div class="footer">
        © 2025 · Desarrollado por <strong>Soporte Ingefix</strong> · Todos los derechos reservados
    </div>
    """, unsafe_allow_html=True)