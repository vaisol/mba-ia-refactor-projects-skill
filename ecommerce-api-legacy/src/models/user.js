const { dbGet, dbAll, dbRun } = require('../database');

const userModel = {
    async findByEmail(email) {
        return dbGet("SELECT id FROM users WHERE email = ?", [email]);
    },

    async findById(id) {
        return dbGet("SELECT id, name, email FROM users WHERE id = ?", [id]);
    },

    async findAll() {
        return dbAll("SELECT id, name, email FROM users");
    },

    async create(name, email, pass) {
        const result = await dbRun(
            "INSERT INTO users (name, email, pass) VALUES (?, ?, ?)",
            [name, email, pass]
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
        await dbRun(`UPDATE users SET ${sets.join(', ')} WHERE id = ?`, values);
    },

    async deleteById(id) {
        await dbRun("DELETE FROM payments WHERE enrollment_id IN (SELECT id FROM enrollments WHERE user_id = ?)", [id]);
        await dbRun("DELETE FROM enrollments WHERE user_id = ?", [id]);
        await dbRun("DELETE FROM users WHERE id = ?", [id]);
    }
};

module.exports = userModel;
