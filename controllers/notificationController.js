import Notification from "../models/Notification.js";

// 🔔 Send notification (used internally when user likes/comments/shares)
export const sendNotification = async (sender_id, receiver_id, type, post_id, message) => {
  try {
    await Notification.create({ sender_id, receiver_id, type, post_id, message });
  } catch (error) {
    console.error("Notification error:", error);
  }
};

// 🧾 Get all notifications for a user
export const getNotifications = async (req, res) => {
  try {
    const { user_id } = req.params;
    const notifications = await Notification.findAll({
      where: { receiver_id: user_id },
      order: [["created_at", "DESC"]],
    });
    res.json(notifications);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Failed to get notifications" });
  }
};

// ✅ Mark notification as read
export const markAsRead = async (req, res) => {
  try {
    const { notification_id } = req.params;
    const notification = await Notification.findByPk(notification_id);
    if (!notification) return res.status(404).json({ error: "Notification not found" });

    notification.is_read = true;
    await notification.save();

    res.json({ message: "Marked as read", notification });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Failed to mark notification" });
  }
};
