from flask import Flask, render_template, request
import requests


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    wetter = None
    stadt = None

    if request.method == "POST":
        stadt = request.form["stadt"]

        # 1. Koordinaten der Stadt holen (Geocoding)
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={stadt}&count=1"
        geo = requests.get(geo_url).json()

        if "results" in geo:
            lat = geo["results"][0]["latitude"]
            lon = geo["results"][0]["longitude"]

            # 2. Wetter für diese Koordinaten holen
            wetter_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            daten = requests.get(wetter_url).json()
            wetter = daten["current_weather"]

    return render_template("index.html", wetter=wetter, stadt=stadt)


if __name__ == "__main__":
    app.run(debug=True)