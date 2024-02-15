const HtmlWebpackPlugin = require('html-webpack-plugin');
const { VueLoaderPlugin } = require('vue-loader')

const path = require('path')
const resolve = (dir) => path.join(__dirname, '..', dir)

module.exports = {
    entry: {
        main: './src/main.js',
    },
    module: {
        rules: [{
            test: /\.css$/i,
            use: ['style-loader', 'css-loader'],
        }, {
            test: /\.scss$/i,
            use: ['style-loader', 'css-loader', "sass-loader"],
        }, {
            test: /\.vue$/i,
            use: 'vue-loader'
        }, {
            test: /\.(png|svg)$/,
            type: 'asset/resource'
        }
        ]
    },
    resolve: {
        alias: {
            '@': resolve('src'),
            'A': resolve('assets'),
        },
    },
    plugins: [
        // new CopyWebpackPlugin({
        //     patterns: [
        //         { from: 'data', to: 'data' },
        //         // { from: 'assets/img', to: 'img' },
        //         // { from: 'login.html', to: '' },
        //     ]
        // }),
        new HtmlWebpackPlugin({
            template: 'index.html',
            favicon: 'assets/icon.png',
        }),
        new VueLoaderPlugin(),
    ]
};