# weather.py
import requests

def get_location():
    response = requests.get('https://ipinfo.io')
    data = response.json()
    return data.get('loc')

def get_weather(latitude, longitude):
    APIkey = '42c29e4f55d6ccdf411e02c1abe6e4e9'
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={APIkey}'
    response = requests.get(url)
    data = response.json()
    return data

def extract_weather_parameters(weather_data):
    try:
        humidity = weather_data.get('main', {}).get('humidity')
        sunrise = weather_data.get('sys', {}).get('sunrise')
        sunset = weather_data.get('sys', {}).get('sunset')
        dt = weather_data.get('dt')
        if sunrise and sunset and dt:
            sunlight = 'day' if sunrise < dt < sunset else 'night'
        else:
            sunlight = 'unknown'
        rain = True if 'rain' in weather_data else False
        
        # Convert temperature values from Kelvin to Celsius
        temperature_kelvin = weather_data.get('main', {}).get('temp')
        temperature_celsius = temperature_kelvin - 273.15  # Conversion from Kelvin to Celsius
        
        temperature_min_kelvin = weather_data.get('main', {}).get('temp_min')
        temperature_max_kelvin = weather_data.get('main', {}).get('temp_max')
        temperature_min_celsius = temperature_min_kelvin - 273.15
        temperature_max_celsius = temperature_max_kelvin - 273.15
        temperature_range_celsius = (temperature_min_celsius, temperature_max_celsius)

        wind_speed = weather_data.get('wind', {}).get('speed')
        cloudiness = weather_data.get('clouds', {}).get('all')

        return {'Humidity': humidity, 'Sunlight': sunlight, 'Rain': rain, 
                'Temperature (Celsius)': temperature_celsius, 
                'Temperature Range (Celsius)': temperature_range_celsius, 
                'Wind Speed': wind_speed, 'Cloudiness': cloudiness}
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

def compare_weather_with_plants(weather_parameters, plants):
    suitable_plants = []
    temperature_celsius = weather_parameters['Temperature (Celsius)']
    humidity = weather_parameters['Humidity']
    
    humidity_ranges = {
        "Low": (0, 10),
        "Moderate": (11, 70),
        "High": (71, 100)
    }
    
    for plant in plants:
        temperature_tolerance = plant['temperature_tolerance']
        if isinstance(temperature_tolerance, tuple):
            min_temp, max_temp = temperature_tolerance
        else:
            try:
                min_temp_str, max_temp_str = temperature_tolerance.split('-')
                min_temp = float(min_temp_str.strip().rstrip('°C'))
                max_temp = float(max_temp_str.strip().rstrip('°C'))
            except ValueError:
                print(f"An error occurred: Invalid temperature tolerance format for plant '{plant['name']}'")
                continue
        
        # Check if temperature and humidity fall within acceptable range for the plant
        if isinstance(temperature_tolerance, str):
            print(f"An error occurred: Invalid temperature tolerance format for plant '{plant['name']}'")
            continue
        
        if (min_temp <= temperature_celsius <= max_temp or
            humidity_ranges.get(plant['humidity_preference'])):
            min_humidity, max_humidity = humidity_ranges[plant['humidity_preference']]
            if min_humidity <= humidity <= max_humidity:
                suitable_plants.append(plant)
    
    if not suitable_plants:
        print("No suitable plants found.")
                
    return suitable_plants
