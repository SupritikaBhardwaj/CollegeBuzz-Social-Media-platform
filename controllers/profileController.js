import User from "../models/User.js";

// 🧍 Get user profile
export const getUserProfile = async (req, res) => {
  try {
    const { user_id } = req.params;
    const user = await User.findByPk(user_id, {
      attributes: ['user_id', 'username', 'email', 'profile_pic', 'bio', 'created_at'],
    });
    if (!user) return res.status(404).json({ error: "User not found" });
    res.json(user);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Failed to fetch profile" });
  }
};

// ✏️ Update profile (bio or picture)
export const updateProfile = async (req, res) => {
  try {
    const { user_id } = req.params;
    const { bio, profile_pic } = req.body;

    const user = await User.findByPk(user_id);
    if (!user) return res.status(404).json({ error: "User not found" });

    if (bio) user.bio = bio;
    if (profile_pic) user.profile_pic = profile_pic;

    await user.save();
    res.json({ message: "Profile updated successfully", user });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Failed to update profile" });
  }
};
