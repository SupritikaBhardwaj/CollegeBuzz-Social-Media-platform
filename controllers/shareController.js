import { sharePost, getSharedPosts } from "../models/Share.js";

// ✅ Share a post - FIXED VERSION
export const shareExistingPost = async (req, res) => {
  try {
    const { post_id } = req.body;
    const user_id = req.user.id; // Get user_id from authenticated token

    if (!post_id) {
      return res.status(400).json({ message: "Post ID required" });
    }

    const shareId = await sharePost(user_id, post_id);
    res.status(201).json({ message: "Post shared successfully", share_id: shareId });
  } catch (err) {
    console.error("Error sharing post:", err);
    res.status(500).json({ error: "Internal Server Error" });
  }
};

// ✅ Get all posts shared by a user
export const getUserSharedPosts = async (req, res) => {
  try {
    const { user_id } = req.params;
    const shares = await getSharedPosts(user_id);
    res.status(200).json(shares);
  } catch (err) {
    console.error("Error fetching shared posts:", err);
    res.status(500).json({ error: "Internal Server Error" });
  }
};