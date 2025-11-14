import express from "express";
import { addNewComment, getComments, getAllComments } from "../controllers/commentController.js";
import { verifyToken } from "../middleware/authMiddleware.js"; // ADD THIS IMPORT

const router = express.Router();

// 📌 Add a comment to a post - ADD AUTHENTICATION
router.post("/add", verifyToken, addNewComment);

// 📌 Get all comments for a post
router.get("/post/:post_id", getComments);

// 📌 Get all comments
router.get("/all", getAllComments);

export default router;