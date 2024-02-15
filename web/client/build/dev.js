const baseConfig = require('./_base.js');
const { merge } = require('webpack-merge');

module.exports = merge(baseConfig, {
    mode: 'development',
    devServer: {
        historyApiFallback: {
            disableDotRule: true
        },
        open: true,
        liveReload: true,
        hot: false,
        port: 8000,
        allowedHosts: "all",
        proxy: {
            '/api': {
                target: {
                    host: "pugsley.int.wsr.at",
                    protocol: 'http:',
                    port: 11239
                },
                pathRewrite: {
                    '^/api': ''
                }
            }
        },
        client: {
            webSocketURL: 'ws://pugsley.int.wsr.at:11231/ws',
        },
    },
    devtool: 'source-map',
    output: {
        publicPath: '/'
    },
});
