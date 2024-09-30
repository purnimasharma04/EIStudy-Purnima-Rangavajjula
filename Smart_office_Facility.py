import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

// Singleton Pattern
class OfficeFacility {
    private static OfficeFacility instance;
    private Map<Integer, Room> rooms;

    private OfficeFacility() {
        rooms = new HashMap<>();
    }

    public static OfficeFacility getInstance() {
        if (instance == null) {
            instance = new OfficeFacility();
        }
        return instance;
    }

    public String configureRooms(int roomCount) {
        rooms.clear();
        for (int i = 1; i <= roomCount; i++) {
            rooms.put(i, new Room(i));
        }
        return String.format("Office configured with %d meeting rooms: %s", roomCount,
                String.join(", ", rooms.keySet().stream().map(k -> "Room " + k).toArray(String[]::new)));
    }

    public String setRoomCapacity(int roomNumber, int capacity) {
        if (!rooms.containsKey(roomNumber)) {
            return String.format("Room %d does not exist.", roomNumber);
        }
        if (capacity <= 0) {
            return "Invalid capacity. Please enter a valid positive number.";
        }
        rooms.get(roomNumber).setCapacity(capacity);
        return String.format("Room %d maximum capacity set to %d.", roomNumber, capacity);
    }

    public Room getRoom(int roomNumber) {
        return rooms.get(roomNumber);
    }
}

// Observer Pattern
interface OccupancyObserver {
    void update(boolean isOccupied);
}

class ACSystem implements OccupancyObserver {
    @Override
    public void update(boolean isOccupied) {
        System.out.println(isOccupied ? "AC turned on." : "AC turned off.");
    }
}

class LightingSystem implements OccupancyObserver {
    @Override
    public void update(boolean isOccupied) {
        System.out.println(isOccupied ? "Lights turned on." : "Lights turned off.");
    }
}

class Room {
    private int roomNumber;
    private int capacity;
    private int occupants;
    private Booking booking;
    private List<OccupancyObserver> observers;
    private LocalDateTime lastOccupiedTime;

    public Room(int roomNumber) {
        this.roomNumber = roomNumber;
        this.capacity = 0;
        this.occupants = 0;
        this.observers = new ArrayList<>();
        observers.add(new ACSystem());
        observers.add(new LightingSystem());
    }

    public void setCapacity(int capacity) {
        this.capacity = capacity;
    }

    public String addOccupants(int count) {
        if (count < 2) {
            return String.format("Room %d occupancy insufficient to mark as occupied.", roomNumber);
        }
        occupants += count;
        lastOccupiedTime = LocalDateTime.now();
        notifyObservers(true);
        return String.format("Room %d is now occupied by %d persons. AC and lights turned on.", roomNumber, occupants);
    }

    public String removeOccupants(int count) {
        occupants = Math.max(0, occupants - count);
        if (occupants == 0) {
            notifyObservers(false);
            return String.format("Room %d is now unoccupied. AC and lights turned off.", roomNumber);
        }
        return String.format("Room %d now has %d occupants.", roomNumber, occupants);
    }

    private void notifyObservers(boolean isOccupied) {
        for (OccupancyObserver observer : observers) {
            observer.update(isOccupied);
        }
    }

    public boolean isOccupied() {
        return occupants > 0;
    }

    public String checkAutomaticRelease() {
        if (!isOccupied() && booking != null) {
            LocalDateTime currentTime = LocalDateTime.now();
            if (currentTime.isAfter(lastOccupiedTime.plusMinutes(5))) {
                booking = null;
                return String.format("Room %d is now unoccupied. Booking released. AC and lights off.", roomNumber);
            }
        }
        return null;
    }

    public Booking getBooking() {
        return booking;
    }

    public void setBooking(Booking booking) {
        this.booking = booking;
    }
}

class Booking {
    private LocalDateTime startTime;
    private int duration;

    public Booking(LocalDateTime startTime, int duration) {
        this.startTime = startTime;
        this.duration = duration;
    }
}

// Command Pattern
interface Command {
    String execute();
}

class BookRoomCommand implements Command {
    private Room room;
    private LocalDateTime startTime;
    private int duration;

    public BookRoomCommand(Room room, LocalDateTime startTime, int duration) {
        this.room = room;
        this.startTime = startTime;
        this.duration = duration;
    }

    @Override
    public String execute() {
        if (room.getBooking() != null) {
            return String.format("Room %d is already booked during this time. Cannot book.", room.roomNumber);
        }
        room.setBooking(new Booking(startTime, duration));
        return String.format("Room %d booked from %s for %d minutes.", room.roomNumber,
                startTime.format(DateTimeFormatter.ofPattern("HH:mm")), duration);
    }
}

class CancelBookingCommand implements Command {
    private Room room;

    public CancelBookingCommand(Room room) {
        this.room = room;
    }

    @Override
    public String execute() {
        if (room.getBooking() == null) {
            return String.format("Room %d is not booked. Cannot cancel booking.", room.roomNumber);
        }
        room.setBooking(null);
        return String.format("Booking for Room %d cancelled successfully.", room.roomNumber);
    }
}

class SmartOfficeSystem {
    private OfficeFacility office;

    public SmartOfficeSystem() {
        this.office = OfficeFacility.getInstance();
    }

    public String executeCommand(Command command) {
        return command.execute();
    }

    public String processInput(String input) {
        String[] parts = input.split(" ");
        String command = parts[0].toLowerCase();

        switch (command) {
            case "config":
                if (parts[1].equals("room") && parts[2].equals("count")) {
                    return office.configureRooms(Integer.parseInt(parts[3]));
                } else if (parts[1].equals("room") && parts[2].equals("max") && parts[3].equals("capacity")) {
                    return office.setRoomCapacity(Integer.parseInt(parts[4]), Integer.parseInt(parts[5]));
                }
                break;
            case "add":
                if (parts[1].equals("occupant")) {
                    Room room = office.getRoom(Integer.parseInt(parts[2]));
                    if (room != null) {
                        return room.addOccupants(Integer.parseInt(parts[3]));
                    }
                    return String.format("Room %s does not exist.", parts[2]);
                }
                break;
            case "block":
                if (parts[1].equals("room")) {
                    Room room = office.getRoom(Integer.parseInt(parts[2]));
                    if (room != null) {
                        LocalDateTime startTime = LocalDateTime.parse(parts[3], DateTimeFormatter.ofPattern("HH:mm"));
                        int duration = Integer.parseInt(parts[4]);
                        return executeCommand(new BookRoomCommand(room, startTime, duration));
                    }
                    return String.format("Room %s does not exist.", parts[2]);
                }
                break;
            case "cancel":
                if (parts[1].equals("room")) {
                    Room room = office.getRoom(Integer.parseInt(parts[2]));
                    if (room != null) {
                        return executeCommand(new CancelBookingCommand(room));
                    }
                    return String.format("Room %s does not exist.", parts[2]);
                }
                break;
            case "room":
                if (parts[1].equals("status")) {
                    Room room = office.getRoom(Integer.parseInt(parts[2]));
                    if (room != null) {
                        String automaticRelease = room.checkAutomaticRelease();
                        if (automaticRelease != null) {
                            return automaticRelease;
                        }
                        return String.format("Room %s status: %s", parts[2], room.isOccupied() ? "Occupied" : "Unoccupied");
                    }
                    return String.format("Room %s does not exist.", parts[2]);
                }
                break;
        }

        return "Invalid command. Please try again.";
    }

    public static void main(String[] args) {
        SmartOfficeSystem system = new SmartOfficeSystem();
        Scanner scanner = new Scanner(System.in);

        System.out.println("Welcome to the Smart Office Facility Management System!");
        System.out.println("Enter commands to interact with the system (type 'exit' to quit):");

        while (true) {
            System.out.print("> ");
            String userInput = scanner.nextLine();
            if (userInput.equalsIgnoreCase("exit")) {
                break;
            }
            String result = system.processInput(userInput);
            System.out.println(result);
        }

        System.out.println("Thank you for using the Smart Office Facility Management System!");
        scanner.close();
    }
}
