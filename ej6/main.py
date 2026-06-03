# Utilizando la API Response, hacer una aplicación en python que permita acceder a los datos del clima 
# de la Ciudad Autónoma de Buenos Aires y lo muestre los datos consultados.


import requests

LATITUD = -34.61 # ejemplo
LONGITUD = -58.38 #ejemplo

URL = (
    f"https://api.open-meteo.com/v1/forecast"
    f"?latitude={LATITUD}"
    f"&longitude={LONGITUD}"
    f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
)

def obtener_clima():
    try:
        respuesta = requests.get(URL)
        respuesta.raise_for_status()

        datos = respuesta.json()

        clima_actual = datos["current"]

        temperatura = clima_actual["temperature_2m"]
        humedad = clima_actual["relative_humidity_2m"]
        viento = clima_actual["wind_speed_10m"]

        print("=== Clima en Ciudad Autónoma de Buenos Aires ===")
        print(f"Temperatura: {temperatura} °C")
        print(f"Humedad: {humedad} %")
        print(f"Velocidad del viento: {viento} km/h")

    except requests.exceptions.RequestException as e:
        print("Error al consultar la API:", e)

if __name__ == "__main__":
    obtener_clima()