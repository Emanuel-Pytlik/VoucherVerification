import express from 'express';
import axios from 'axios';
import cors from 'cors';

// Test
//const axios = require('axios');
const app = express();
const port = 3000;

// Configure CORS with specific allowed headers
app.use(cors({
    origin: 'http://localhost:8000',  // Allow only your frontend origin
    methods: ['GET', 'POST'],  // Specify allowed methods if necessary
    allowedHeaders: ['x-printed-credit-key', 'x-verification-code', 'Content-Type', 'Authorization']  // Add your custom header here
}));

app.get('/api/voucher', async (req, res) => {
    try {
        const response = await axios.get('https://dmpay-gateway.services.dmtech.com/checker/DE/credits', {
            headers: {
                'x-printed-credit-key': req.headers['x-printed-credit-key'],
                'x-verification-code': req.headers['x-verification-code']
            }
        });
        res.json(response.data);
    } catch (error) {
        res.status(error.response?.status || 500).send(error.message);
    }
});

app.listen(port, () => {
    console.log(`Proxy server running on http://localhost:${port}`);
});