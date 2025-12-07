from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

app = FastAPI()

# --- CONFIGURACIÓN DE CORS ---
# Esto permite que tu React (puerto 5173) hable con este Python (puerto 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # La dirección de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CARGA DE LA BASE DE CONOCIMIENTO ---
# Asegúrate de tener un archivo 'canciones.csv' en la misma carpeta
# Estructura sugerida del CSV: id, titulo, artista, genero, ritmo, estado_animo

try:
    # Cargamos el CSV al iniciar la app para no leerlo en cada consulta (eficiencia)
    df = pd.read_csv("canciones.csv")
    print("Base de conocimiento cargada correctamente.")
except Exception as e:
    print(f"Error cargando CSV: {e}")
    df = pd.DataFrame()  # DataFrame vacío para evitar crasheos si falla

# --- MOTOR DE INFERENCIA (Endpoint) ---


@app.get("/recomendar")
def recomendar_musica(genero: str = None, ritmo: str = None):
    """
    Ejemplo simple de inferencia.
    React llamará a: http://localhost:8000/recomendar?genero=rock&ritmo=rapido
    """
    if df.empty:
        raise HTTPException(
            status_code=500, detail="Base de conocimiento no disponible")

    # Empezamos con todas las canciones
    resultados = df.copy()

    # REGLA 1: Filtrar por género si el usuario seleccionó uno
    if genero:
        resultados = resultados[resultados['genero'].str.lower()
                                == genero.lower()]

    # REGLA 2: Filtrar por ritmo si el usuario seleccionó uno
    if ritmo:
        resultados = resultados[resultados['ritmo'].str.lower()
                                == ritmo.lower()]

    # Convertimos a diccionario para enviarlo a React (JSON)
    return resultados.to_dict(orient="records")


@app.get("/")
def read_root():
    return {"mensaje": "El Sistema Experto está activo"}
