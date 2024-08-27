from flask import Flask, render_template, request
import requests
import geocoder

app = Flask(__name__)

API_URL = "https://goweather.herokuapp.com/weather"

def get_weather(city):
    response = requests.get(f"{API_URL}/{city}")
    if response.status_code == 200:
        data = response.json()
        data['city'] = city
        return data
    else:
        return None

def get_weather_by_location():
    g = geocoder.ip('me')
    return get_weather(g.city)

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    weather_icon = None
    if request.method == "POST":
        if "get_weather" in request.form:
            city = request.form["city"]
            weather = get_weather(city)
        elif "get_location_weather" in request.form:
            weather = get_weather_by_location()
        
        if weather:
            weather_icon = "https://cdn2.iconfinder.com/data/icons/weather-flat-14/64/weather02-512.png" 
            
    return render_template("index.html", weather=weather, weather_icon=weather_icon)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
