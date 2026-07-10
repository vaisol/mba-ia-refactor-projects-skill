const { dbGet, dbAll, dbRun } = require('../database');

const enrollmentModel = {
    async findById(id) {
        return dbGet("SELECT * FROM enrollments WHERE id = ?", [id]);
    },

    async findAll() {
        return dbAll("SELECT * FROM enrollments");
    },

    async create(userId, courseId) {
        const result = await dbRun(
            "INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)",
            [userId, courseId]
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
        await dbRun(`UPDATE enrollments SET ${sets.join(', ')} WHERE id = ?`, values);
    },

    async deleteById(id) {
        await dbRun("DELETE FROM payments WHERE enrollment_id = ?", [id]);
        await dbRun("DELETE FROM enrollments WHERE id = ?", [id]);
    }
};

module.exports = enrollmentModel;
