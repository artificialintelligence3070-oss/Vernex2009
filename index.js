const express = require("express");
const axios = require("axios");

const app = express();

app.get("/api/number", async (req, res) => {
    try {
        const num = req.query.num;

        if (!num) {
            return res.status(400).json({
                status: false,
                message: "Number is required"
            });
        }

        const response = await axios.get(
            `https://ft-osint-api.duckdns.org/api/number?key=ft-rahun2m&num=${num}`
        );

        const data = response.data;

        delete data.by;
        delete data.channel;

        data.by = "VERNEX";

        res.json(data);

    } catch (error) {
        res.status(500).json({
            status: false,
            message: "Server Error"
        });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server Running On ${PORT}`);
});
