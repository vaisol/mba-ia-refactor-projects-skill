const courseModel = require('../models/course');
const { dbAll, dbGet } = require('../database');

async function getFinancialReport() {
    const courses = await courseModel.findAll();
    const report = [];

    for (const course of courses) {
        const courseData = { course: course.title, revenue: 0, students: [] };
        const enrollments = await dbAll(
            "SELECT * FROM enrollments WHERE course_id = ?",
            [course.id]
        );

        for (const enr of enrollments) {
            const user = await dbGet(
                "SELECT name, email FROM users WHERE id = ?",
                [enr.user_id]
            );
            const payment = await dbGet(
                "SELECT amount, status FROM payments WHERE enrollment_id = ?",
                [enr.id]
            );

            if (payment && payment.status === 'PAID') {
                courseData.revenue += payment.amount;
            }

            courseData.students.push({
                student: user ? user.name : 'Unknown',
                paid: payment ? payment.amount : 0
            });
        }

        report.push(courseData);
    }

    return report;
}

module.exports = { getFinancialReport };
