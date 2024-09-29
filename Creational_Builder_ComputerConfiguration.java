package com.example.designpatterns.creational.builder;

import java.util.logging.Logger;

class Computer {
    private String CPU;
    private String RAM;
    private String storage;
    private String GPU;
    private String powerSupply;

    private Computer(ComputerBuilder builder) {
        this.CPU = builder.CPU;
        this.RAM = builder.RAM;
        this.storage = builder.storage;
        this.GPU = builder.GPU;
        this.powerSupply = builder.powerSupply;
    }

    @Override
    public String toString() {
        return "Computer{" +
                "CPU='" + CPU + '\'' +
                ", RAM='" + RAM + '\'' +
                ", storage='" + storage + '\'' +
                ", GPU='" + GPU + '\'' +
                ", powerSupply='" + powerSupply + '\'' +
                '}';
    }

    public static class ComputerBuilder {
        private String CPU;
        private String RAM;
        private String storage;
        private String GPU;
        private String powerSupply;

        public ComputerBuilder(String CPU, String RAM) {
            this.CPU = CPU;
            this.RAM = RAM;
        }

        public ComputerBuilder setStorage(String storage) {
            this.storage = storage;
            return this;
        }

        public ComputerBuilder setGPU(String GPU) {
            this.GPU = GPU;
            return this;
        }

        public ComputerBuilder setPowerSupply(String powerSupply) {
            this.powerSupply = powerSupply;
            return this;
        }

        public Computer build() {
            return new Computer(this);
        }
    }
}

public class ComputerShop {
    private static final Logger logger = Logger.getLogger(ComputerShop.class.getName());

    public static void demo() {
        Computer gamingPC = new Computer.ComputerBuilder("Intel i9", "32GB")
                .setStorage("1TB SSD")
                .setGPU("NVIDIA RTX 3080")
                .setPowerSupply("850W")
                .build();

        Computer officePC = new Computer.ComputerBuilder("Intel i5", "16GB")
                .setStorage("512GB SSD")
                .build();

        logger.info("Gaming PC: " + gamingPC);
        logger.info("Office PC: " + officePC);

        logger.info("Computer Shop demo completed.");
    }
}
