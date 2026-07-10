const config = {
    dbUser: process.env.DB_USER || "admin",
    dbPass: process.env.DB_PASS || "password",
    paymentGatewayKey: process.env.PAYMENT_KEY || "",
    smtpUser: process.env.SMTP_USER || "no-reply@example.com",
    port: parseInt(process.env.PORT || "3000", 10)
};

module.exports = { config };
