// src/server.js
require("dotenv").config();
const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const authRoutes = require("../routes/authRoutes");
const requestRoutes = require("../routes/requestRoutes");
const { sequelize } = require("../models");

const app = express();
app.use(cors());
app.use(bodyParser.json());

// Mount our routes
app.use("/auth", authRoutes);
app.use("/request", requestRoutes);

const PORT = process.env.PORT || 3000;

sequelize.authenticate().then(() => {
  console.log("Database connected successfully.");
  app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
  });
}).catch(error => {
  console.error("Failed to connect to DB:", error);
  process.exit(1);
});
