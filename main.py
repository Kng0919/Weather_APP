from flask import Flask, render_template, request
import requests
import geocoder

app = Flask(__name__)

API_URL = "https://goweather.herokuapp.com/weather"
api_keys = "285539eb30e58322a122bce085d78097"

def get_weather(city):
    lat = ""
    lon = ""

    # Fetching location's Latitude and Longitude
    response = requests.get(f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_keys}")
    if response.status_code == 200:
        try:
            data = response.json()
            lat = data[0]["lat"]
            lon = data[0]["lon"]
        except (IndexError, KeyError):
            return None

    # Fetching weather data
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_keys}&units=metric")
    if response.status_code == 200:
        return response.json()


def get_weather_by_location():
    g = geocoder.ip('me')
    return get_weather(g.city), g.city

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    temp = None
    weather_icon = None
    city = None
    if request.method == "POST":
        if "get_weather" in request.form:
            city = request.form["city"]
            weather = get_weather(city)
        elif "get_location_weather" in request.form:
            weather, city = get_weather_by_location()
        
        if weather:
            temp = round(weather['main']['temp'], 0)
            weather_icon = "https://cdn2.iconfinder.com/data/icons/weather-flat-14/64/weather02-512.png" 
            
    return render_template("index.html", city = city, weather=weather, temp=temp, weather_icon=weather_icon)

if __name__ == "__main__":
    app.run(debug=True, port=5005)