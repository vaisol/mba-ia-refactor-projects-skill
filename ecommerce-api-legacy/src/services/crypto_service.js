const bcrypt = require('bcrypt');
const SALT_ROUNDS = 10;

async function hashPassword(pwd) {
    return bcrypt.hash(pwd || "123456", SALT_ROUNDS);
}

async function verifyPassword(pwd, hash) {
    return bcrypt.compare(pwd, hash);
}

module.exports = { hashPassword, verifyPassword };
