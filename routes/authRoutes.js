// routes/authRoutes.js
const express = require("express");
const router = express.Router();
const { checkTelegramAuth } = require("../utils/telegramAuth"); // We'll create this next.
const { User } = require("../models");
const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;

router.get("/telegram/callback", async (req, res) => {
  try {
    const data = req.query; // Telegram sends auth data via query parameters
    if (!checkTelegramAuth(data, TELEGRAM_BOT_TOKEN)) {
      return res.status(401).json({ error: "Invalid Telegram auth data" });
    }
    const [user] = await User.findOrCreate({
      where: { telegramId: data.id },
      defaults: {
        username: data.username || "",
        firstName: data.first_name || "",
        lastName: data.last_name || ""
      },
    });
    return res.json({ success: true, user });
  } catch (error) {
    console.error("Telegram auth error:", error);
    return res.status(500).json({ error: "Server error" });
  }
});

module.exports = router;
