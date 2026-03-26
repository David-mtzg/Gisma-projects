"""
Simple GUI for the Weather Dashboard.
Uses Tkinter to provide a graphical interface.

"""

import tkinter as tk
from tkinter import messagebox

from api_client import GeocodingClient, WeatherClient
from charts import generate_all_charts


# create service objects
geocoder = GeocodingClient()
weather_client = WeatherClient()


def search_weather():
    """Search weather for the entered city."""
    city_name = city_entry.get().strip()

    if not city_name:
        messagebox.showerror("Error", "Please enter a city name.")
        return

    try:
        # find city
        city = geocoder.search(city_name)

        # fetch weather
        current, forecast = weather_client.fetch(city)

        # show result in GUI
        result_text.set(
            f"{city.name}, {city.country}\n"
            f"Temperature: {current.temperature_c} °C\n"
            f"Feels like: {current.feels_like_c} °C\n"
            f"Humidity: {current.humidity_pct}%\n"
            f"Wind: {current.wind_speed_kmh} km/h\n"
            f"Condition: {current.weather_description}"
        )

        # generate charts using your existing system
        generate_all_charts(forecast, current)

    except Exception as exc:
        messagebox.showerror("Error", str(exc))


# main window
window = tk.Tk()
window.title("Weather Dashboard")
window.geometry("420x320")


# title
title = tk.Label(
    window,
    text="Weather Dashboard",
    font=("Arial", 16, "bold")
)
title.pack(pady=10)


# city input
city_label = tk.Label(window, text="Enter city name:")
city_label.pack()

city_entry = tk.Entry(window, width=30)
city_entry.pack(pady=5)


# search button
search_button = tk.Button(
    window,
    text="Search Weather",
    command=search_weather
)
search_button.pack(pady=10)


# result display
result_text = tk.StringVar()

result_label = tk.Label(
    window,
    textvariable=result_text,
    justify="left",
    font=("Arial", 10)
)
result_label.pack(pady=10)


# start GUI
window.mainloop()