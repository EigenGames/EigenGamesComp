// routes/requestRoutes.js
const express = require("express");
const router = express.Router();
const { Request } = require("../models");

// For now, a dummy matching function (always returns null)
function findMatchingSolution(requestText) {
  return null;
}

router.post("/submit", async (req, res) => {
  try {
    const { userId, requestText } = req.body;
    const existingSolution = findMatchingSolution(requestText);
    if (existingSolution) {
      return res.json({ matched: true, data: existingSolution });
    } else {
      const newRequest = await Request.create({
        userId,
        requestText,
        status: "in_development",
      });
      return res.json({
        matched: false,
        message: "No matching solution found; new request created.",
        request: newRequest,
      });
    }
  } catch (error) {
    console.error("Request submission error:", error);
    return res.status(500).json({ error: "Server error" });
  }
});

module.exports = router;
