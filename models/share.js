import db from "../config/db.js";



export const sharePost = (user_id, post_id) => {
  return new Promise((resolve, reject) => {
    const sql = "INSERT INTO shares (user_id, post_id) VALUES (?, ?)";
    db.query(sql, [user_id, post_id], (err, result) => {
      if (err) return reject(err);
      resolve(result.insertId);
    });
  });
};

export const getSharedPosts = (user_id) => {
  return new Promise((resolve, reject) => {
    const sql = `
      SELECT s.*, p.content, p.image_url, u.name AS post_owner
      FROM shares s
      JOIN posts p ON s.post_id = p.post_id
      JOIN users u ON p.user_id = u.user_id
      WHERE s.user_id = ?
      ORDER BY s.shared_at DESC
    `;
    db.query(sql, [user_id], (err, results) => {
      if (err) return reject(err);
      resolve(results);
    });
  });
};
