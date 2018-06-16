'use strict';

const WebSocket = require('ws');
const insert = require('./insert_db')();

function gdax() {
    const ws = new WebSocket('wss://ws-feed.gdax.com');

    const subscribe = {
        type: "subscribe",
        product_ids: [ "ETH-USD", "BTC-USD"],
        channels: [
            {
              name: "ticker",
              product_ids: [ "BTC-USD", "ETH-USD" ]
            }
        ]
    }

    ws.on('open', function open() {
        ws.send(JSON.stringify(subscribe));
    });

    ws.on('message', function incoming(data) {
        if (JSON.parse(data).type === 'ticker') {
            const jsoData = JSON.parse(data);
            const currencyData = jsoData.product_id.split('-');
            console.log('adding price data');
            insert.insertMongo('gdax', jsoData.price,
                currencyData[0], currencyData[1]);
        }
    });

    ws.on('close', function close() {
      console.log('disconnected');
    });
}

gdax();
