const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
    res.json({ mensagem: 'E-commerce API refatorada', versao: '1.0.0' });
});

router.get('/health', (req, res) => {
    res.json({ status: 'ok' });
});

module.exports = router;
