import express from "express";
import { shareExistingPost, getUserSharedPosts } from "../controllers/shareController.js";
import { verifyToken } from "../middleware/authMiddleware.js"; // ADD THIS IMPORT

const router = express.Router();

// 📌 Share a post - ADD AUTHENTICATION
router.post("/share", verifyToken, shareExistingPost);

// 📌 Get shared posts of a specific user
router.get("/user/:user_id", getUserSharedPosts);

export default router;