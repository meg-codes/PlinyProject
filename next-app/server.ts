import express from "express";
import next from "next";

const env = process.env.NODE_ENV;
const dev = env !== 'production';
const app = next({ dev });
const handle = app.getRequestHandler();

interface Proxy {
  [key: string]: object
}

const devProxy: Proxy = {
  '/api': {
    target: 'http://localhost:8000',
  },
  '/people/nodes.json': {
    target: 'http://localhost:8000'
  },
  '/people/social_class.json': {
    target: 'http://localhost:8000'
  }
}

app
  .prepare()
  .then(() => {
    const server = express();

    // Set up the proxy.
    if (dev && devProxy) {
      const proxyMiddleware = require('http-proxy-middleware')
      Object.keys(devProxy).forEach(function (context) {
        server.use(proxyMiddleware(context, devProxy[context]))
      });
    }

    server.get(/\/people\/(\D*)?-?(\d+)$/, (req,res) => {
      const realPage = '/people-detail'
      const query = {id: req.params[1] || 1, nomina: req.params[0] || ''}
      app.render(req, res, realPage, query)
    });


    server.get('*', (req, res) => {
      return handle(req, res);
    });

    server.listen(3000, err => {
      if (err) throw err;
      console.log('> Ready on http://localhost:3000');
    });
  })
  .catch(ex => {
    console.error(ex.stack);
    process.exit(1);
  });