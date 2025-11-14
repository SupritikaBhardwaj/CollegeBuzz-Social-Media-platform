import { createPost, getAllPosts, getPostById, deletePost, getPostOwner } from "../models/post.js";

// ✅ Create a new post
export const createNewPost = async (req, res) => {
  try {
    const { content, post_type, image_url } = req.body;
    const user_id = req.user.id;

    if (!content) {
      return res.status(400).json({ message: "Content is required" });
    }

    const postId = await createPost(user_id, content, image_url, post_type);
    res.status(201).json({ message: "Post created successfully", post_id: postId });
  } catch (err) {
    console.error("Error creating post:", err);
    res.status(500).json({ error: "Internal Server Error" });
  }
};

// ✅ Get all posts (feed)
export const fetchAllPosts = async (req, res) => {
  try {
    const posts = await getAllPosts();
    res.status(200).json(posts);
  } catch (err) {
    console.error("Error fetching posts:", err);
    res.status(500).json({ error: "Internal Server Error" });
  }
};

// ✅ Get single post details
export const fetchPostById = async (req, res) => {
  try {
    const { post_id } = req.params;
    const post = await getPostById(post_id);

    if (!post) {
      return res.status(404).json({ message: "Post not found" });
    }

    res.status(200).json(post);
  } catch (err) {
    console.error("Error fetching post:", err);
    res.status(500).json({ error: "Internal Server Error" });
  }
};

// ✅ NEW: Delete a post
export const deleteUserPost = async (req, res) => {
  try {
    const { post_id } = req.params;
    const user_id = req.user.id;

    if (!post_id) {
      return res.status(400).json({ message: "Post ID is required" });
    }

    // Check if post exists and belongs to user
    const postOwner = await getPostOwner(post_id);
    if (!postOwner) {
      return res.status(404).json({ message: "Post not found" });
    }

    if (postOwner !== user_id) {
      return res.status(403).json({ message: "You can only delete your own posts" });
    }

    const deleted = await deletePost(post_id, user_id);
    
    if (deleted) {
      res.status(200).json({ message: "Post deleted successfully" });
    } else {
      res.status(404).json({ message: "Post not found or already deleted" });
    }
  } catch (err) {
    console.error("Error deleting post:", err);
    res.status(500).json({ error: "Internal Server Error" });
  }
};

// ✅ NEW: Get user's posts
export const getUserPosts = async (req, res) => {
  try {
    const { user_id } = req.params;
    
    const sql = `
      SELECT p.*, u.name AS username
      FROM posts p
      JOIN users u ON p.user_id = u.user_id
      WHERE p.user_id = ?
      ORDER BY p.created_at DESC
    `;
    
    db.query(sql, [user_id], (err, results) => {
      if (err) {
        console.error("Error fetching user posts:", err);
        return res.status(500).json({ error: "Internal Server Error" });
      }
      res.status(200).json(results);
    });
  } catch (err) {
    console.error("Error fetching user posts:", err);
    res.status(500).json({ error: "Internal Server Error" });
  }
};