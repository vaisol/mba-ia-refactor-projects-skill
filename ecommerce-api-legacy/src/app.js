const express = require('express');
const config = require('./config');
const { initDb } = require('./AppManager');
const routes = require('./routes');

const app = express();
app.use(express.json());

app.use('/api', routes);

initDb().then(() => {
    app.listen(config.port, () => {
        console.log(`E-commerce API refatorada rodando na porta ${config.port}...`);
    });
});
