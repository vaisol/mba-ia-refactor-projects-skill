const courseModel = require('../models/course');

async function listCourses() {
    return courseModel.findAll();
}

async function getCourseById(id) {
    const course = await courseModel.findById(id);
    if (!course) {
        throw new AppError("Curso não encontrado", 404);
    }
    return course;
}

async function createCourse(title, price) {
    if (!title || price === undefined) {
        throw new AppError("Título e preço são obrigatórios", 400);
    }
    const id = await courseModel.create(title, price);
    return { id, title, price, active: 1 };
}

async function updateCourse(id, fields) {
    const course = await courseModel.findById(id);
    if (!course) {
        throw new AppError("Curso não encontrado", 404);
    }
    await courseModel.updateById(id, fields);
    return { ...course, ...fields };
}

async function deleteCourse(id) {
    const course = await courseModel.findById(id);
    if (!course) {
        throw new AppError("Curso não encontrado", 404);
    }
    await courseModel.deleteById(id);
    return { message: "Curso desativado com sucesso" };
}

class AppError extends Error {
    constructor(message, statusCode = 400) {
        super(message);
        this.statusCode = statusCode;
    }
}

module.exports = { listCourses, getCourseById, createCourse, updateCourse, deleteCourse, AppError };
