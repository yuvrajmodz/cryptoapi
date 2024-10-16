# Cryptocurrency API

## Features

- Retrieve cryptocurrency name, price, market cap using its symbol (short code).
- Simple RESTful API with JSON response.
- Flask-based lightweight server.
  
## How It Works

The application scrapes the data from `crypto.com/price` and searches for the requested cryptocurrency based on its symbol provided in the query parameter.

### Example:

To fetch Bitcoin data (BTC):

``` Example Request
GET http://your-server-ip:5001/crypto-api?cr=btc

### Developed By @YuvrajMODZ