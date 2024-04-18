import csv
import ast

plants = []

with open('plants.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Convert string representation of tuple to actual tuple
        row['temperature_tolerance'] = ast.literal_eval(row['temperature_tolerance'])
        plants.append(row)

# Function to extract temperature range from temperature tolerance tuple
def extract_temperature_range(temperature_tolerance):
    try:
        if isinstance(temperature_tolerance, tuple) and len(temperature_tolerance) == 2:
            min_temp, max_temp = temperature_tolerance
            return min_temp, max_temp
        else:
            print("Invalid temperature tolerance format")
            return None, None
    except ValueError:
        print("Error converting temperature range")
        return None, None

# Process each plant data
for plant in plants:
    temperature_tolerance = plant['temperature_tolerance']
    min_temp, max_temp = extract_temperature_range(temperature_tolerance)
    print(f"Plant: {plant['name']}, Temperature Range: {min_temp}°C - {max_temp}°C")
