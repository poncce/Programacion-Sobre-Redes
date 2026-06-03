# Utilizando la API Response, hacer una aplicación en python que permita acceder a los datos del 
# clima de la Ciudad Autónoma de Buenos Aires y lo muestre los datos consultados.


from flask import Flask
import requests

app = Flask(__name__)

def obtener_precio_bitcoin():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd,ars"
    respuesta = requests.get(url)
    datos = respuesta.json()
    precio_usd = datos["bitcoin"]["usd"]
    precio_ars = datos["bitcoin"]["ars"]
    return precio_usd, precio_ars

@app.route("/")
def index():
    precio_usd, precio_ars = obtener_precio_bitcoin()
    return f"""
    <html>
        <head>
            <title>Precio Bitcoin</title>
        </head>
        <body>
            <h1>Precio actual de Bitcoin</h1>
            
            <p>Valor en dolares: ${precio_usd}</p>
            <p>Valor en pesos argentinos: ${precio_ars}</p>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)