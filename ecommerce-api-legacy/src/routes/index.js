const { checkout, AppError } = require('../controllers/checkout_controller');
const financialController = require('../controllers/financial_controller');
const userController = require('../controllers/user_controller');
const courseController = require('../controllers/course_controller');
const enrollmentController = require('../controllers/enrollment_controller');

function registerRoutes(app) {
    app.get('/health', (req, res) => {
        res.json({ status: 'ok' });
    });

    app.post('/api/checkout', async (req, res, next) => {
        try {
            const { usr, eml, pwd, c_id, card } = req.body;
            if (!usr || !eml || !c_id || !card) {
                return res.status(400).json({ error: "Bad Request" });
            }
            const result = await checkout(usr, eml, pwd, c_id, card);
            res.status(200).json(result);
        } catch (err) {
            if (err instanceof AppError) {
                return res.status(err.statusCode).json({ error: err.message });
            }
            next(err);
        }
    });

    app.get('/api/admin/financial-report', async (req, res, next) => {
        try {
            const report = await financialController.getFinancialReport();
            res.json(report);
        } catch (err) {
            next(err);
        }
    });

    // Users
    app.get('/api/users', async (req, res, next) => {
        try {
            const users = await userController.listUsers();
            res.json(users);
        } catch (err) {
            next(err);
        }
    });

    app.get('/api/users/:id', async (req, res, next) => {
        try {
            const user = await userController.getUserById(parseInt(req.params.id, 10));
            res.json(user);
        } catch (err) {
            if (err instanceof userController.AppError) {
                return res.status(err.statusCode).json({ error: err.message });
            }
            next(err);
        }
    });

    app.post('/api/users', async (req, res, next) => {
        try {
            const { name, email, pass } = req.body;
            const user = await userController.createUser(name, email, pass);
            res.status(201).json(user);
        } catch (err) {
            if (err instanceof userController.AppError) {
                return res.status(err.statusCode).json({ error: err.message });
            }
            next(err);
        }
    });

    app.put('/api/users/:id', async (req, res, next) => {
        try {
            const user = await userController.updateUser(parseInt(req.params.id, 10), req.body);
            res.json(user);
        } catch (err) {
            if (err instanceof userController.AppError) {
                return res.status(err.statusCode).json({ error: err.message });
            }
            next(err);
        }
    });

    app.delete('/api/users/:id', async (req, res, next) => {
        try {
            const result = await userController.deleteUser(parseInt(req.params.id, 10));
            res.json(result);
        } catch (err) {
            if (err instanceof userController.AppError) {
                return res.status(err.statusCode).json({ error: err.message });
            }
            next(err);
        }
    });

    // Courses
    app.get('/api/courses', async (req, res, next) => {
        try {
            const courses = await courseController.listCourses();
            res.json(courses);
        } catch (err) {
            next(err);
        }
    });

    app.get('/api/courses/:id', async (req, res, next) => {
        try {
            const course = await courseController.getCourseById(parseInt(req.params.id, 10));
            res.json(course);
        } catch (err) {
            if (err instanceof courseController.AppError) {
                return res.status(err.statusCode).json({ error: err.message });
            }
            next(err);
        }
    });

    app.post('/api/courses', async (req, res, next) => {
        try {
            const { title, price } = req.body;
            const course = await courseController.createCourse(title, price);
            res.status(201).json(course);
        } catch (err) {
            if (err instanceof courseController.AppError) {
                return res.status(err.statusCode).json({ error: err.message });
            }
            next(err);
        }
    });

    app.put('/api/courses/:id', async (req, res, next) => {
        try {
            const course = await courseController.updateCourse(parseInt(req.params.id, 10), req.body);
            res.json(course);
        } catch (err) {
            if (err instanceof courseController.AppError) {
                return res.status(err.statusCode).json({ error: err.message });
            }
            next(err);
        }
    });

    app.delete('/api/courses/:id', async (req, res, next) => {
        try {
            const result = await courseController.deleteCourse(parseInt(req.params.id, 10));
            res.json(result);
        } catch (err) {
            if (err instanceof courseController.AppError) {
                return res.status(err.statusCode).json({ error: err.message });
            }
            next(err);
        }
    });

    // Enrollments
    app.get('/api/enrollments', async (req, res, next) => {
        try {
            const enrollments = await enrollmentController.listEnrollments();
            res.json(enrollments);
        } catch (err) {
            next(err);
        }
    });

    app.get('/api/enrollments/:id', async (req, res, next) => {
        try {
            const enrollment = await enrollmentController.getEnrollmentById(parseInt(req.params.id, 10));
            res.json(enrollment);
        } catch (err) {
            if (err instanceof enrollmentController.AppError) {
                return res.status(err.statusCode).json({ error: err.message });
            }
            next(err);
        }
    });

    app.post('/api/enrollments', async (req, res, next) => {
        try {
            const { user_id, course_id } = req.body;
            const enrollment = await enrollmentController.createEnrollment(user_id, course_id);
            res.status(201).json(enrollment);
        } catch (err) {
            if (err instanceof enrollmentController.AppError) {
                return res.status(err.statusCode).json({ error: err.message });
            }
            next(err);
        }
    });

    app.put('/api/enrollments/:id', async (req, res, next) => {
        try {
            const enrollment = await enrollmentController.updateEnrollment(parseInt(req.params.id, 10), req.body);
            res.json(enrollment);
        } catch (err) {
            if (err instanceof enrollmentController.AppError) {
                return res.status(err.statusCode).json({ error: err.message });
            }
            next(err);
        }
    });

    app.delete('/api/enrollments/:id', async (req, res, next) => {
        try {
            const result = await enrollmentController.deleteEnrollment(parseInt(req.params.id, 10));
            res.json(result);
        } catch (err) {
            if (err instanceof enrollmentController.AppError) {
                return res.status(err.statusCode).json({ error: err.message });
            }
            next(err);
        }
    });
}

module.exports = { registerRoutes };
