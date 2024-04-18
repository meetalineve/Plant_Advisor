import tkinter as tk
from tkinter import ttk
import dataset
import weather

def ask_interest():
    choice = interest_var.get()
    return choice

def ask_skill():
    choice = skill_var.get()
    return choice

def sort_plants_by_user_preference(plants, interest_level, skill_level):
    # Sort plants primarily based on maintenance level
    plants.sort(key=lambda x: x['maintenance_level'])
    
    # If user has high skill level, prioritize high maintenance plants
    if skill_level == 'Skilled':
        plants.sort(key=lambda x: x['maintenance_level'], reverse=True)
    
    return plants

def update_recommendations():
    try:
        location = weather.get_location()
        latitude, longitude = location.split(',')
        weather_data = weather.get_weather(latitude, longitude)
        weather_parameters = weather.extract_weather_parameters(weather_data)
        if weather_parameters:
            # Retrieve updated interest and skill levels
            interest_level = ask_interest()
            skill_level = ask_skill()
            
            suitable_plants = dataset.plants  # Start with all plants
            suitable_plants = weather.compare_weather_with_plants(weather_parameters, suitable_plants)
            
            # Sort plants based on user preference
            sorted_plants = sort_plants_by_user_preference(suitable_plants, interest_level, skill_level)
            
            # Prepare data for tabular display
            headers = ["Name", "Maintenance Level", "Flowering", "Growth Habit", "Information"]

            # Display recommendations in a separate window
            
            recommendations_window = tk.Toplevel(root)
            recommendations_window.title("Recommended Plants")
            
            # Recommendations table
            table = ttk.Treeview(recommendations_window, columns=headers, show="headings")
            for header in headers:
                table.heading(header, text=header)
            table.pack(fill="both", expand=True)
            
            # Insert data into the recommendations table
            for plant in sorted_plants:
                # Truncate the information field if necessary
                information = plant.get('info', 'Information not available')
                table.insert('', 'end', values=[
                    plant['name'],
                    plant['maintenance_level'],
                    'Flowering' if plant['flowering'] else 'Non-Flowering',
                    plant['growth_habit'],
                    information
                ])

        else:
            print("Failed to extract weather parameters.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Create Tkinter window
root = tk.Tk()
root.title("Plant Advisor")

# Create frame for user input
input_frame = ttk.Frame(root)
input_frame.pack(padx=10, pady=10)

# Configure column and row sizes
input_frame.columnconfigure(0, weight=1)  # Make the first column expandable
input_frame.columnconfigure(1, weight=1)  # Make the second column expandable
input_frame.rowconfigure(2, weight=1)     # Make the third row expandable

# Interest level dropdown
interest_label = ttk.Label(input_frame, text="How interested are you in plants?")
interest_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
interest_var = tk.StringVar()
interest_dropdown = ttk.Combobox(input_frame, textvariable=interest_var, values=["", "Low", "Medium", "High"])
interest_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
interest_dropdown.current(0)

# Skill level dropdown
skill_label = ttk.Label(input_frame, text="How good are you at taking care of plants?")
skill_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
skill_var = tk.StringVar()
skill_dropdown = ttk.Combobox(input_frame, textvariable=skill_var, values=["", "Hopeless", "Beginner", "Skilled"])
skill_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
skill_dropdown.current(0)

# Button to update recommendations
update_button = ttk.Button(input_frame, text="Get Recommendations", command=update_recommendations)
update_button.grid(row=2, columnspan=2, padx=5, pady=5)

# Run the Tkinter event loop
root.mainloop()
