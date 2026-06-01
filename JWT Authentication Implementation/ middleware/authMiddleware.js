const jwt = require('jsonwebtoken');

/**
 * Middleware to verify JWT token
 * Extracts token from Authorization header and validates it
 */
const verifyToken = (req, res, next) => {
    // TODO: Get token from Authorization header (format: "Bearer TOKEN")
    // TODO: Check if token exists, if not return 403 error
    // TODO: Verify token using jwt.verify() with JWT_SECRET
    // TODO: If verification fails, return 401 error
    // TODO: If successful, attach decoded user data to req.user
    // TODO: Call next() to proceed to the route handler
};

module.exports = verifyToken;
