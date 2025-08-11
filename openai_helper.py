# openai_helper.py
import os
import pandas as pd
import streamlit as st
from openai import OpenAI

def _get_api_key() -> str | None:
    # 1) Secrets (Streamlit Cloud)  2) Variable de entorno (Render/local)
    return st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

def _get_client() -> OpenAI:
    api_key = _get_api_key()
    if not api_key:
        raise RuntimeError(
            "Falta OPENAI_API_KEY. Configúrala en Streamlit (Manage app → Secrets) "
            "o como variable de entorno antes de usar el asistente."
        )
    return OpenAI(api_key=api_key)

def _df_to_context(df: pd.DataFrame, max_rows: int = 60) -> str:
    if df is None or df.empty:
        return "SIN_DATOS"
    # recorta filas muy grandes para no pasarle todo al modelo
    if len(df) > max_rows:
        df = df.head(max_rows).copy()
    return df.to_csv(index=False)

def preguntar_a_openai(df: pd.DataFrame, pregunta: str) -> str:
    client = _get_client()
    contenido_csv = _df_to_context(df)

    system_msg = (
        "Eres un asistente contable especializado en facturas y DTE del SII de Chile. "
        "Responde en español, claro y conciso. Si la pregunta no está relacionada con los "
        "documentos o la contabilidad, responde exactamente: "
        "'Lo siento, solo puedo responder preguntas contables sobre los documentos subidos.'"
    )

    user_msg = (
        f"Eres un asistente contable experto en documentos electrónicos del SII de Chile, "
        f"para la empresa Ingefix S.A.\n\n"
        f"Pregunta: {pregunta}\n\n"
        f"Datos extraídos en CSV:\n{contenido_csv}\n"
    )

    resp = client.chat.completions.create(
        model="gpt-4o",          # usa el modelo que prefieras
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.3,
        max_tokens=800,
    )

    return resp.choices[0].message.content.strip()
