const { config } = require('../config/settings');

function processPayment(cardNumber) {
    if (!cardNumber || typeof cardNumber !== 'string') {
        return "DENIED";
    }
    return cardNumber.startsWith("4") ? "PAID" : "DENIED";
}

module.exports = { processPayment };
