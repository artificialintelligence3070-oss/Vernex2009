const express = require("express");
const axios = require("axios");

const app = express();

app.get("/api/number", async (req, res) => {
  try {
    const num = req.query.num;

    const response = await axios.get(
      `https://ft-osint-api.duckdns.org/api/number?key=ft-rahun2m&num=${num}`
    );

    const data = response.data;

    delete data.by;
    delete data.channel;

    data.by = "VERNEX";

    res.json(data);
  } catch {
    res.status(500).json({
      success: false,
      message: "Server Error",
      by: "VERNEX"
    });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT);
