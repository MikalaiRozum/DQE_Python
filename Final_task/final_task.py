import os
import sqlite3
import pyodbc
from math import radians, cos, sin, asin, sqrt

script_directory = os.path.dirname(os.path.abspath(__file__))
# Check if the database file exists, and create it if not
if 'full_db.db' not in script_directory:
    connection = sqlite3.connect('full_db.db')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS city '
                   '(id INTEGER PRIMARY KEY AUTOINCREMENT, city_name TEXT, longitude TEXT, latitude TEXT)')
    connection.commit()
    connection.close()

class DatabaseHandler:
    def __init__(self):
        self.connection = pyodbc.connect("DRIVER={SQLite3 ODBC Driver};"
                                         " DIRECT=True; "
                                         "DATABASE=full_db.db; "
                                         "String Types=Unicode")
        self.cursor = self.connection.cursor()

    def calculate_distance(self, city_1, city_2):
        # Get coordinates from database or ask user for input
        coordinates1 = self.get_coordinates_from_db(city_1)
        coordinates2 = self.get_coordinates_from_db(city_2)
        if not coordinates1:
            coordinates1 = self.get_user_coordinates(city_1)
        if not coordinates2:
            coordinates2 = self.get_user_coordinates(city_2)

        # Calculation of distance between two coordinates
        distance_km = self.calculate_circle_distance(coordinates1, coordinates2)

        return distance_km

    def get_coordinates_from_db(self, city_name):
        # Select coordinates from the database based on city name
        query = "SELECT longitude, latitude FROM city WHERE city_name = ?"
        result = self.cursor.execute(query, (city_name,)).fetchone()

        if result:
            longitude, latitude = result
            return float(longitude), float(latitude)
        else:
            return None

    def get_user_coordinates(self, city_name):
        # Ask user for city coordinates and insert to the database
        longitude = input(f"Enter the longitude for {city_name}: ")
        latitude = input(f"Enter the latitude for {city_name}: ")

        query = "INSERT INTO city (city_name, longitude, latitude) VALUES (?, ?, ?)"
        self.cursor.execute(query, (city_name, longitude, latitude))
        self.connection.commit()

        return float(longitude), float(latitude)

    @staticmethod
    def calculate_circle_distance(coordinates1, coordinates2):
        # Haversine formula for calculating the great-circle distance
        # Convert decimal degrees to radians
        lon1, lat1 = map(radians, coordinates1)
        lon2, lat2 = map(radians, coordinates2)

        diff_lon = lon2 - lon1
        diff_lat = lat2 - lat1
        a = sin(diff_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(diff_lon / 2) ** 2
        c = 2 * asin(sqrt(a))
        # Radius of earth in kilometers
        r = 6371.0
        distance_km = r * c

        return distance_km


if __name__ == "__main__":
    db_handler = DatabaseHandler()
    city1 = input("Enter the first city name: ")
    city2 = input("Enter the second city name: ")
    distance = db_handler.calculate_distance(city1, city2)
    print(f"The straight-line distance between {city1} and {city2} is approximately {distance:.2f} kilometers.")