import cors from 'cors';
import express from 'express';
import { calculateDamage } from './tools/damage-calculator.js';

const app = express();
app.use(cors());  // Allow CORS for all origins (⚠️ Testing only ⚠️)
app.use(express.json());

const apiRouter = express.Router();

apiRouter.post('/damage-calculator', (req, res) => {
    try {
        const { gen, attacker, defender } = req.body;
        const result = calculateDamage(attacker, defender, gen);
        res.json(result);
    } catch (err) {
        console.error(err);
        res.status(400).json({ error: err.message });
    }
});

app.use('/api/tools', apiRouter);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Calculator API running on port ${PORT}`));