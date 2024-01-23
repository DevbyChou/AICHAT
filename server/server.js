const express = require('express');
const axios = require('axios');
const bodyParser = require('body-parser');
const swaggerUi = require('swagger-ui-express');
const swaggerJsdoc = require('swagger-jsdoc');

const app = express();
const port = 3000;

// Swagger definition
const swaggerOptions = {
    swaggerDefinition: {
        openapi: '3.0.0',
        info: {
            title: 'Machine Learning Model API',
            version: '1.0.0',
            description: 'API for interacting with a machine learning model',
        },
        servers: [{ url: `http://localhost:${port}` }],
    },
    apis: ['server.js'], 
};

// Initialize swagger-jsdoc
const swaggerDocs = swaggerJsdoc(swaggerOptions);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocs));

// For parsing application/json
app.use(bodyParser.json());

/**
 * @swagger
 * /generate-text:
 *   post:
 *     summary: Generate text using GPT-2 model
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               text:
 *                 type: string
 *     responses:
 *       200:
 *         description: Generated text
 *       500:
 *         description: Error message
 */
app.post('/generate-text', async (req, res) => {
    try {
        const inputText = req.body.text;
        const response = await axios.post('http://localhost:5000/generate', { text: inputText });
        res.json(response.data);
    } catch (error) {
        console.error('Error generating text:', error);
        res.status(500).send('Error generating text');
    }
});

/**
 * @swagger
 * /predict:
 *   post:
 *     summary: Make a prediction using the machine learning model
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               features:
 *                 type: array
 *                 items:
 *                   type: number
 *     responses:
 *       200:
 *         description: Prediction result
 *       500:
 *         description: Error message
 */
app.post('/predict', async (req, res) => {
    try {
        const features = req.body.features;
        const response = await axios.post('http://localhost:5000/predict', { features: features });
        res.json(response.data);
    } catch (error) {
        console.error('Error making prediction:', error);
        res.status(500).send('Error making prediction');
    }
});

app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
    console.log(`Swagger UI available on http://localhost:${port}/api-docs`);
});
