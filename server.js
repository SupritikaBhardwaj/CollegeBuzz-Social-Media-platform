import express from "express";
import cors from "cors";
import bodyParser from "body-parser";
import dotenv from "dotenv";
import db from "./config/db.js";

// Routes
import authRoutes from "./routes/authRoutes.js";
import postRoutes from "./routes/postRoutes.js";
import shareRoutes from "./routes/shareRoutes.js";
import commentRoutes from "./routes/commentRoutes.js";
import likeRoutes from "./routes/likeRoutes.js";
import profileRoutes from "./routes/profileRoutes.js";
import interactionRoutes from "./routes/interactionRoutes.js";
import pollRoutes from "./routes/pollRoute.js";
// import notificationRoutes from "./routes/notificationRoutes.js";

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());
app.use(bodyParser.json());
app.use("/uploads", express.static("uploads"));

// Test DB connection (optional since db.js already logs it)
db.query("SELECT 1", (err) => {
  if (err) console.error("❌ Database not reachable:", err);
  else console.log("✅ Database test query successful");
});

// Routes
app.use("/api/auth", authRoutes);
app.use("/api/posts", postRoutes);
app.use("/api/comments", commentRoutes);
app.use("/api/shares", shareRoutes);
app.use("/api/likes", likeRoutes);
app.use("/api/profile", profileRoutes);
app.use("/api/interactions", interactionRoutes);
app.use("/api/polls", pollRoutes);
// app.use("/api/notifications", notificationRoutes);

app.get("/", (req, res) => res.send("CollegeBuzz Backend Running ✅"));

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`✅ Server running on port ${PORT}`));
