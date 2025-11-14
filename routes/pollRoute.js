import express from "express";
import { createPollController, getPollForPost, voteOnPoll, getResults } from "../controllers/pollController.js";
import { verifyToken } from "../middleware/authMiddleware.js"; // ADD THIS IMPORT

const router = express.Router();

// Create a poll for a post
router.post("/create", createPollController);

// Get poll for a post
router.get("/post/:post_id", getPollForPost);

// Vote on a poll - ADD AUTHENTICATION
router.post("/vote", verifyToken, voteOnPoll);

// Get poll results
router.get("/results/:poll_id", getResults);

export default router;