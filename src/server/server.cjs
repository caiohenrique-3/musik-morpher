// dependencies
const express = require("express");
const cors = require("cors");
const multer = require("multer");
const ffmpeg = require("fluent-ffmpeg");

// Setting up server
const app = express();
const upload = multer({ dest: "uploads/" });
const serverPort = 5000;

// For enabling requests with other domains
app.use(cors());

// Log incoming requests
app.use((req, res, next) => {
  console.log(`Received ${req.method} request to ${req.path}`);
  next();
});

// For downloading the file after modifying it
app.use("/output", express.static("output"));

// TODO: Do all of ffmpeg operations in a separate function instead
app.post("/upload", upload.single("file"), (req, res) => {
  const file = req.file;
  const speed = 1.6;

  ffmpeg(file.path)
    .audioFilters(`atempo=${speed}`)
    .saveToFile(`output/${file.filename}.mp3`)
    .on("end", () => {
      res.send(
        `http://localhost:${serverPort}/output/${file.filename}.mp3`,
      );
    })
    .on("error", (err) => {
      console.error(err);
      res.status(500).send("File processing failed");
    });
});

app.listen(serverPort, () => {
  console.log(`Server is running on http:localhost:${serverPort}`);
});
