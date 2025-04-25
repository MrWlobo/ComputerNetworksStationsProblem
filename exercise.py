class Exercise:
    def __init__(self, number, description, stations):
        self.number = number
        self.description = description
        self.stations = stations

    # Returns True if exercise can be performed on at least one of the available stations, False otherwise
    def station_match(self, available_stations):
        stations_indices = [int(number) - 1 for number in available_stations]
        return any(self.stations[index] for index in stations_indices)

    def __repr__(self):
        return f"{self.number}: {self.stations}, {self.description}"
