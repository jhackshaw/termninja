const withCSS = require('@zeit/next-css')



module.exports = withCSS({
  cssModules: true,
  cssLoaderOptions: {
    mode: 'local'
  },
  env: {
    TERMNINJA_API_URL: process.env.TERMNINJA_API_URL
  }
})
