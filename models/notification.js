import { DataTypes } from "sequelize";
import sequelize from "../config/db.js";

const Notification = sequelize.define("Notification", {
  notification_id: { type: DataTypes.INTEGER, autoIncrement: true, primaryKey: true },
  sender_id: { type: DataTypes.INTEGER, allowNull: false }, // who triggered it
  receiver_id: { type: DataTypes.INTEGER, allowNull: false }, // who gets it
  post_id: { type: DataTypes.INTEGER, allowNull: true },
  type: { 
    type: DataTypes.ENUM('like', 'comment', 'share', 'follow'), 
    allowNull: false 
  },
  message: { type: DataTypes.STRING, allowNull: false },
  is_read: { type: DataTypes.BOOLEAN, defaultValue: false },
  created_at: { type: DataTypes.DATE, defaultValue: DataTypes.NOW },
});

export default Notification;
