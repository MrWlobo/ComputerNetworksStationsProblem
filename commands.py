class Commands:

    # Filter exercises according to provided available stations
    @classmethod
    def _filter_and_print(cls, all_exercises, chosen_exercises, available_stations_list, should_match):
        exercises_count = 0
        for exercise in all_exercises:
            if exercise.number in chosen_exercises:
                match = exercise.station_match(available_stations_list) or len(available_stations_list) == 0
                if match == should_match:
                    print(exercise)
                    exercises_count += 1
        print(f"Dostępnych ćwiczeń: {exercises_count}\n")

    # Show exercises that are possible to do on given stations
    @classmethod
    def show_command(cls, all_exercises, chosen_exercises, available_stations_list):
        cls._filter_and_print(all_exercises, chosen_exercises, available_stations_list, should_match=True)

    # Show exercises that are impossible to do on given stations
    @classmethod
    def no_show_command(cls, all_exercises, chosen_exercises, available_stations_list):
        cls._filter_and_print(all_exercises, chosen_exercises, available_stations_list, should_match=False)

    # Add new exercises to the list
    @classmethod
    def add_command(cls, exercises_file, exercises_to_add):
        with open(exercises_file, "r") as f:
            current_exercises = f.readlines()

        for exercise in exercises_to_add:
            current_exercises.append(f"{exercise}\n")
        current_exercises.sort()

        with open(exercises_file, "w") as f:
            f.writelines(current_exercises)

        return [exercise.strip() for exercise in current_exercises]

    # Remove chosen exercises from the list
    @classmethod
    def no_add_command(cls, exercises_file, exercises_to_remove):
        with open(exercises_file, "r") as f:
            current_exercises = f.readlines()

        updated_exercises = [exercise for exercise in current_exercises if exercise.strip() not in exercises_to_remove]

        with open(exercises_file, "w") as f:
            f.writelines(updated_exercises)

        return [exercise.strip() for exercise in updated_exercises]
