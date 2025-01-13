const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    entry: './src/index.js',
    output: {
        path: path.resolve('./dist/'),
        filename: '[name]-[fullhash].js',
        publicPath: '/static/frontend/',
    },
    plugins: [
        new BundleTracker({ path: __dirname, filename: 'webpack-stats.json' }),
    ],
    devServer: {
        publicPath: '/static/',
        hot: true,
        liveReload: true,
        headers: { 'Access-Control-Allow-Origin': '*' },
        proxy: {
            '/': 'http://localhost:8000',
        }
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env', '@babel/preset-react']
                    }
                }
            },
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader'],
            },
            {
                test: /\.(png|jpg|gif|svg)$/,
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            name: '[name].[hash].[ext]',
                            outputPath: 'static/media/'
                        }
                    }
                ]
            },
            {
                enforce: 'pre',
                test: /\.js$/,
                loader: 'source-map-loader',
                exclude: [
                  /node_modules\/antd\/dist\/antd\.css/
                ]
              },
        ],
    },
};
