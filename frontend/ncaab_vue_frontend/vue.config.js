// vue.config.js
//https://cli.vuejs.org/config/#css-loaderoptions
//https://webpack.js.org/configuration/dev-server/
/**
 * @type {import('@vue/cli-service').ProjectOptions}
 */
 module.exports = {
    // options...
    devServer: {
        watchOptions: {
          ignored: /node_modules/,
          aggregateTimeout: 300,
          poll: 1000,
        },
        allowedHosts: ['dev.winecoffeewifi.com']
      }
  }
  