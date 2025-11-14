import bcrypt from "bcryptjs";
import jwt from "jsonwebtoken";
import db from "../config/db.js";
import dotenv from "dotenv";
dotenv.config();

// Register New User
export const registerUser = (req, res) => {
  const { name, email, password } = req.body;

  // Check if user already exists
  db.query("SELECT * FROM users WHERE email = ?", [email], async (err, result) => {
    if (err) return res.status(500).json({ message: "Database error" });
    if (result.length > 0) return res.status(400).json({ message: "User already exists" });

    // Hash password
    const hashed = await bcrypt.hash(password, 10);

    // Insert user
    db.query("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", [name, email, hashed], (err2, result) => {
      if (err2) return res.status(500).json({ message: "Error creating user" });
      res.status(201).json({ message: "User registered successfully", user_id: result.insertId });
    });
  });
};

// Login User - FIXED to return user_id
export const loginUser = (req, res) => {
  const { email, password } = req.body;

  db.query("SELECT * FROM users WHERE email = ?", [email], async (err, result) => {
    if (err) return res.status(500).json({ message: "Database error" });
    if (result.length === 0) return res.status(404).json({ message: "User not found" });

    const user = result[0];
    const valid = await bcrypt.compare(password, user.password);
    if (!valid) return res.status(401).json({ message: "Invalid credentials" });

    // Generate JWT token with user_id
    const token = jwt.sign({ id: user.user_id, email: user.email }, process.env.JWT_SECRET, { expiresIn: "1d" });

    res.json({ 
      message: "Login successful", 
      token,
      user: {
        user_id: user.user_id,
        name: user.name,
        email: user.email
      }
    });
  });
};