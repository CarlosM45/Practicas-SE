from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import pandas as pd

app = FastAPI()

# --- CONFIGURACIÓN CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELOS ---
class RespuestaUsuario(BaseModel):
    questionId: int
    answer: str


# --- CARGA DE DATOS ---
try:
    # Asegúrate de que el CSV tenga: title, artist, genre, valence, popularity, explicit
    df = pd.read_csv("dataset.csv")

    # Limpieza inicial: Convertir género a string y minúsculas para evitar errores
    df['genre'] = df['genre'].astype(str).str.lower()

    print("Base de conocimiento cargada.")
except Exception as e:
    print(f"Error cargando CSV: {e}")
    df = pd.DataFrame()

# --- MOTOR DE INFERENCIA ---
def aplicar_filtros(respuestas: List[RespuestaUsuario], dataframe):
    # Trabajamos sobre una copia para no alterar la base original
    df_filtrado = dataframe.copy()

    for r in respuestas:

        # --- REGLA 1: ESTADO DE ÁNIMO (Valence) ---
        # Lógica: 0.0 a 0.33 (Melancólico), 0.34 a 0.66 (Relajado), 0.67 a 1.0 (Feliz)
        if r.questionId == 1:
            if 'valence' in df_filtrado.columns:
                if "Feliz" in r.answer:
                    df_filtrado = df_filtrado[df_filtrado['valence'] >= 0.67]
                elif "Relajado" in r.answer:
                    df_filtrado = df_filtrado[
                        (df_filtrado['valence'] >= 0.34) & (
                            df_filtrado['valence'] <= 0.66)
                    ]
                elif "Melancólico" in r.answer:
                    df_filtrado = df_filtrado[df_filtrado['valence'] <= 0.33]

        # --- REGLA 2: GÉNERO (Búsqueda semántica en inglés) ---
        if r.questionId == 2:
            if 'genre' in df_filtrado.columns:
                respuesta = r.answer

                if "Hip-Hop" in respuesta:  # Cubre "Hip-Hop/Rap"
                    # Busca tanto 'hip hop' como 'rap' usando Regex (| significa O)
                    df_filtrado = df_filtrado[
                        df_filtrado['genre'].str.contains(
                            'hip hop|rap', case=False, regex=True)
                    ]
                elif "Electrónica" in respuesta:
                    # Busca 'electronic' o 'techno'
                    df_filtrado = df_filtrado[
                        df_filtrado['genre'].str.contains(
                            'electronic|techno', case=False, regex=True)
                    ]
                elif "Anime" in respuesta:
                    # A veces en los dataset aparece como 'j-pop' o 'anime'
                    df_filtrado = df_filtrado[
                        df_filtrado['genre'].str.contains(
                            'anime|j-pop', case=False, regex=True)
                    ]
                else:
                    # Para Pop y Rock, búsqueda directa simple
                    # Usamos contains por si el género es "alternative rock" o "pop punk"
                    df_filtrado = df_filtrado[
                        df_filtrado['genre'].str.contains(
                            respuesta.lower(), case=False)
                    ]

        # --- REGLA 3: POPULARIDAD (Rangos numéricos) ---
        if r.questionId == 3:
            if 'popularity' in df_filtrado.columns:
                if "muy popular" in r.answer:
                    df_filtrado = df_filtrado[df_filtrado['popularity'] > 80]
                elif "poco popular" in r.answer:
                    df_filtrado = df_filtrado[df_filtrado['popularity'] < 50]
                elif "música popular" in r.answer:  # Opción media
                    # Rango intermedio: entre 50 y 80 inclusive
                    df_filtrado = df_filtrado[
                        (df_filtrado['popularity'] >= 50) & (
                            df_filtrado['popularity'] <= 80)
                    ]

        # --- REGLA 4: LETRA EXPLÍCITA (Filtro Condicional) ---
        if r.questionId == 4:
            if 'explicit' in df_filtrado.columns:
                if r.answer == "No":
                    # El usuario NO quiere explicit -> Filtramos para dejar solo explicit=False
                    df_filtrado = df_filtrado[df_filtrado['explicit'] == False]
                # Si la respuesta es "Sí", NO hacemos nada.
                # (Dejamos pasar tanto True como False, que es lo que pediste).

    return df_filtrado


@app.post("/recomendar")
def recomendar(respuestas: List[RespuestaUsuario]):
    if df.empty:
        raise HTTPException(status_code=500, detail="Base de datos no cargada")

    resultados = aplicar_filtros(respuestas, df)

    # Manejo de error si el filtro es muy estricto y no queda nada
    if resultados.empty:
        return []

    cantidad_resultados = len(resultados)

    if cantidad_resultados > 10:
        # Si hay muchas coincidencias (ej. 500), tomamos 10 al azar.
        # random_state=None asegura que cada vez sea diferente.
        resultados = resultados.sample(n=10)
    resultados = resultados.sort_values(by='popularity', ascending=False)
    return resultados.to_dict(orient="records")
