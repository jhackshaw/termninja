const withCSS = require("@zeit/next-css");

module.exports = withCSS({
  cssModules: true,
  env: {
    TERMNINJA_API_URL: process.env.TERMNINJA_API_URL,
    TERMNINJA_CLIENT_API_URL: process.env.TERMNINJA_CLIENT_API_URL,
  },
});
