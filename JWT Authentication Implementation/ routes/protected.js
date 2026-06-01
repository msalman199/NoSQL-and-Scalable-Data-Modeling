const express = require('express');
const router = express.Router();
const verifyToken = require('../middleware/authMiddleware');

// Public route (no authentication required)
router.get('/public', (req, res) => {
    res.json({ message: 'This is a public endpoint' });
});

// Protected route (authentication required)
router.get('/dashboard', verifyToken, (req, res) => {
    // TODO: Access user information from req.user
    // TODO: Return personalized dashboard data
    // Example: res.json({ message: `Welcome ${req.user.userId}`, data: {...} })
});

// Protected route with user profile
router.get('/profile', verifyToken, (req, res) => {
    // TODO: Return user profile information
    // TODO: Use req.user to get authenticated user details
});

module.exports = router;
