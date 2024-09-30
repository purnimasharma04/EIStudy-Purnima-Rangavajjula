package com.example.designpatterns.structural.decorator;

import java.util.logging.Logger;

// Component interface
interface Coffee {
    String getDescription();
    double getCost();
}

// Concrete component
class SimpleCoffee implements Coffee {
    @Override
    public String getDescription() {
        return "Simple Coffee";
    }

    @Override
    public double getCost() {
        return 1.0;
    }
}

// Decorator
abstract class CoffeeDecorator implements Coffee {
    protected Coffee decoratedCoffee;

    public CoffeeDecorator(Coffee coffee) {
        this.decoratedCoffee = coffee;
    }

    public String getDescription() {
        return decoratedCoffee.getDescription();
    }

    public double getCost() {
        return decoratedCoffee.getCost();
    }
}

// Concrete decorators
class Milk extends CoffeeDecorator {
    public Milk(Coffee coffee) {
        super(coffee);
    }

    @Override
    public String getDescription() {
        return decoratedCoffee.getDescription() + ", Milk";
    }

    @Override
    public double getCost() {
        return decoratedCoffee.getCost() + 0.5;
    }
}

class Sugar extends CoffeeDecorator {
    public Sugar(Coffee coffee) {
        super(coffee);
    }

    @Override
    public String getDescription() {
        return decoratedCoffee.getDescription() + ", Sugar";
    }

    @Override
    public double getCost() {
        return decoratedCoffee.getCost() + 0.2;
    }
}

class Whip extends CoffeeDecorator {
    public Whip(Coffee coffee) {
        super(coffee);
    }

    @Override
    public String getDescription() {
        return decoratedCoffee.getDescription() + ", Whip";
    }

    @Override
    public double getCost() {
        return decoratedCoffee.getCost() + 0.7;
    }
}

public class CoffeeShop {
    private static final Logger logger = Logger.getLogger(CoffeeShop.class.getName());

    public static void demo() {
        // Order a simple coffee
        Coffee coffee = new SimpleCoffee();
        logger.info("Order: " + coffee.getDescription() + " Cost: $" + coffee.getCost());

        // Decorate it with milk
        Coffee milkCoffee = new Milk(coffee);
        logger.info("Order: " + milkCoffee.getDescription() + " Cost: $" + milkCoffee.getCost());

        // Decorate it with milk and sugar
        Coffee sweetMilkCoffee = new Sugar(new Milk(coffee));
        logger.info("Order: " + sweetMilkCoffee.getDescription() + " Cost: $" + sweetMilkCoffee.getCost());

        // Create a complex coffee with all toppings
        Coffee specialCoffee = new Whip(new Sugar(new Milk(coffee)));
        logger.info("Order: " + specialCoffee.getDescription() + " Cost: $" + specialCoffee.getCost());

        logger.info("Coffee Shop demo completed.");
    }
}
