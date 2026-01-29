const cors = require('cors');
const express = require('express');
const { calc } = require('./calculator');

const app = express();
app.use(cors()); // Allow CORS for all origins (⚠️ Testing only ⚠️)
app.use(express.json());

app.post('/calculate', (req, res) => {
    try {
        const { gen, attacker, defender } = req.body;
        const result = calc(attacker, defender, gen);
        res.json(result);
    } catch (err) {
        console.error(err);
        res.status(400).json({ error: err.message });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Calculator API running on port ${PORT}`));