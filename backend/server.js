import express from "express";
import dotenv from "dotenv";

const app = express();
const PORT = process.env.PORT || 4000;

app.get("/", (req, res) => {
  res.send("Hello World");
});

app.use("/api/auth", authRoutes);
app.listen(PORT, () => console.log(`Server Running on port ${PORT}`));