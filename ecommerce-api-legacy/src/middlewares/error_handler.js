function errorHandler(err, req, res, next) {
    if (err.statusCode) {
        return res.status(err.statusCode).json({ error: err.message });
    }
    console.error("Unhandled error:", err);
    res.status(500).json({ error: "Erro interno do servidor" });
}

module.exports = { errorHandler };
