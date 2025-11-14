import express from "express";
import { getUserProfile, updateProfile } from "../controllers/profileController.js";

const router = express.Router();

router.get("/:user_id", getUserProfile);
router.put("/:user_id", updateProfile);

export default router;
