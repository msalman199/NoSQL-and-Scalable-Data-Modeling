const express = require('express');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const router = express.Router();

// Mock user database (in production, use a real database)
const users = [];

// Register endpoint
router.post('/register', async (req, res) => {
    try {
        const { username, password } = req.body;
        
        // TODO: Check if user already exists
        // TODO: Hash the password using bcrypt (salt rounds: 10)
        // TODO: Store user in the users array
        // TODO: Return success message
        
    } catch (error) {
        res.status(500).json({ message: 'Server error' });
    }
});

// Login endpoint
router.post('/login', async (req, res) => {
    try {
        const { username, password } = req.body;
        
        // TODO: Find user in the users array
        // TODO: If user not found, return 401 error
        // TODO: Compare password with hashed password using bcrypt
        // TODO: If password invalid, return 401 error
        // TODO: Generate JWT token with payload: { userId: user.username }
        // TODO: Use JWT_SECRET and JWT_EXPIRES_IN from environment variables
        // TODO: Return token in response
        
    } catch (error) {
        res.status(500).json({ message: 'Server error' });
    }
});

module.exports = router;
