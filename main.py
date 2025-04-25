from bs4 import BeautifulSoup
import requests
import re

from exercise import Exercise
from commands import Commands

url = "http://sieci.kis.agh.edu.pl/zasoby.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

exercises_file = "exercises.txt"

pattern = r"\b\d{3}\b"

# All exercises from provided website
all_exercises = []
# Only exercises matching the numbers provided in exercises.txt
chosen_exercises = []

# Dummy exercise
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
with open(exercises_file, "r") as f:
    chosen_exercises = [number.strip() for number in f.readlines()]

# Main loop
run = True
prefix = "Switch#"

while run:

    command = input(f"{prefix} ").split(" ")

    if command[0] == "show":
        available_stations_list = command[1:]
        Commands.show_command(all_exercises, chosen_exercises, available_stations_list)

    elif command[0] == "no" and command[1] == "show":
        available_stations_list = command[2:]
        Commands.no_show_command(all_exercises, chosen_exercises, available_stations_list)

    elif command[0] == "add":
        exercises_to_add = command[1:]
        chosen_exercises = Commands.add_command(exercises_file, exercises_to_add)

    elif command[0] == "no" and command[1] == "add":
        exercises_to_remove = command[2:]
        chosen_exercises = Commands.no_add_command(exercises_file, exercises_to_remove)

    elif command[0] == "shutdown":
        run = False

    elif command[0] == "":
        pass

    else:
        print(f"{prefix} Command not recognized")
