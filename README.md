
## Binance Chain python SDK
The Binance Chain python SDK is a asynchronous implementation for [Binance Chain API](https://binance-chain.github.io/index.html),
It includes the following modules:

- BinanceChainRestAPI - The [Binance Chain HTTP API](https://binance-chain.github.io/api-reference/dex-api/paths.html) client, provides access to a Binance Chain node deployment and market data services.
- BinanceChainWsStream - The [DEX websocket](https://binance-chain.github.io/api-reference/dex-api/ws-connection.html) streams data client, provides subscribe and unsubscribe topic from server.


### Requirement

- python 3.5.3 or above

- third-part library
	- aiohttp>=3.2.1


### Install
use `pip` install 
```text
pip install binance-chain
```

### Usage

##### REST API client

First, create a rest api client instance.
```python
from binance_chain.rest_api import BinanceChainRestAPI

HOST = "https://testnet-dex.binance.org"

api = BinanceChainRestAPI(HOST)
```

you can get node information,
```python
import asyncio

def test():
    result, err = await api.node_info()
    print("err:", err)
    print("result:", result)

asyncio.get_event_loop().run_until_complete(test())
```

and you can use the fallowing methods like that:
```python
    result, err = await api.get_time()
    result, err = await api.node_info()
    result, err = await api.validators()
    result, err = await api.peers()
    result, err = await api.account(ADDRESS)
    result, err = await api.tx(TX_HASH)
    result, err = await api.tokens()
    result, err = await api.markets()
    result, err = await api.fees()
    result, err = await api.depth("NNB-0AD_BNB", 20)
    result, err = await api.klines("NNB-0AD_BNB", "1d")
    result, err = await api.orders_closed(ADDRESS, symbol="BNB_BTC.B-918")
    result, err = await api.orders_open(ADDRESS)
    result, err = await api.order(order_id)
    result, err = await api.ticker_24hr("000-0E1_BNB")
    result, err = await api.trades(ADDRESS)
    result, err = await api.transactions(ADDRESS)
```


##### Websocket Stream data client

Create a websocket stream data client instance, and subscribe topics, or unsubscribe topics.
```python
import asyncio

from binance_chain import consts
from binance_chain.websocket import BinanceChainWsStream


HOST = "wss://testnet-dex.binance.org"
ADDRESS = "tbnb1efsnn75w7vxaummlhha9lmgcq4kpe38pjks0ee"


class Test:

    def __init__(self):
        self.ws = BinanceChainWsStream(HOST, connected_callback=self.subscribe_some_topics)

    async def subscribe_some_topics(self):
        print("websocket is connected success")
        await self.ws.do(consts.METHOD_SUBSCRIBE, consts.TOPIC_ORDER, ADDRESS, callback=self.orders_callback)
        await self.ws.do(consts.METHOD_SUBSCRIBE, consts.TOPIC_ORDER, ADDRESS, callback=self.depth_callback)

    async def orders_callback(self, data):
        print("order data:", data)

    async def depth_callback(self, data):
        print("depth data:", data)


Test()
asyncio.get_event_loop().run_forever()
```

- command method
```python
from binance_chain import consts

consts.METHOD_SUBSCRIBE  # subscribe
consts.METHOD_UNSUBSCRIBE  # unsubscribe
```

- topics
```python
from binance_chain import consts

consts.TOPIC_ORDER # orders
consts.TOPIC_ACCOUNT  # accounts
consts.TOPIC_TRANSFER  # transfers
consts.TOPIC_TRADE  # "trades
consts.TOPIC_MARKET_DIFF  # marketDiff
consts.TOPIC_MARKET_DEPTH  # marketDepth
consts.TOPIC_KLINE_1M  # kline_1m
consts.TOPIC_KLINE_3M  # kline_3m
consts.TOPIC_KLINE_5M  # kline_5m
consts.TOPIC_KLINE_15M  # kline_15m
consts.TOPIC_KLINE_30M  # kline_30m
consts.TOPIC_KLINE_1H  # kline_1h
consts.TOPIC_KLINE_2H  # kline_2h
consts.TOPIC_KLINE_4H  # kline_4h
consts.TOPIC_KLINE_6H  # kline_6h
consts.TOPIC_KLINE_8H  # kline_8h
consts.TOPIC_KLINE_12H  # kline_12h
consts.TOPIC_KLINE_1D  # kline_1d
consts.TOPIC_KLINE_3D  # kline_3d
consts.TOPIC_KLINE_1W  # kline_1w
consts.TOPIC_KLINE_1MON  # kline_1M
consts.TOPIC_TICKER  # ticker
consts.TOPIC_TICKER_ALL  # allTickers
consts.TOPIC_TICKER_MINI  # miniTicker
consts.TOPIC_TICKER_MINI_ALL  # allMiniTickers
consts.TOPIC_BLOCK_HEIGHT  # blockheight
```


For more API usage documentation, please check the [wiki...](https://binance-chain.github.io/index.html)
