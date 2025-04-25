from bs4 import BeautifulSoup
import requests
import re

from exercise import Exercise
from commands import Commands


def fetch_exercises(url: str) -> list[Exercise]:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Three-digit numbers, leading zeros allowed
    pattern = r"\b\d{3}\b"

    # All exercises from provided website
    all_exercises = []

    # Dummy exercise
    current_exercise_number = None
    current_exercise_description = ""
    current_exercise_stations = []

    is_next_row_description = False

    # Get all exercises
    for heading in soup.find_all("table", class_="texttable"):
        for row in heading.find_all("td"):

            # Load the description of the exercise
            if is_next_row_description:
                current_exercise_description = row.text.encode('latin1').decode('utf-8')
                is_next_row_description = False

            # Load the number of the exercise
            if re.fullmatch(pattern, row.text):
                # If current_exercise variables are not default, create new Exercise object and reset the values
                if current_exercise_number is not None:
                    all_exercises.append(Exercise(current_exercise_number,
                                                  current_exercise_description,
                                                  current_exercise_stations[:]))

                    current_exercise_number = None
                    current_exercise_description = ""
                    current_exercise_stations.clear()
                current_exercise_number = row.text
                is_next_row_description = True

            # class == y -> can do exercise on the given station
            if row.get("class") and row.get("class")[0] == "y":
                current_exercise_stations.append(1)

            # class == n -> can't do exercise on the given station
            elif row.get("class") and row.get("class")[0] == "n":
                current_exercise_stations.append(0)

    # Sort exercise by number
    all_exercises.sort(key=lambda x: x.number)
    return all_exercises


def load_chosen_exercises(file: str) -> list[str]:
    with open(file, "r") as f:
        chosen_exercises = [number.strip() for number in f.readlines()]
    return chosen_exercises


def command_loop(all_exercises, chosen_exercises, exercises_file):
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


if __name__ == "__main__":
    URL = "http://sieci.kis.agh.edu.pl/zasoby.html"
    EXERCISES_FILE = "exercises.txt"

    all_exercises = fetch_exercises(URL)
    chosen_exercises = load_chosen_exercises(EXERCISES_FILE)
    command_loop(all_exercises, chosen_exercises, EXERCISES_FILE)
