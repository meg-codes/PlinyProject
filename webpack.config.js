// path and webpack
const path = require('path')
const webpack = require('webpack')

// webpack plugins
const BundleTracker = require('webpack-bundle-tracker')
const UglifyJsPlugin = require('uglifyjs-webpack-plugin')
const MiniCssExtractPlugin = require("mini-css-extract-plugin")


// configure dev mode because of absurdly misleading webpack documentation

module.exports = {
  entry: {
    'index': './media/js/index.js',
  },
  output: {
    path: path.resolve(__dirname, 'build'),
    filename: 'js/[name]-[hash].js'
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader'
        ],
      },
       {
        test: /\.scss$/,
        use: [
          'css-loader',
          'sass-loader'
        ],
      },
           {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: /node_modules/
      },
      {
        test: /\.(png|jpg|gif|svg|eot|ttf|woff|woff2)$/,
        loader: 'file-loader',
        options: {
          name: '[name].[hash].[ext]',
          publicPath: 'static/'
        }
      },

    ]
  },
  optimization: {
     minimizer: [new UglifyJsPlugin()]
  },
    devServer: {
    contentBase: path.join(__dirname, 'build'),
    hot: true,
    compress: true,
    port: 3000,
    allowedHosts: ['localhost'],
    headers: {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
    "Access-Control-Allow-Headers": "X-Requested-With, content-type, Authorization"
    },
    historyApiFallback: true,
    noInfo: true,
    overlay: true
  },
  performance: {
    hints: false
  },
  devtool: '#eval-source-map',
  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery',
      jquery: 'jquery',
      'window.jQuery': 'jquery'
    }),
    new MiniCssExtractPlugin({
      filename: 'css/[name]-[hash].css'
    })
  ]
}

if (process.env.NODE_ENV !== 'production') {
  module.exports.mode = process.env.NODE_ENV
  module.exports.output.publicPath = 'http://localhost:3000/'
}
