'use strict';

const MongoClient = require('mongodb').MongoClient;
const url = 'mongodb://localhost:27017/';

module.exports = () => {
    function insertMongo(exchange, price, currency, den) {
        const priceDoc = {
          exchange: exchange,
          price: price,
          currency: currency,
          denomination: den,
          timestamp: Date.now()
        };

        _mongoDB(priceDoc);
    }

    function _mongoDB(doc) {
        MongoClient.connect(url, (err, db) => {
            if (err) throw(err);
            const dbo = db.db("cryptoData");

            dbo.collection('prices').insertOne(doc, (err, result) => {
              if (err) throw(err);
              db.close();
            });
        });
    }


    return {
        insertMongo
    }
};
