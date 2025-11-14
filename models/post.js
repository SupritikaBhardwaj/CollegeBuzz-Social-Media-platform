import db from "../config/db.js";

export const createPost = (user_id, content, image_url = null, post_type = "text") => {
  return new Promise((resolve, reject) => {
    const sql = "INSERT INTO posts (user_id, content, image_url, post_type) VALUES (?, ?, ?, ?)";
    db.query(sql, [user_id, content, image_url, post_type], (err, result) => {
      if (err) return reject(err);
      resolve(result.insertId);
    });
  });
};

export const getAllPosts = () => {
  return new Promise((resolve, reject) => {
    const sql = `
      SELECT p.*, u.name AS username
      FROM posts p
      JOIN users u ON p.user_id = u.user_id
      ORDER BY p.created_at DESC
    `;
    db.query(sql, (err, results) => {
      if (err) return reject(err);
      resolve(results);
    });
  });
};

export const getPostById = (post_id) => {
  return new Promise((resolve, reject) => {
    const sql = `
      SELECT p.*, u.name AS username 
      FROM posts p 
      JOIN users u ON p.user_id = u.user_id 
      WHERE p.post_id = ?`;
    db.query(sql, [post_id], (err, results) => {
      if (err) return reject(err);
      resolve(results[0]);
    });
  });
};

// ✅ NEW: Delete a post
export const deletePost = (post_id, user_id) => {
  return new Promise((resolve, reject) => {
    const sql = "DELETE FROM posts WHERE post_id = ? AND user_id = ?";
    db.query(sql, [post_id, user_id], (err, result) => {
      if (err) return reject(err);
      resolve(result.affectedRows > 0);
    });
  });
};

// ✅ NEW: Get post owner
export const getPostOwner = (post_id) => {
  return new Promise((resolve, reject) => {
    const sql = "SELECT user_id FROM posts WHERE post_id = ?";
    db.query(sql, [post_id], (err, results) => {
      if (err) return reject(err);
      resolve(results[0]?.user_id || null);
    });
  });
};