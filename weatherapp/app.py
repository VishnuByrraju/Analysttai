from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_weather(city):
    api_key = '4946ba3b670a306d7713685da47a3105'  # Replace 'YOUR_API_KEY' with your actual API key
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    weather_data = get_weather(city)
    if weather_data['cod'] == 200:
        city_name = weather_data['name']
        country = weather_data['sys']['country']
        description = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        return render_template('weather.html', city=city_name, country=country,
                               description=description, temperature=temperature,
                               humidity=humidity, wind_speed=wind_speed)
    else:
        error_message = "City not found!"
        return render_template('error.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
