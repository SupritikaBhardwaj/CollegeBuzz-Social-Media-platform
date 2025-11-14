import db from "../config/db.js";


const Comment = {
  create: (postId, userId, content, callback) => {
    const sql = 'INSERT INTO comments (post_id, user_id, content) VALUES (?, ?, ?)';
    db.query(sql, [postId, userId, content], callback);
  }
};

export default Comment;

export const addComment = (user_id, post_id, comment_text) => {
  return new Promise((resolve, reject) => {
    const sql = 'INSERT INTO comments (user_id, post_id, comment_text) VALUES (?, ?, ?)';
    db.query(sql, [user_id, post_id, comment_text], (err, result) => {
      if (err) return reject(err);
      resolve(result.insertId);
    });
  });
};

export const getCommentsForPost = (post_id) => {
  return new Promise((resolve, reject) => {
    const sql = `
      SELECT c.comment_id, c.comment_text, c.commented_at AS created_at, u.name AS username
      FROM comments c
      JOIN users u ON c.user_id = u.user_id
      WHERE c.post_id = ?
      ORDER BY c.commented_at DESC`;
    db.query(sql, [post_id], (err, rows) => {
      if (err) return reject(err);
      resolve(rows);
    });
  });
};