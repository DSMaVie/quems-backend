import express from 'express';

const config = {
  port: 6299,
};

const server = express();
server.listen(config.port);

server.get('/', (req, res) => {
  res.send('Hello World');
});

// https://medium.com/better-programming/create-an-express-server-using-typescript-dec8a51e7f8d