const enrollmentModel = require('../models/enrollment');

async function listEnrollments() {
    return enrollmentModel.findAll();
}

async function getEnrollmentById(id) {
    const enrollment = await enrollmentModel.findById(id);
    if (!enrollment) {
        throw new AppError("Matrícula não encontrada", 404);
    }
    return enrollment;
}

async function createEnrollment(userId, courseId) {
    if (!userId || !courseId) {
        throw new AppError("user_id e course_id são obrigatórios", 400);
    }
    const id = await enrollmentModel.create(userId, courseId);
    return { id, user_id: userId, course_id: courseId };
}

async function updateEnrollment(id, fields) {
    const enrollment = await enrollmentModel.findById(id);
    if (!enrollment) {
        throw new AppError("Matrícula não encontrada", 404);
    }
    await enrollmentModel.updateById(id, fields);
    return { ...enrollment, ...fields };
}

async function deleteEnrollment(id) {
    const enrollment = await enrollmentModel.findById(id);
    if (!enrollment) {
        throw new AppError("Matrícula não encontrada", 404);
    }
    await enrollmentModel.deleteById(id);
    return { message: "Matrícula deletada com sucesso" };
}

class AppError extends Error {
    constructor(message, statusCode = 400) {
        super(message);
        this.statusCode = statusCode;
    }
}

module.exports = { listEnrollments, getEnrollmentById, createEnrollment, updateEnrollment, deleteEnrollment, AppError };
