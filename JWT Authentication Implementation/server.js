require('dotenv').config();
const express = require('express');
const authRoutes = require('./routes/auth');
const protectedRoutes = require('./routes/protected');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());

// Routes
app.use('/api/auth', authRoutes);
app.use('/api', protectedRoutes);

// Health check
app.get('/', (req, res) => {
    res.json({ message: 'JWT Authentication API is running' });
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
