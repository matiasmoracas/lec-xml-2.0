import streamlit as st
import pandas as pd
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def preguntar_a_openai(df: pd.DataFrame, pregunta: str) -> str:
    contenido_csv = df.to_csv(index=False)

    prompt = f"""
Eres un asistente contable experto en documentos electrónicos del SII de Chile.
Pregunta: {pregunta}

Aquí tienes los datos extraídos en formato CSV:
{contenido_csv}
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """
             Eres un asistente contable especializado en facturas y documentos electrónicos del SII de Chile.
             Solo puedes responder preguntas directamente relacionadas con el contenido entregado en formato CSV.
             Si el usuario te hace una pregunta absurda, personal, o que no tiene relación con el XML o la contabilidad, simplemente responde: 
             'Lo siento, solo puedo responder preguntas contables sobre los documentos subidos.'"""},
                                                                                                 
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=800
    )

    return response.choices[0].message.content
