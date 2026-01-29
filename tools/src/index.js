const cors = require('cors');
const express = require('express');
const { calculateDamage } = require('./tools/damage-calculator');

const app = express();
app.use(cors()); // Allow CORS for all origins (⚠️ Testing only ⚠️)
app.use(express.json());

app.post('/damage-calculator', (req, res) => {
    try {
        const { gen, attacker, defender } = req.body;
        const result = calculateDamage(attacker, defender, gen);
        res.json(result);
    } catch (err) {
        console.error(err);
        res.status(400).json({ error: err.message });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Calculator API running on port ${PORT}`));