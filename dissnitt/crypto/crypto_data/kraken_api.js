'use strict';

const rp = require('request-promise');
const _ = require('lodash');
const insert = require('./insert_db')();

const ticker = 'https://api.kraken.com/0/public/Ticker';
const assets = {
    'XXBTZUSD': 'BTC-USD',
    'XETHZUSD': 'ETH-USD'
}

function getPrice(krakenPair) {
    var options = {
        url: ticker,
        method: 'GET',
        qs: {'pair': krakenPair}
    };

    rp(options)
        .then(tickerRaw => {
            const lastPrice = JSON.parse(tickerRaw).result[krakenPair].c[0];
            const assetPair = assets[krakenPair].split('-');
            insert.insertMongo('kraken', lastPrice, assetPair[0], assetPair[1]);
        })
        .catch(err => console.log(err));
};

function start() {
    _.keys(assets).forEach((item) => {
        getPrice(item);
    });
}

setInterval(start, 5000);
