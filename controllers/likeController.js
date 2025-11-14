import db from "../config/db.js";

// ❤️ Like a post - FIXED VERSION
export const likePost = async (req, res) => {
  try {
    const { post_id } = req.body;
    const user_id = req.user.id; // Get user_id from authenticated token

    if (!post_id) return res.status(400).json({ error: "Post ID required" });

    db.query(
      "SELECT 1 FROM likes WHERE post_id = ? AND user_id = ? LIMIT 1",
      [post_id, user_id],
      (err, rows) => {
        if (err) return res.status(500).json({ error: "Database error" });
        if (rows.length) return res.status(400).json({ message: "Already liked this post" });

        db.query(
          "INSERT INTO likes (post_id, user_id) VALUES (?, ?)",
          [post_id, user_id],
          (err2) => {
            if (err2) return res.status(500).json({ error: "Failed to like post" });
            res.status(201).json({ message: "Post liked successfully" });
          }
        );
      }
    );
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Failed to like post" });
  }
};

// 💔 Unlike a post - FIXED VERSION
export const unlikePost = async (req, res) => {
  try {
    const { post_id } = req.body;
    const user_id = req.user.id; // Get user_id from authenticated token

    db.query(
      "DELETE FROM likes WHERE post_id = ? AND user_id = ?",
      [post_id, user_id],
      (err, result) => {
        if (err) return res.status(500).json({ error: "Failed to unlike post" });
        if (result.affectedRows === 0) return res.status(404).json({ message: "Like not found" });
        res.json({ message: "Post unliked successfully" });
      }
    );
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Failed to unlike post" });
  }
};

// 📊 Get like count
export const getLikeCount = async (req, res) => {
  try {
    const { post_id } = req.params;
    db.query(
      "SELECT COUNT(*) AS like_count FROM likes WHERE post_id = ?",
      [post_id],
      (err, rows) => {
        if (err) return res.status(500).json({ error: "Failed to get like count" });
        res.json({ post_id, like_count: rows[0]?.like_count || 0 });
      }
    );
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Failed to get like count" });
  }
};