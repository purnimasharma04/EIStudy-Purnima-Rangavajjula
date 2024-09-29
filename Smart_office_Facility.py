import datetime
from abc import ABC, abstractmethod
from typing import List, Dict

# Singleton Pattern
class OfficeFacility:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.rooms = {}
        return cls._instance

    def configure_rooms(self, room_count: int):
        self.rooms = {i: Room(i) for i in range(1, room_count + 1)}
        return f"Office configured with {room_count} meeting rooms: " + ", ".join([f"Room {i}" for i in range(1, room_count + 1)])

    def set_room_capacity(self, room_number: int, capacity: int):
        if room_number not in self.rooms:
            return f"Room {room_number} does not exist."
        if capacity <= 0:
            return "Invalid capacity. Please enter a valid positive number."
        self.rooms[room_number].set_capacity(capacity)
        return f"Room {room_number} maximum capacity set to {capacity}."

    def get_room(self, room_number: int):
        return self.rooms.get(room_number)

# Observer Pattern
class OccupancyObserver(ABC):
    @abstractmethod
    def update(self, is_occupied: bool):
        pass

class ACSystem(OccupancyObserver):
    def update(self, is_occupied: bool):
        if is_occupied:
            print("AC turned on.")
        else:
            print("AC turned off.")

class LightingSystem(OccupancyObserver):
    def update(self, is_occupied: bool):
        if is_occupied:
            print("Lights turned on.")
        else:
            print("Lights turned off.")

class Room:
    def __init__(self, room_number: int):
        self.room_number = room_number
        self.capacity = 0
        self.occupants = 0
        self.booking = None
        self.observers: List[OccupancyObserver] = [ACSystem(), LightingSystem()]
        self.last_occupied_time = None

    def set_capacity(self, capacity: int):
        self.capacity = capacity

    def add_occupants(self, count: int):
        if count < 2:
            return f"Room {self.room_number} occupancy insufficient to mark as occupied."
        self.occupants += count
        self.last_occupied_time = datetime.datetime.now()
        self.notify_observers(True)
        return f"Room {self.room_number} is now occupied by {self.occupants} persons. AC and lights turned on."

    def remove_occupants(self, count: int):
        self.occupants = max(0, self.occupants - count)
        if self.occupants == 0:
            self.notify_observers(False)
            return f"Room {self.room_number} is now unoccupied. AC and lights turned off."
        return f"Room {self.room_number} now has {self.occupants} occupants."

    def notify_observers(self, is_occupied: bool):
        for observer in self.observers:
            observer.update(is_occupied)

    def is_occupied(self):
        return self.occupants > 0

    def check_automatic_release(self):
        if not self.is_occupied() and self.booking:
            current_time = datetime.datetime.now()
            if (current_time - self.last_occupied_time).total_seconds() > 300:  # 5 minutes
                self.booking = None
                return f"Room {self.room_number} is now unoccupied. Booking released. AC and lights off."
        return None

# Command Pattern
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class BookRoomCommand(Command):
    def __init__(self, room: Room, start_time: datetime.datetime, duration: int):
        self.room = room
        self.start_time = start_time
        self.duration = duration

    def execute(self):
        if self.room.booking:
            return f"Room {self.room.room_number} is already booked during this time. Cannot book."
        self.room.booking = (self.start_time, self.duration)
        return f"Room {self.room.room_number} booked from {self.start_time.strftime('%H:%M')} for {self.duration} minutes."

class CancelBookingCommand(Command):
    def __init__(self, room: Room):
        self.room = room

    def execute(self):
        if not self.room.booking:
            return f"Room {self.room.room_number} is not booked. Cannot cancel booking."
        self.room.booking = None
        return f"Booking for Room {self.room.room_number} cancelled successfully."

class SmartOfficeSystem:
    def __init__(self):
        self.office = OfficeFacility()

    def execute_command(self, command: Command):
        return command.execute()

    def process_input(self, input_string: str):
        parts = input_string.split()
        command = parts[0].lower()

        if command == "config":
            if parts[1] == "room" and parts[2] == "count":
                return self.office.configure_rooms(int(parts[3]))
            elif parts[1] == "room" and parts[2] == "max" and parts[3] == "capacity":
                return self.office.set_room_capacity(int(parts[4]), int(parts[5]))

        elif command == "add" and parts[1] == "occupant":
            room = self.office.get_room(int(parts[2]))
            if room:
                return room.add_occupants(int(parts[3]))
            return f"Room {parts[2]} does not exist."

        elif command == "block" and parts[1] == "room":
            room = self.office.get_room(int(parts[2]))
            if room:
                start_time = datetime.datetime.strptime(parts[3], "%H:%M")
                duration = int(parts[4])
                return self.execute_command(BookRoomCommand(room, start_time, duration))
            return f"Room {parts[2]} does not exist."

        elif command == "cancel" and parts[1] == "room":
            room = self.office.get_room(int(parts[2]))
            if room:
                return self.execute_command(CancelBookingCommand(room))
            return f"Room {parts[2]} does not exist."

        elif command == "room" and parts[1] == "status":
            room = self.office.get_room(int(parts[2]))
            if room:
                return room.check_automatic_release() or f"Room {parts[2]} status: {'Occupied' if room.is_occupied() else 'Unoccupied'}"
            return f"Room {parts[2]} does not exist."

        return "Invalid command. Please try again."

# Main execution
if __name__ == "__main__":
    system = SmartOfficeSystem()
    print("Welcome to the Smart Office Facility Management System!")
    print("Enter commands to interact with the system (type 'exit' to quit):")

    while True:
        user_input = input("> ")
        if user_input.lower() == 'exit':
            break
        result = system.process_input(user_input)
        print(result)

    print("Thank you for using the Smart Office Facility Management System!")
