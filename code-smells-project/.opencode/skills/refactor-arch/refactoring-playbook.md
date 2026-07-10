# Refactoring Playbook

Concrete transformation patterns with before/after code examples. Apply these patterns when refactoring from legacy code to MVC architecture.

---

## Pattern 1: Extract Configuration

**When to use:** Secrets, database URLs, ports, or any environment-specific values are hardcoded in source files.

**Before (Python/Flask):**
```python
# app.py
app = Flask(__name__)
app.config["SECRET_KEY"] = "minha-chave-super-secreta-123"
app.config["DEBUG"] = True
app.run(host="0.0.0.0", port=5000, debug=True)
```

**After (Python/Flask):**
```python
# config/settings.py
import os

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")
DEBUG = os.environ.get("FLASK_DEBUG", "true").lower() == "true"
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", 5000))
DB_PATH = os.environ.get("DB_PATH", "loja.db")

# app.py
from flask import Flask
from config.settings import SECRET_KEY, DEBUG, HOST, PORT

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["DEBUG"] = DEBUG

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
```

**Before (Node.js/Express):**
```javascript
// utils.js
const config = {
    dbUser: "admin_master",
    dbPass: "senha_super_secreta_prod_123",
    paymentGatewayKey: "pk_live_1234567890abcdef",
    smtpUser: "no-reply@fullcycle.com.br",
    port: 3000
};
```

**After (Node.js/Express):**
```javascript
// src/config/settings.js
const config = {
    dbUser: process.env.DB_USER || "admin",
    dbPass: process.env.DB_PASS || "password",
    paymentGatewayKey: process.env.PAYMENT_KEY || "",
    smtpUser: process.env.SMTP_USER || "no-reply@example.com",
    port: parseInt(process.env.PORT || "3000", 10)
};
module.exports = { config };
```

---

## Pattern 2: Parameterize SQL Queries

**When to use:** SQL queries built with string concatenation or f-strings.

**Before (Python):**
```python
def get_produto_por_id(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM produtos WHERE id = " + str(id))
    row = cursor.fetchone()
    if row:
        return {"id": row["id"], "nome": row["nome"], "preco": row["preco"]}
    return None

def criar_produto(nome, descricao, preco, estoque, categoria):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO produtos (nome, descricao, preco, estoque, categoria) VALUES ('" +
        nome + "', '" + descricao + "', " + str(preco) + ", " + str(estoque) + ", '" + categoria + "')"
    )
    db.commit()
    return cursor.lastrowid
```

**After (Python — parameterized queries):**
```python
def get_produto_por_id(produto_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
    row = cursor.fetchone()
    if row:
        return {"id": row["id"], "nome": row["nome"], "preco": row["preco"]}
    return None

def criar_produto(nome, descricao, preco, estoque, categoria):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO produtos (nome, descricao, preco, estoque, categoria) VALUES (?, ?, ?, ?, ?)",
        (nome, descricao, preco, estoque, categoria)
    )
    db.commit()
    return cursor.lastrowid
```

**After (Python — SQLAlchemy ORM):**
```python
class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, default=0)
    categoria = db.Column(db.String(50))

    def to_dict(self):
        return {
            "id": self.id, "nome": self.nome, "descricao": self.descricao,
            "preco": self.preco, "estoque": self.estoque, "categoria": self.categoria
        }

# Usage:
# produto = Produto.query.get(produto_id)
# produto = Produto(nome="...", preco=9.99, ...)
# db.session.add(produto)
# db.session.commit()
```

---

## Pattern 3: Break God File into MVC Layers

**When to use:** A single file contains models, routes, and business logic all mixed together.

**Before (Node.js — God Class):**
```javascript
// AppManager.js — 140 lines doing EVERYTHING
class AppManager {
    constructor() {
        this.db = new sqlite3.Database(':memory:');
    }

    initDb() {
        this.db.serialize(() => {
            this.db.run("CREATE TABLE users ...");
            this.db.run("CREATE TABLE courses ...");
            // ... seed data ...
        });
    }

    setupRoutes(app) {
        app.post('/api/checkout', (req, res) => {
            // 50 lines of business logic + DB queries + payment processing
        });
        app.get('/api/admin/financial-report', (req, res) => {
            // 40 lines of nested callback hell
        });
        app.delete('/api/users/:id', (req, res) => {
            // Simple but mixed with everything else
        });
    }
}
```

**After (Node.js — separated layers):**

```javascript
// src/database.js
const sqlite3 = require('sqlite3').verbose();
let db;
function initDatabase() {
    db = new sqlite3.Database(':memory:');
    db.serialize(() => {
        db.run("CREATE TABLE users ...");
        db.run("CREATE TABLE courses ...");
    });
    return db;
}
function getDb() { return db; }
module.exports = { initDatabase, getDb };

// src/models/user.js
const { getDb } = require('../database');
const userModel = {
    findByEmail(email) {
        return new Promise((resolve, reject) => {
            getDb().get("SELECT * FROM users WHERE email = ?", [email], (err, row) => {
                err ? reject(err) : resolve(row);
            });
        });
    },
    create(name, email, pass) {
        return new Promise((resolve, reject) => {
            getDb().run("INSERT INTO users (name, email, pass) VALUES (?, ?, ?)",
                [name, email, pass], function(err) {
                    err ? reject(err) : resolve(this.lastID);
                });
        });
    }
};
module.exports = userModel;

// src/controllers/checkout_controller.js
const userModel = require('../models/user');
const courseModel = require('../models/course');
const enrollmentModel = require('../models/enrollment');
const paymentModel = require('../models/payment');
const { processPayment } = require('../services/payment_service');

async function checkout(userId, email, courseId, cardNumber) {
    const course = await courseModel.findById(courseId);
    if (!course) throw new Error("Curso não encontrado");

    let user = await userModel.findByEmail(email);
    if (!user) {
        const hash = await hashPassword("123456");
        const userId = await userModel.create(userId, email, hash);
        user = { id: userId };
    }

    const paymentStatus = processPayment(cardNumber);
    if (paymentStatus === "DENIED") throw new Error("Pagamento recusado");

    const enrollmentId = await enrollmentModel.create(user.id, courseId);
    await paymentModel.create(enrollmentId, course.price, paymentStatus);
    return { enrollment_id: enrollmentId };
}

// src/routes/index.js
const express = require('express');
const checkoutController = require('../controllers/checkout_controller');
const router = express.Router();

router.post('/api/checkout', async (req, res) => {
    try {
        const { usr, eml, c_id, card } = req.body;
        if (!usr || !eml || !c_id || !card) return res.status(400).json({ error: "Bad Request" });
        const result = await checkoutController.checkout(usr, eml, c_id, card);
        res.json(result);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

module.exports = router;

// src/app.js — composition root
const express = require('express');
const { initDatabase } = require('./database');
const routes = require('./routes');

const app = express();
app.use(express.json());
initDatabase();
app.use(routes);
app.listen(process.env.PORT || 3000);
```

---

## Pattern 4: Extract Controllers from Routes

**When to use:** Route handlers contain business logic, validation, and database queries.

**Before (Python/Flask):**
```python
# routes/task_routes.py
@task_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400

    title = data.get('title')
    if not title:
        return jsonify({'error': 'Título é obrigatório'}), 400
    if len(title) < 3:
        return jsonify({'error': 'Título muito curto'}), 400
    if len(title) > 200:
        return jsonify({'error': 'Título muito longo'}), 400

    status = data.get('status', 'pending')
    if status not in ['pending', 'in_progress', 'done', 'cancelled']:
        return jsonify({'error': 'Status inválido'}), 400

    # ... more validation ...
    # ... database operations ...
    # ... response formatting ...

    task = Task()
    task.title = title
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201
```

**After (Python/Flask):**
```python
# controllers/task_controller.py
from models.task import Task
from database import db

VALID_STATUSES = ['pending', 'in_progress', 'done', 'cancelled']

def create_task(data):
    title = data.get('title')
    if not title or len(title) < 3 or len(title) > 200:
        return None, "Título deve ter entre 3 e 200 caracteres"

    status = data.get('status', 'pending')
    if status not in VALID_STATUSES:
        return None, "Status inválido"

    task = Task()
    task.title = title
    task.description = data.get('description', '')
    task.status = status
    task.priority = data.get('priority', 3)
    task.user_id = data.get('user_id')
    task.category_id = data.get('category_id')

    db.session.add(task)
    db.session.commit()
    return task, None

# routes/task_routes.py
from flask import Blueprint, request, jsonify
from controllers import task_controller

task_bp = Blueprint('tasks', __name__)

@task_bp.route('/tasks', methods=['POST'])
def create_task_route():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400

    task, error = task_controller.create_task(data)
    if error:
        return jsonify({'error': error}), 400
    return jsonify(task.to_dict()), 201
```

---

## Pattern 5: Centralize Error Handling

**When to use:** Every route has its own try/except with inconsistent error responses.

**Before (Python/Flask):**
```python
@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        tasks = Task.query.all()
        return jsonify([t.to_dict() for t in tasks]), 200
    except:
        return jsonify({'error': 'Erro interno'}), 500

@task_bp.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    try:
        task = Task.query.get(id)
        if not task:
            return jsonify({'error': 'Task não encontrada'}), 404
        return jsonify(task.to_dict()), 200
    except:
        return jsonify({'error': 'Erro interno'}), 500
```

**After (Python/Flask):**
```python
# middlewares/error_handler.py
from flask import jsonify

class AppError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code

def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(error):
        return jsonify({"error": error.message}), error.status_code

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(Exception)
    def handle_generic(error):
        return jsonify({"error": "Internal server error"}), 500

# routes/task_routes.py
from flask import Blueprint, request, jsonify
from controllers import task_controller
from middlewares.error_handler import AppError

task_bp = Blueprint('tasks', __name__)

@task_bp.route('/tasks', methods=['GET'])
def get_tasks_route():
    tasks = task_controller.get_all_tasks()
    return jsonify([t.to_dict() for t in tasks]), 200

@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task_route(task_id):
    task = task_controller.get_task_by_id(task_id)
    if not task:
        raise AppError("Task não encontrada", 404)
    return jsonify(task.to_dict()), 200

# app.py
from middlewares.error_handler import register_error_handlers
register_error_handlers(app)
```

---

## Pattern 6: Replace Callbacks with Async/Await (Node.js)

**When to use:** Deeply nested callbacks (callback hell) in Node.js code.

**Before (Node.js):**
```javascript
app.get('/api/admin/financial-report', (req, res) => {
    let report = [];
    this.db.all("SELECT * FROM courses", [], (err, courses) => {
        if (err) return res.status(500).send("Erro DB");
        let coursesPending = courses.length;
        courses.forEach(c => {
            let courseData = { course: c.title, revenue: 0, students: [] };
            this.db.all("SELECT * FROM enrollments WHERE course_id = ?", [c.id], (err, enrollments) => {
                let enrPending = enrollments.length;
                enrollments.forEach(enr => {
                    this.db.get("SELECT name FROM users WHERE id = ?", [enr.user_id], (err, user) => {
                        this.db.get("SELECT amount FROM payments WHERE enrollment_id = ?", [enr.id], (err, payment) => {
                            // ... process ...
                            enrPending--;
                            if (enrPending === 0) {
                                report.push(courseData);
                                coursesPending--;
                                if (coursesPending === 0) res.json(report);
                            }
                        });
                    });
                });
            });
        });
    });
});
```

**After (Node.js):**
```javascript
// database.js — promisified helpers
function dbAll(sql, params = []) {
    return new Promise((resolve, reject) => {
        getDb().all(sql, params, (err, rows) => err ? reject(err) : resolve(rows));
    });
}
function dbGet(sql, params = []) {
    return new Promise((resolve, reject) => {
        getDb().get(sql, params, (err, row) => err ? reject(err) : resolve(row));
    });
}

// controllers/financial_controller.js
async function getFinancialReport() {
    const courses = await dbAll("SELECT * FROM courses");
    const report = [];

    for (const course of courses) {
        const courseData = { course: course.title, revenue: 0, students: [] };
        const enrollments = await dbAll("SELECT * FROM enrollments WHERE course_id = ?", [course.id]);

        for (const enr of enrollments) {
            const user = await dbGet("SELECT name FROM users WHERE id = ?", [enr.user_id]);
            const payment = await dbGet("SELECT amount, status FROM payments WHERE enrollment_id = ?", [enr.id]);

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

// routes/index.js
router.get('/api/admin/financial-report', async (req, res) => {
    try {
        const report = await financialController.getFinancialReport();
        res.json(report);
    } catch (err) {
        res.status(500).json({ error: "Erro ao gerar relatório" });
    }
});
```

---

## Pattern 7: Extract Services for Cross-Cutting Concerns

**When to use:** Business logic that doesn't belong to a specific model or controller is scattered across routes.

**Before (Python/Flask — notifications inline in controller):**
```python
def criar_pedido():
    # ... create order ...
    print("ENVIANDO EMAIL: Pedido " + str(resultado["pedido_id"]) + " criado para usuario " + str(usuario_id))
    print("ENVIANDO SMS: Seu pedido foi recebido!")
    print("ENVIANDO PUSH: Novo pedido recebido pelo sistema")
    return jsonify({"dados": resultado, "sucesso": True}), 201
```

**After (Python/Flask — notification service):**
```python
# services/notification_service.py
import os
import logging

logger = logging.getLogger(__name__)

def notify_order_created(order_id, user_id):
    """Send notification when an order is created."""
    logger.info(f"NOTIFICATION: Order {order_id} created for user {user_id}")
    # In production: send email, SMS, push notification via external services
    # For now, structured logging replaces print statements

def notify_order_status_changed(order_id, new_status):
    """Send notification when order status changes."""
    if new_status == "aprovado":
        logger.info(f"NOTIFICATION: Order {order_id} approved. Prepare shipment.")
    elif new_status == "cancelado":
        logger.info(f"NOTIFICATION: Order {order_id} cancelled. Restock inventory.")

# controllers/pedido_controller.py
from services.notification_service import notify_order_created

def criar_pedido(data):
    # ... create order logic ...
    notify_order_created(resultado["pedido_id"], usuario_id)
    return resultado
```

**Before (Node.js — payment processing inline in route):**
```javascript
app.post('/api/checkout', (req, res) => {
    // ... mixed DB, payment, and enrollment logic all in one route handler ...
    console.log(`Processando cartão ${cc} na chave ${config.paymentGatewayKey}`);
    let status = cc.startsWith("4") ? "PAID" : "DENIED";
    // ... more inline logic ...
});
```

**After (Node.js — payment service):**
```javascript
// services/payment_service.js
function processPayment(cardNumber) {
    // In production: call real payment gateway
    return cardNumber.startsWith("4") ? "PAID" : "DENIED";
}
module.exports = { processPayment };

// controllers/checkout_controller.js
const { processPayment } = require('../services/payment_service');

async function checkout(userId, email, courseId, cardNumber) {
    const status = processPayment(cardNumber);
    if (status === "DENIED") throw new Error("Pagamento recusado");
    // ... rest of checkout logic ...
}
```

---

## Pattern 8: Add Input Validation

**When to use:** Endpoints accept input without validating required fields, types, ranges, or formats.

**Before (Python/Flask — no validation):**
```python
@task_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task = Task()
    task.title = data['title']  # KeyError if missing
    task.priority = data['priority']  # No range check
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201
```

**After (Python/Flask — proper validation):**
```python
# controllers/task_controller.py
from models.task import Task
from database import db

VALID_STATUSES = ['pending', 'in_progress', 'done', 'cancelled']

def create_task(data):
    errors = []

    title = data.get('title')
    if not title:
        errors.append("Título é obrigatório")
    elif len(title) < 3 or len(title) > 200:
        errors.append("Título deve ter entre 3 e 200 caracteres")

    priority = data.get('priority', 3)
    if not isinstance(priority, int) or priority < 1 or priority > 5:
        errors.append("Prioridade deve ser entre 1 e 5")

    status = data.get('status', 'pending')
    if status not in VALID_STATUSES:
        errors.append(f"Status inválido. Válidos: {VALID_STATUSES}")

    if errors:
        return None, errors

    task = Task()
    task.title = title
    task.description = data.get('description', '')
    task.status = status
    task.priority = priority
    task.user_id = data.get('user_id')
    task.category_id = data.get('category_id')

    db.session.add(task)
    db.session.commit()
    return task, None
```

---

## Pattern 9: Fix Broken Cryptography

**When to use:** MD5, SHA1, or custom "encryption" used for password hashing.

**Before (Python):**
```python
import hashlib

class User(db.Model):
    def set_password(self, pwd):
        self.password = hashlib.md5(pwd.encode()).hexdigest()

    def check_password(self, pwd):
        return self.password == hashlib.md5(pwd.encode()).hexdigest()
```

**After (Python — using werkzeug):**
```python
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    def set_password(self, pwd):
        self.password = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.password, pwd)
```

**Before (Node.js):**
```javascript
function badCrypto(pwd) {
    let hash = "";
    for(let i = 0; i < 10000; i++) {
        hash += Buffer.from(pwd).toString('base64').substring(0, 2);
    }
    return hash.substring(0, 10);
}
```

**After (Node.js — using bcrypt):**
```javascript
const bcrypt = require('bcrypt');
const SALT_ROUNDS = 10;

async function hashPassword(pwd) {
    return bcrypt.hash(pwd, SALT_ROUNDS);
}

async function verifyPassword(pwd, hash) {
    return bcrypt.compare(pwd, hash);
}
```

**After (Python — using passlib as alternative):**
```python
from passlib.hash import bcrypt

class User(db.Model):
    def set_password(self, pwd):
        self.password = bcrypt.hash(pwd)

    def check_password(self, pwd):
        return bcrypt.verify(pwd, self.password)
```

---

## Pattern 10: Eliminate Duplicated Code

**When to use:** The same logic (validation, formatting, calculations) appears in multiple files.

**Before (Python — overdue check duplicated 3 times):**
```python
# In routes/task_routes.py
if t.due_date:
    if t.due_date < datetime.utcnow():
        if t.status != 'done' and t.status != 'cancelled':
            task_data['overdue'] = True
        else:
            task_data['overdue'] = False
    else:
        task_data['overdue'] = False
else:
    task_data['overdue'] = False

# In routes/report_routes.py (exact same logic)
if t.due_date:
    if t.due_date < datetime.utcnow():
        if t.status != 'done' and t.status != 'cancelled':
            overdue_count = overdue_count + 1

# In routes/user_routes.py (exact same logic)
if t.due_date:
    if t.due_date < datetime.utcnow():
        if t.status != 'done' and t.status != 'cancelled':
            task_data['overdue'] = True
```

**After (Python — single source of truth in model):**
```python
# models/task.py
class Task(db.Model):
    def is_overdue(self):
        if not self.due_date:
            return False
        if self.status in ('done', 'cancelled'):
            return False
        return self.due_date < datetime.utcnow()

    def to_dict(self):
        data = {
            'id': self.id,
            'title': self.title,
            # ... other fields ...
            'overdue': self.is_overdue()
        }
        return data

# In controllers — just call the model method
task_data = task.to_dict()  # overdue is included automatically

# In report controller
overdue_count = sum(1 for t in tasks if t.is_overdue())
```

**Before (Python — validation duplicated):**
```python
# In routes/task_routes.py
if len(title) < 3:
    return jsonify({'error': 'Título muito curto'}), 400
if len(title) > 200:
    return jsonify({'error': 'Título muito longo'}), 400
if status not in ['pending', 'in_progress', 'done', 'cancelled']:
    return jsonify({'error': 'Status inválido'}), 400

# In utils/helpers.py (same validation but never used!)
def process_task_data(data):
    if 'title' in data:
        title = data['title']
        if len(title) >= 3 and len(title) <= 200:
            result['title'] = title
```

**After (Python — validation in controller only):**
```python
# controllers/task_controller.py
from utils.helpers import VALID_STATUSES, MIN_TITLE_LENGTH, MAX_TITLE_LENGTH

def validate_task_data(data):
    errors = []
    title = data.get('title')
    if not title:
        errors.append("Título é obrigatório")
    elif len(title) < MIN_TITLE_LENGTH or len(title) > MAX_TITLE_LENGTH:
        errors.append(f"Título deve ter entre {MIN_TITLE_LENGTH} e {MAX_TITLE_LENGTH} caracteres")
    # ... other validations ...
    return errors
```

---

## Pattern Checklist

When refactoring, apply these patterns as needed:

- [ ] Pattern 1: Extract Configuration — all secrets to env vars
- [ ] Pattern 2: Parameterize SQL — no string concatenation in queries
- [ ] Pattern 3: Break God File — split into models/controllers/routes
- [ ] Pattern 4: Extract Controllers — business logic out of routes
- [ ] Pattern 5: Centralize Error Handling — middleware instead of try/except everywhere
- [ ] Pattern 6: Replace Callbacks — async/await for Node.js
- [ ] Pattern 7: Extract Services — cross-cutting concerns to service layer
- [ ] Pattern 8: Add Input Validation — validate all inputs
- [ ] Pattern 9: Fix Cryptography — proper password hashing
- [ ] Pattern 10: Eliminate Duplicates — single source of truth
