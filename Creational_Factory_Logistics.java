package com.example.designpatterns.creational.factory;

import java.util.logging.Logger;

interface Transport {
    void deliver();
}

class Truck implements Transport {
    private static final Logger logger = Logger.getLogger(Truck.class.getName());

    @Override
    public void deliver() {
        logger.info("Delivering by land in a truck");
    }
}

class Ship implements Transport {
    private static final Logger logger = Logger.getLogger(Ship.class.getName());

    @Override
    public void deliver() {
        logger.info("Delivering by sea in a ship");
    }
}

class Plane implements Transport {
    private static final Logger logger = Logger.getLogger(Plane.class.getName());

    @Override
    public void deliver() {
        logger.info("Delivering by air in a plane");
    }
}

class LogisticsFactory {
    public Transport createTransport(String type) {
        switch (type.toLowerCase()) {
            case "truck":
                return new Truck();
            case "ship":
                return new Ship();
            case "plane":
                return new Plane();
            default:
                throw new IllegalArgumentException("Unknown transport type");
        }
    }
}

public class LogisticsApp {
    private static final Logger logger = Logger.getLogger(LogisticsApp.class.getName());

    public static void demo() {
        LogisticsFactory factory = new LogisticsFactory();

        Transport truck = factory.createTransport("truck");
        truck.deliver();

        Transport ship = factory.createTransport("ship");
        ship.deliver();

        Transport plane = factory.createTransport("plane");
        plane.deliver();

        logger.info("Logistics Application demo completed.");
    }
}
