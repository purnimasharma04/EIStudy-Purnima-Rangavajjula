package com.example.designpatterns.behavioral.strategy;

import java.util.logging.Logger;

interface PaymentStrategy {
    void pay(int amount);
}

class CreditCardPayment implements PaymentStrategy {
    private String name;
    private String cardNumber;
    private String cvv;
    private String dateOfExpiry;
    private static final Logger logger = Logger.getLogger(CreditCardPayment.class.getName());

    public CreditCardPayment(String name, String cardNumber, String cvv, String dateOfExpiry) {
        this.name = name;
        this.cardNumber = cardNumber;
        this.cvv = cvv;
        this.dateOfExpiry = dateOfExpiry;
    }

    @Override
    public void pay(int amount) {
        logger.info(amount + " paid with credit card");
    }
}

class PayPalPayment implements PaymentStrategy {
    private String emailId;
    private String password;
    private static final Logger logger = Logger.getLogger(PayPalPayment.class.getName());

    public PayPalPayment(String email, String pwd) {
        this.emailId = email;
        this.password = pwd;
    }

    @Override
    public void pay(int amount) {
        logger.info(amount + " paid using PayPal");
    }
}

class ShoppingCart {
    private static final Logger logger = Logger.getLogger(ShoppingCart.class.getName());

    public static void demo() {
        PaymentStrategy creditCardStrategy = new CreditCardPayment("John Doe", "1234567890123456", "786", "12/2025");
        PaymentStrategy paypalStrategy = new PayPalPayment("johndoe@example.com", "password");

        // Using credit card
        creditCardStrategy.pay(1000);

        // Using PayPal
        paypalStrategy.pay(500);

        logger.info("Shopping Cart demo completed.");
    }
}
