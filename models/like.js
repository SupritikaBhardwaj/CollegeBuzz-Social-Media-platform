import { DataTypes } from "sequelize";
import db from "../config/db.js";


const Like = sequelize.define("Like", {
  like_id: { type: DataTypes.INTEGER, autoIncrement: true, primaryKey: true },
  post_id: { type: DataTypes.INTEGER, allowNull: false },
  user_id: { type: DataTypes.INTEGER, allowNull: false },
  created_at: { type: DataTypes.DATE, defaultValue: DataTypes.NOW },
});

export default Like;
