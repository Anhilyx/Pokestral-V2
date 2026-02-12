import cors from 'cors';
import express from 'express';
import { calculateDamage_knownAttacker, calculateDamage_knownDefender, calculateDamage_knownBoth, calculateDamage_knownNone } from './tools/damage-calculator.js';
import { getDefinition } from './tools/dictionnary.js';

const app = express();
app.use(cors());  // Allow CORS for all origins (⚠️ Testing only ⚠️)
app.use(express.json());

const apiRouter = express.Router();

/********************
| Damage Calculator |
********************/

// Damage calculator for known attacker set and unknown defender set
apiRouter.post('/damage-calculator/known-attacker', (req, res) => {
    try {
        const { attacker, defender, gen } = req.body;
        const result = calculateDamage_knownAttacker(attacker, defender, gen);
        res.json(result);
    } catch (err) {
        console.error(err);
        res.status(400).json({ error: err.message });
    }
});

// Damage calculator for unknown attacker set and known defender set
apiRouter.post('/damage-calculator/known-defender', (req, res) => {
    try {
        const { attacker, defender, moves, gen } = req.body;
        const result = calculateDamage_knownDefender(attacker, defender, moves, gen);
        res.json(result);
    } catch (err) {
        console.error(err);
        res.status(400).json({ error: err.message });
    }
});

// Damage calculator for known attacker set and known defender set
apiRouter.post('/damage-calculator/known-both', (req, res) => {
    try {
        const {  attacker, defender, gen } = req.body;
        const result = calculateDamage_knownBoth(attacker, defender, gen);
        res.json(result);
    } catch (err) {
        console.error(err);
        res.status(400).json({ error: err.message });
    }
});

// Damage calculator for unknown attacker set and unknown defender set
apiRouter.post('/damage-calculator/known-none', (req, res) => {
    try {
        const { attacker, defender, moves, gen } = req.body;
        const result = calculateDamage_knownNone(attacker, defender, moves, gen);
        res.json(result);
    } catch (err) {
        console.error(err);
        res.status(400).json({ error: err.message });
    }
});

/**************
| Dictionnary |
**************/

// Dictionnary endpoint to get the definition of a move/ability by its name and, optionally, its category
apiRouter.post('/dictionnary', async (req, res) => {
    try {
        const { name, category } = req.body;
        const result = await getDefinition(name, category);
        res.json(result);
    } catch (err) {
        console.error(err);
        res.status(400).json({ error: err.message });
    }
});

app.use('/api/tools', apiRouter);

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => console.log(`Calculator API running on port ${PORT}`));