const { dbGet, dbRun } = require('../database');

const userModel = {
    async findByEmail(email) {
        return dbGet("SELECT id FROM users WHERE email = ?", [email]);
    },

    async findById(id) {
        return dbGet("SELECT id, name, email FROM users WHERE id = ?", [id]);
    },

    async create(name, email, pass) {
        const result = await dbRun(
            "INSERT INTO users (name, email, pass) VALUES (?, ?, ?)",
            [name, email, pass]
        );
        return result.lastID;
    },

    async deleteById(id) {
        await dbRun("DELETE FROM enrollments WHERE user_id = ?", [id]);
        await dbRun("DELETE FROM payments WHERE enrollment_id IN (SELECT id FROM enrollments WHERE user_id = ?)", [id]);
        await dbRun("DELETE FROM users WHERE id = ?", [id]);
    }
};

module.exports = userModel;
