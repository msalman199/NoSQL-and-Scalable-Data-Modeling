# 🔐 JWT Authentication Implementation (Node.js + Express)

<p align="center">
  <img src="https://img.shields.io/badge/Auth-JWT_Authentication-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Node.js-Backend-green?style=for-the-badge&logo=node.js" />
  <img src="https://img.shields.io/badge/Express-API_Framework-black?style=for-the-badge&logo=express" />
  <img src="https://img.shields.io/badge/Bcrypt-Password_Security-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Linux-Ubuntu-orange?style=for-the-badge&logo=ubuntu" />
</p>

---

# 📖 Overview

In this lab, you will implement **JWT (JSON Web Token) authentication** using **Node.js and Express.js**. You will build secure login/register endpoints, protect routes using middleware, and validate tokens for API security.

---

# 🎯 Learning Objectives

By the end of this lab, you will be able to:

✅ Understand JWT structure and workflow  
✅ Generate authentication tokens  
✅ Protect API routes using middleware  
✅ Validate and decode JWT tokens  
✅ Handle authentication errors and expiration  

---

# 📋 Prerequisites

Before starting, you should have:

- Basic REST API knowledge
- Node.js & Express.js understanding
- JavaScript ES6+ familiarity
- Linux command line basics
- Understanding of authentication concepts

---

# 🛠️ Environment Setup

## 🔹 Update System

```bash
sudo apt update
```

---

## 🔹 Install Node.js

```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
node --version
npm --version
```

---

## 🔹 Create Project

```bash
mkdir ~/jwt-auth-lab
cd ~/jwt-auth-lab
npm init -y
```

---

## 🔹 Install Dependencies

```bash
npm install express jsonwebtoken bcryptjs dotenv
npm install --save-dev nodemon
```

---

## 🔹 Create Project Structure

```bash
mkdir routes middleware
touch server.js .env
touch routes/auth.js routes/protected.js middleware/authMiddleware.js
```

---

# 🔐 Task 1: JWT Token Generation

## ⚙️ Step 1: Environment Variables

```bash
nano .env
```

```env
PORT=3000
JWT_SECRET=your_super_secret_key_change_this_in_production
JWT_EXPIRES_IN=1h
```

---

## 👤 Step 2: Authentication Routes

```bash
nano routes/auth.js
```

### ✨ Code

```javascript
const express = require('express');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const router = express.Router();

const users = [];

// REGISTER
router.post('/register', async (req, res) => {
    try {
        const { username, password } = req.body;

        const existingUser = users.find(u => u.username === username);
        if (existingUser) {
            return res.status(400).json({ message: "User already exists" });
        }

        const hashedPassword = await bcrypt.hash(password, 10);

        users.push({
            username,
            password: hashedPassword
        });

        res.json({ message: "User registered successfully" });

    } catch (error) {
        res.status(500).json({ message: "Server error" });
    }
});

// LOGIN
router.post('/login', async (req, res) => {
    try {
        const { username, password } = req.body;

        const user = users.find(u => u.username === username);
        if (!user) {
            return res.status(401).json({ message: "Invalid credentials" });
        }

        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) {
            return res.status(401).json({ message: "Invalid credentials" });
        }

        const token = jwt.sign(
            { userId: user.username },
            process.env.JWT_SECRET,
            { expiresIn: process.env.JWT_EXPIRES_IN }
        );

        res.json({ token });

    } catch (error) {
        res.status(500).json({ message: "Server error" });
    }
});

module.exports = router;
```

---

# 🛡️ Task 2: JWT Middleware (Route Protection)

## 🔐 Step 1: Create Middleware

```bash
nano middleware/authMiddleware.js
```

### ✨ Code

```javascript
const jwt = require('jsonwebtoken');

const verifyToken = (req, res, next) => {
    const authHeader = req.headers['authorization'];

    if (!authHeader) {
        return res.status(403).json({ message: "No token provided" });
    }

    const token = authHeader.split(' ')[1];

    if (!token) {
        return res.status(403).json({ message: "Invalid token format" });
    }

    try {
        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        req.user = decoded;
        next();
    } catch (error) {
        return res.status(401).json({ message: "Unauthorized" });
    }
};

module.exports = verifyToken;
```

---

# 🌐 Task 3: Protected Routes

```bash
nano routes/protected.js
```

### ✨ Code

```javascript
const express = require('express');
const router = express.Router();
const verifyToken = require('../middleware/authMiddleware');

router.get('/public', (req, res) => {
    res.json({ message: "Public endpoint accessible" });
});

router.get('/dashboard', verifyToken, (req, res) => {
    res.json({
        message: `Welcome ${req.user.userId}`,
        data: "Secure dashboard data"
    });
});

router.get('/profile', verifyToken, (req, res) => {
    res.json({
        user: req.user.userId,
        role: "user"
    });
});

module.exports = router;
```

---

# 🚀 Task 4: Main Server Setup

```bash
nano server.js
```

### ✨ Code

```javascript
require('dotenv').config();
const express = require('express');

const authRoutes = require('./routes/auth');
const protectedRoutes = require('./routes/protected');

const app = express();

app.use(express.json());

app.use('/api/auth', authRoutes);
app.use('/api', protectedRoutes);

app.get('/', (req, res) => {
    res.json({ message: "JWT Auth API Running" });
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
```

---

# ▶️ Run Server

```bash
npx nodemon server.js
```

---

# 🧪 API Testing

## 🔹 Register User

```bash
curl -X POST http://localhost:3000/api/auth/register \
-H "Content-Type: application/json" \
-d '{"username":"alice","password":"123456"}'
```

---

## 🔹 Login User (Get Token)

```bash
curl -X POST http://localhost:3000/api/auth/login \
-H "Content-Type: application/json" \
-d '{"username":"alice","password":"123456"}'
```

---

## 🔹 Public Route

```bash
curl http://localhost:3000/api/public
```

---

## 🔹 Protected Route (No Token)

```bash
curl http://localhost:3000/api/dashboard
```

---

## 🔹 Protected Route (With Token)

```bash
curl http://localhost:3000/api/dashboard \
-H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

# 🧪 Expected Outputs

| Test | Result |
|------|--------|
| Register | User created |
| Login | JWT token returned |
| Public route | Works without auth |
| Protected route (no token) | 403 error |
| Protected route (valid token) | Success response |
| Invalid token | 401 error |

---

# 🛠️ Troubleshooting

### ❌ Module Not Found
```bash
npm install
```

### ❌ Invalid Token
Check:
- JWT_SECRET match
- Bearer format

### ❌ Port Busy
```bash
lsof -i :3000
kill -9 <PID>
```

---

# 📌 Key Concepts Learned

### 🔐 JWT Workflow
- User login → Token generated
- Token sent in headers
- Middleware validates token

### 🧠 Security Practices
- Password hashing (bcrypt)
- Secret stored in `.env`
- Stateless authentication

---

# 🏁 Conclusion

You have successfully built:

✅ JWT authentication system  
✅ Secure login/register API  
✅ Protected routes using middleware  
✅ Token validation system  
✅ Real-world authentication flow  

---

# 🚀 Next Steps

- Add Refresh Tokens
- Use MongoDB/PostgreSQL database
- Implement Role-Based Access Control (RBAC)
- Add Logout with token blacklist
- Add Swagger API documentation
- Deploy using Docker + Cloud

---

## 🎉 Lab Completed Successfully
**JWT Authentication Implementation with Node.js & Express** 🔐
