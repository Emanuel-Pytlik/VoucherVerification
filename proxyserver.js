import express from 'express';
import axios from 'axios';

// Test
//const axios = require('axios');
const app = express();
const port = 3000;

app.get('/api/voucher', async (req, res) => {
    try {
        console.log("Req0", req.headers)
        console.log("Req0", req.headers['x-verification-code'])
        // console.log("Req1", req.headers('x-verification-code'))
        //console.log("req", req)
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