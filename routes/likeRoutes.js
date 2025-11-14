import express from "express";
import { likePost, unlikePost, getLikeCount } from "../controllers/likeController.js";
import { verifyToken } from "../middleware/authMiddleware.js"; // ADD THIS IMPORT

const router = express.Router();

router.post("/add", verifyToken, likePost);
router.post("/remove", verifyToken, unlikePost);
router.get("/:post_id", getLikeCount);

export default router;