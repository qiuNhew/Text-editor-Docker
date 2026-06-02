'use strict';

const express = require('express');
const cors = require('cors');

const PORT = process.env.PORT || 80;
const HOST = '0.0.0.0';

const charcount = require('./charcount');

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Request logging middleware
app.use((req, res, next) => {
    console.log(`${new Date().toISOString()} - ${req.method} ${req.url}`);
    next();
});

app.get('/', (req, res) => {
    const output = {
        error: false,
        string: '',
        answer: 0,
        message: ''
    };

    try {
        const text = req.query.text;
        
        // Validate input
        const validation = charcount.validate(text);
        if (!validation.valid) {
            throw new Error(validation.message);
        }

        // Get character count
        const answer = charcount.counter(text);
        
        output.string = `Contains ${answer} characters`;
        output.answer = answer;
        
        res.json(output);
    } catch (error) {
        console.error(`Error processing request: ${error.message}`);
        
        output.error = true;
        output.message = error.message;
        
        res.status(400).json(output);
    }
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(`Unhandled error: ${err.message}`);
    
    res.status(500).json({
        error: true,
        string: '',
        answer: 0,
        message: 'Internal server error'
    });
});

const server = app.listen(PORT, HOST, () => {
    console.log(`Server running on http://${HOST}:${PORT}`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
    server.close(() => {
        console.log('Server shutdown complete');
    });
});

module.exports = { app, server };