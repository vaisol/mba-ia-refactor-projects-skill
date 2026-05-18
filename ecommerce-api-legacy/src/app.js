const express = require('express');
const config = require('./src/config');
const { initDb } = require('./src/config/database');
const routes = require('./src/routes');

const app = express();
app.use(express.json());

app.use('/api', routes);

initDb().then(() => {
    app.listen(config.port, () => {
        console.log(`E-commerce API refatorada rodando na porta ${config.port}...`);
    });
});
