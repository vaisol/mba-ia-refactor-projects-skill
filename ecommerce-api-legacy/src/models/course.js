const { dbGet, dbAll } = require('../database');

const courseModel = {
    async findById(id) {
        return dbGet("SELECT * FROM courses WHERE id = ? AND active = 1", [id]);
    },

    async findAll() {
        return dbAll("SELECT * FROM courses");
    }
};

module.exports = courseModel;
