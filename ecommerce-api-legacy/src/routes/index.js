const { checkout, deleteUser, AppError } = require('../controllers/checkout_controller');
const financialController = require('../controllers/financial_controller');

function registerRoutes(app) {
    app.post('/api/checkout', async (req, res) => {
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
            res.status(500).json({ error: "Erro interno do servidor" });
        }
    });

    app.get('/api/admin/financial-report', async (req, res) => {
        try {
            const report = await financialController.getFinancialReport();
            res.json(report);
        } catch (err) {
            res.status(500).json({ error: "Erro ao gerar relatório financeiro" });
        }
    });

    app.delete('/api/users/:id', async (req, res) => {
        try {
            const userId = parseInt(req.params.id, 10);
            const result = await deleteUser(userId);
            res.json(result);
        } catch (err) {
            res.status(500).json({ error: "Erro ao deletar usuário" });
        }
    });
}

module.exports = { registerRoutes };
