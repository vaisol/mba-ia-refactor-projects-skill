const userModel = require('../models/user');

async function listUsers() {
    return userModel.findAll();
}

async function getUserById(id) {
    const user = await userModel.findById(id);
    if (!user) {
        throw new AppError("Usuário não encontrado", 404);
    }
    return user;
}

async function createUser(name, email, pass) {
    if (!name || !email || !pass) {
        throw new AppError("Nome, email e senha são obrigatórios", 400);
    }
    const existing = await userModel.findByEmail(email);
    if (existing) {
        throw new AppError("Email já cadastrado", 409);
    }
    const id = await userModel.create(name, email, pass);
    return { id, name, email };
}

async function updateUser(id, fields) {
    const user = await userModel.findById(id);
    if (!user) {
        throw new AppError("Usuário não encontrado", 404);
    }
    await userModel.updateById(id, fields);
    return { ...user, ...fields };
}

async function deleteUser(userId) {
    const user = await userModel.findById(userId);
    if (!user) {
        throw new AppError("Usuário não encontrado", 404);
    }
    await userModel.deleteById(userId);
    return { message: "Usuário deletado com sucesso" };
}

class AppError extends Error {
    constructor(message, statusCode = 400) {
        super(message);
        this.statusCode = statusCode;
    }
}

module.exports = { listUsers, getUserById, createUser, updateUser, deleteUser, AppError };
