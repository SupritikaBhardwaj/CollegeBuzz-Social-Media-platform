import express from "express";
import { 
  createNewPost, 
  fetchAllPosts, 
  fetchPostById, 
  deleteUserPost,
  getUserPosts 
} from "../controllers/postController.js";
import { verifyToken } from "../middleware/authMiddleware.js";

const router = express.Router();

// 📌 Create a new post
router.post("/create", verifyToken, createNewPost);

// 📌 Get all posts (feed)
router.get("/all", fetchAllPosts);

// 📌 Get user's posts
router.get("/user/:user_id", getUserPosts);

// 📌 Get post by ID
router.get("/:post_id", fetchPostById);

// 📌 NEW: Delete a post
router.delete("/:post_id", verifyToken, deleteUserPost);

export default router;