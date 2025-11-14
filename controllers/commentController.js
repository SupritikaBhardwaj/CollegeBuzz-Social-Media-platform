import { addComment, getCommentsForPost } from "../models/comment.js";
import db from "../config/db.js";

// ✅ Add a comment to a post - FIXED VERSION
export const addNewComment = async (req, res) => {
  try {
    const { post_id, comment_text } = req.body;
    const user_id = req.user.id; // Get user_id from authenticated token

    if (!post_id || !comment_text) {
      return res.status(400).json({ message: "Post ID and comment text are required" });
    }

    const commentId = await addComment(user_id, post_id, comment_text);
    res.status(201).json({ message: "Comment added successfully", comment_id: commentId });
  } catch (err) {
    console.error("Error adding comment:", err);
    res.status(500).json({ error: "Internal Server Error" });
  }
};

// ✅ Get all comments for a post
export const getComments = async (req, res) => {
  try {
    const { post_id } = req.params;
    const comments = await getCommentsForPost(post_id);
    res.status(200).json(comments);
  } catch (err) {
    console.error("Error fetching comments:", err);
    res.status(500).json({ error: "Internal Server Error" });
  }
};

// ✅ Get all comments across all posts
export const getAllComments = (req, res) => {
  const sql = `
    SELECT c.comment_id, c.comment_text, c.commented_at AS created_at, c.post_id, u.name AS username
    FROM comments c
    JOIN users u ON c.user_id = u.user_id
    ORDER BY c.commented_at DESC`;
  db.query(sql, (err, rows) => {
    if (err) {
      console.error("Error fetching all comments:", err);
      return res.status(500).json({ error: "Internal Server Error" });
    }
    res.json(rows);
  });
};