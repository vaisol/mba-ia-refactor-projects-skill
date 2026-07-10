const { dbGet, dbAll, dbRun } = require('../database');

const courseModel = {
    async findById(id) {
        return dbGet("SELECT * FROM courses WHERE id = ? AND active = 1", [id]);
    },

    async findAll() {
        return dbAll("SELECT * FROM courses");
    },

    async create(title, price) {
        const result = await dbRun(
            "INSERT INTO courses (title, price, active) VALUES (?, ?, 1)",
            [title, price]
        );
        return result.lastID;
    },

    async updateById(id, fields) {
        const sets = [];
        const values = [];
        for (const [key, val] of Object.entries(fields)) {
            if (val !== undefined) {
                sets.push(`${key} = ?`);
                values.push(val);
            }
        }
        if (sets.length === 0) return;
        values.push(id);
        await dbRun(`UPDATE courses SET ${sets.join(', ')} WHERE id = ?`, values);
    },

    async deleteById(id) {
        await dbRun("UPDATE courses SET active = 0 WHERE id = ?", [id]);
    }
};

module.exports = courseModel;
