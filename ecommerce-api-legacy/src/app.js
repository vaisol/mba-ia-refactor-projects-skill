const express = require('express');
const { config } = require('./config/settings');
const { initDatabase } = require('./database');
const { registerRoutes } = require('./routes');
const { errorHandler } = require('./middlewares/error_handler');

const app = express();
app.use(express.json());

initDatabase();
registerRoutes(app);
app.use(errorHandler);

app.listen(config.port, () => {
    console.log(`LMS API rodando na porta ${config.port}...`);
});
