const path = require('path');

module.exports = {
  publicPath: '/static/vue/dist/',
  outputDir: path.resolve(__dirname, '../static/vue/dist/'),
  filenameHashing: false,
  runtimeCompiler: true,
  devServer: {
    writeToDisk: true
  }
};
