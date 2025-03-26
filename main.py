from bs4 import BeautifulSoup
import requests
import re

from exercise import Exercise

url = "http://sieci.kis.agh.edu.pl/zasoby.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

pattern = r"\b\d{3}\b"

all_exercises = []
chosen_exercises = []

curr_ex_number = "000"
curr_ex_description = ""
curr_ex_stations = []

is_next_row_desc = False

# Get all exercises
for heading in soup.find_all("table", class_="texttable"):
    for row in heading.find_all("td"):
        # Load the description of the exercise
        if is_next_row_desc:
            curr_ex_description = row.text.encode('latin1').decode('utf-8')
            is_next_row_desc = False

        # Load the number of the exercise
        if re.fullmatch(pattern, row.text):
            # If curr_ex variables are not default, create new Exercise object and reset the values
            if curr_ex_number != "000":
                all_exercises.append(Exercise(curr_ex_number, curr_ex_description, curr_ex_stations[:]))
                curr_ex_number = "000"
                curr_ex_description = ""
                curr_ex_stations.clear()
            curr_ex_number = row.text
            is_next_row_desc = True

        # class == y -> can do exercise on the given station
        if row.get("class") and row.get("class")[0] == "y":
            curr_ex_stations.append(1)
        # class == n -> can't do exercise on the given station
        elif row.get("class") and row.get("class")[0] == "n":
            curr_ex_stations.append(0)

# Sort exercise by number
all_exercises.sort(key=lambda x: x.number)

# Get chosen exercises
with open("exercises.txt", "r") as f:
    chosen_exercises = [number.strip() for number in f.readlines()]

available_stations = input("Podaj dostępne stanowiska: ")
available_stations_list = available_stations.split(" ")

# Print out valid exercises
for exercise in all_exercises:
    if exercise.number in chosen_exercises and exercise.station_match(available_stations_list):
        print(exercise)
