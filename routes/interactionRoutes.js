import express from "express";
import { likePost, addComment, getComments, sharePost } from "../controllers/interactionController.js";
import { verifyToken } from "../middleware/authMiddleware.js"; // ADD THIS IMPORT

const router = express.Router();

// Likes - ADD AUTHENTICATION
router.post("/like", verifyToken, likePost);

// Comments - ADD AUTHENTICATION
router.post("/comment", verifyToken, addComment);
router.get("/comments/:post_id", getComments);

// Shares - ADD AUTHENTICATION
router.post("/share", verifyToken, sharePost);

export default router;