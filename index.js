const express = require("express");
const axios = require("axios");

const app = express();

app.get("/", (req, res) => {
    res.json({
        status: true,
        owner: "VERNEX",
        message: "API Running"
    });
});

app.get("/api/number", async (req, res) => {
    try {
        const num = req.query.num;

        if (!num) {
            return res.status(400).json({
                status: false,
                message: "Number parameter required"
            });
        }

        const response = await axios.get(
            `https://ft-osint-api.duckdns.org/api/number?key=ft-rahun2m&num=${num}`,
            {
                timeout: 15000
            }
        );

        const data = response.data;

        if (typeof data === "object") {
            delete data.by;
            delete data.channel;

            data.by = "VERNEX";
        }

        res.json(data);

    } catch (error) {
        console.error(error);

        res.status(500).json({
            status: false,
            message: error.message,
            details: error.response?.data || null
        });
    }
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
    console.log(`Server Running On Port ${PORT}`);
});
