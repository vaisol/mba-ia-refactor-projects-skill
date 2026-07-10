const userModel = require('../models/user');
const courseModel = require('../models/course');
const enrollmentModel = require('../models/enrollment');
const paymentModel = require('../models/payment');
const auditModel = require('../models/audit');
const { hashPassword } = require('../services/crypto_service');
const { processPayment } = require('../services/payment_service');

const checkoutCache = {};

async function checkout(userName, email, password, courseId, cardNumber) {
    const course = await courseModel.findById(courseId);
    if (!course) {
        throw new AppError("Curso não encontrado", 404);
    }

    let user = await userModel.findByEmail(email);
    let userId;

    if (!user) {
        const hash = await hashPassword(password);
        userId = await userModel.create(userName, email, hash);
    } else {
        userId = user.id;
    }

    const paymentStatus = processPayment(cardNumber);
    if (paymentStatus === "DENIED") {
        throw new AppError("Pagamento recusado", 400);
    }

    const enrollmentId = await enrollmentModel.create(userId, courseId);
    await paymentModel.create(enrollmentId, course.price, paymentStatus);
    await auditModel.log(`Checkout curso ${courseId} por ${userId}`);

    checkoutCache[`last_checkout_${userId}`] = course.title;

    return { msg: "Sucesso", enrollment_id: enrollmentId };
}

async function deleteUser(userId) {
    await userModel.deleteById(userId);
    return { message: "Usuário deletado com sucesso" };
}

class AppError extends Error {
    constructor(message, statusCode = 400) {
        super(message);
        this.statusCode = statusCode;
    }
}

module.exports = { checkout, deleteUser, AppError };
