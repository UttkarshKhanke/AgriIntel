import requests

def get_weather(city):
    API_KEY = "40bc60c2d9e8f065643bad455c961b72"  # 🔑 Replace with your API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    response = requests.get(url).json()
    
    if response.get("cod") != 200:
        raise Exception("Error fetching weather. Check city name or API key.")

    temperature = response['main']['temp']
    humidity = response['main']['humidity']
    rainfall = response.get('rain', {}).get('1h', 0)  # mm rain in last 1 hour
    
    return temperature, humidity, rainfall
