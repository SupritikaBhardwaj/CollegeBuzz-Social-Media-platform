import db from "../config/db.js";

export const createPoll = (post_id, question, options) => {
  return new Promise((resolve, reject) => {
    const [option1, option2, option3 = null, option4 = null] = options;
    const sql = `INSERT INTO polls (post_id, question, option1, option2, option3, option4) VALUES (?, ?, ?, ?, ?, ?)`;
    db.query(sql, [post_id, question, option1, option2, option3, option4], (err, result) => {
      if (err) return reject(err);
      resolve(result.insertId);
    });
  });
};

export const getPollByPost = (post_id) => {
  return new Promise((resolve, reject) => {
    const sql = `SELECT * FROM polls WHERE post_id = ? LIMIT 1`;
    db.query(sql, [post_id], (err, rows) => {
      if (err) return reject(err);
      resolve(rows[0] || null);
    });
  });
};

export const votePoll = (poll_id, user_id, optionIndex) => {
  return new Promise((resolve, reject) => {
    const sql = `INSERT INTO poll_votes (poll_id, user_id, option_index) VALUES (?, ?, ?)`;
    db.query(sql, [poll_id, user_id, optionIndex], (err, result) => {
      if (err) return reject(err);
      resolve(result.insertId);
    });
  });
};

export const getPollResults = (poll_id) => {
  return new Promise((resolve, reject) => {
    const sql = `SELECT option_index, COUNT(*) as votes FROM poll_votes WHERE poll_id = ? GROUP BY option_index`;
    db.query(sql, [poll_id], (err, rows) => {
      if (err) return reject(err);
      resolve(rows);
    });
  });
};

// ✅ NEW: Delete poll votes when poll is deleted (handled by CASCADE if FK set)
export const deletePollByPost = (post_id) => {
  return new Promise((resolve, reject) => {
    const sql = `DELETE FROM polls WHERE post_id = ?`;
    db.query(sql, [post_id], (err, result) => {
      if (err) return reject(err);
      resolve(result.affectedRows > 0);
    });
  });
};