import math
import pandas as pd
import streamlit as st
from streamlit_js_eval import get_geolocation

# Configuración de página
st.set_page_config(
    page_title="Postas Policiales SPS", page_icon="👮", layout="centered"
)

st.title("Actividad: Postas Policiales Más Cercanas - SPS")
st.markdown(
    "Esta aplicación identifica las 3 postas policiales más cercanas a tu"
    " ubicación en San Pedro Sula mediante coordenadas GPS."
)

st.divider()

# Lista de Postas Policiales Reales en San Pedro Sula
POSTAS = [
    {
        "nombre": "UMEP #5 - Barrio Barandillas (Centro)",
        "latitud": 15.5132,
        "longitud": -88.0218,
    },
    {
        "nombre": "Posta Policial Colonia Satélite",
        "latitud": 15.4981,
        "longitud": -87.9754,
    },
    {
        "nombre": "Posta Policial Rivera Hernández",
        "latitud": 15.5352,
        "longitud": -87.9651,
    },
    {
        "nombre": "Posta Policial Chamelecón",
        "latitud": 15.4523,
        "longitud": -88.0125,
    },
    {
        "nombre": "Posta Policial Colonia Fesitranh (Norte)",
        "latitud": 15.5651,
        "longitud": -88.0053,
    },
    {
        "nombre": "Posta Policial Barrio Sunseri",
        "latitud": 15.4925,
        "longitud": -88.0281,
    },
    {
        "nombre": "Posta Policial Cofradía",
        "latitud": 15.4053,
        "longitud": -88.1521,
    },
]


# Cálculo de distancia mediante fórmula de Haversine
def calcular_distancia(lat1, lon1, lat2, lon2):
  R = 6371.0
  dlat = math.radians(lat2 - lat1)
  dlon = math.radians(lon2 - lon1)

  a = (
      math.sin(dlat / 2) ** 2
      + math.cos(math.radians(lat1))
      * math.cos(math.radians(lat2))
      * math.sin(dlon / 2) ** 2
  )
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
  return R * c


# Intentar obtener GPS del dispositivo
loc = get_geolocation()

default_lat = 15.5042
default_lon = -88.0250

if loc and "coords" in loc:
  default_lat = loc["coords"]["latitude"]
  default_lon = loc["coords"]["longitude"]
  st.success("📍 Ubicación detectada automáticamente mediante GPS.")

# Formulario de entrada
with st.form("form_coordenadas"):
  st.subheader("📍 Coordenadas de Búsqueda")
  col1, col2 = st.columns(2)

  with col1:
    user_lat = st.number_input("Latitud", value=default_lat, format="%.6f")
  with col2:
    user_lon = st.number_input("Longitud", value=default_lon, format="%.6f")

  btn_buscar = st.form_submit_button("🔍 Buscar Postas Cercanas")

if btn_buscar:
  resultados = []
  for posta in POSTAS:
    dist = calcular_distancia(
        user_lat, user_lon, posta["latitud"], posta["longitud"]
    )
    resultados.append({
        "Nombre de la Posta": posta["nombre"],
        "Distancia (km)": round(dist, 2),
        "lat": posta["latitud"],
        "lon": posta["longitud"],
    })

  df_resultados = pd.DataFrame(resultados)
  df_top3 = df_resultados.sort_values(by="Distancia (km)").head(3)

  st.subheader("🚨 Las 3 Postas Policiales Más Cercanas")

  for idx, row in df_top3.reset_index(drop=True).iterrows():
    st.markdown(
        f"**{idx+1}. {row['Nombre de la Posta']}**  \n"
        f"📏 **Distancia:** `{row['Distancia (km)']} km` | 🌐 **Coordenadas:**"
        f" `{row['lat']}, {row['lon']}`"
    )

  st.divider()

  # Mapa
  st.subheader("🗺️ Ubicación en el Mapa")
  puntos_mapa = pd.DataFrame({
      "lat": [user_lat] + list(df_top3["lat"]),
      "lon": [user_lon] + list(df_top3["lon"]),
  })
  st.map(puntos_mapa)
