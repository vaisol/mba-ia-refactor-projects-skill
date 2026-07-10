const { dbRun } = require('../database');

const auditModel = {
    async log(action) {
        await dbRun(
            "INSERT INTO audit_logs (action, created_at) VALUES (?, datetime('now'))",
            [action]
        );
    }
};

module.exports = auditModel;
