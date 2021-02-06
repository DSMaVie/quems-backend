import express from "express";

const config = {
  port: 6299,
};

const server = express();

server.get("/", (req, res) => {
  res.send("Hello World");
});
