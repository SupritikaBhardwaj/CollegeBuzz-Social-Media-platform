import db from "../config/db.js";

const queryAsync = (sql, params = []) =>
  new Promise((resolve, reject) => {
    db.query(sql, params, (err, results) => {
      if (err) return reject(err);
      resolve(results);
    });
  });

// 🔹 LIKE a post - FIXED VERSION
export const likePost = async (req, res) => {
  const { post_id } = req.body;
  const user_id = req.user.id; // Get user_id from authenticated token

  try {
    const existing = await queryAsync(
      "SELECT * FROM likes WHERE post_id = ? AND user_id = ?",
      [post_id, user_id]
    );

    if (existing.length > 0) {
      await queryAsync("DELETE FROM likes WHERE post_id = ? AND user_id = ?", [
        post_id,
        user_id,
      ]);
      return res.json({ message: "Post unliked" });
    }

    await queryAsync("INSERT INTO likes (post_id, user_id) VALUES (?, ?)", [
      post_id,
      user_id,
    ]);
    res.json({ message: "Post liked" });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Error liking post" });
  }
};

// 🔹 COMMENT on a post - FIXED VERSION
export const addComment = async (req, res) => {
  const { post_id, comment_text } = req.body;
  const user_id = req.user.id; // Get user_id from authenticated token

  try {
    await queryAsync(
      "INSERT INTO comments (post_id, user_id, comment_text) VALUES (?, ?, ?)",
      [post_id, user_id, comment_text]
    );
    res.json({ message: "Comment added successfully" });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Error adding comment" });
  }
};

// 🔹 FETCH comments for a post
export const getComments = async (req, res) => {
  const { post_id } = req.params;

  try {
    const comments = await queryAsync(
      `SELECT c.comment_id, c.comment_text, c.commented_at AS created_at, u.name AS username
       FROM comments c JOIN users u ON c.user_id = u.user_id
       WHERE c.post_id = ?
       ORDER BY c.commented_at DESC`,
      [post_id]
    );
    res.json(comments);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Error fetching comments" });
  }
};

// 🔹 SHARE a post - FIXED VERSION
export const sharePost = async (req, res) => {
  const { post_id } = req.body;
  const user_id = req.user.id; // Get user_id from authenticated token

  try {
    await queryAsync("INSERT INTO shares (post_id, user_id) VALUES (?, ?)", [
      post_id,
      user_id,
    ]);
    res.json({ message: "Post shared successfully" });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Error sharing post" });
  }
};