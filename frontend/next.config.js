const path = require('path')


const withCSS = require('@zeit/next-css')
module.exports = withCSS({
  cssModules: true,
  cssLoaderOptions: {
    mode: 'local'
  },
})
