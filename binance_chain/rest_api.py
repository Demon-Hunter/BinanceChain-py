# -*- coding:utf-8 -*-

"""
Binance chain REST API
https://binance-chain.github.io/api-reference/dex-api/paths.html

Author: HuangTao
Date:   2019/04/03
Email:  huangtao@ifclover.com
"""

import aiohttp
import asyncio
from urllib.parse import urljoin


__all__ = ("BinanceChainRestAPI", )


class BinanceChainRestAPI:
    """ Binance chain REST API
    """

    def __init__(self, host=None, timeout=10, proxy=None):
        """ 初始化
        @param host Binance chain's REST API host, default is the test host: https://testnet-dex.binance.org
        @param timeout HTTP request timeout(s), default 10s
        @param proxy HTTP proxy
        """
        self._host = host or "https://testnet-dex.binance.org"
        self._timeout = timeout
        self._proxy = proxy

        self._session = aiohttp.ClientSession()

    def __del__(self):
        asyncio.get_event_loop().create_task(self._session.close())

    async def get_time(self):
        """ Get the block time.
        refer: https://binance-chain.github.io/api-reference/dex-api/paths.html#apiv1time
        """
        uri = "/api/v1/time"
        result, err = await self.request("GET", uri)
        return result, err

    async def node_info(self):
        """ Get node information.
        refer: https://binance-chain.github.io/api-reference/dex-api/paths.html#apiv1node-info
        """
        uri = "/api/v1/node-info"
        result, err = await self.request("GET", uri)
        return result, err

    async def validators(self):
        """ Get validators.
        refer: https://binance-chain.github.io/api-reference/dex-api/paths.html#apiv1validators
        """
        uri = "/api/v1/validators"
        result, err = await self.request("GET", uri)
        return result, err

    async def peers(self):
        """ Get network peers.
        refer: https://binance-chain.github.io/api-reference/dex-api/paths.html#apiv1peers
        """
        uri = "/api/v1/peers"
        result, err = await self.request("GET", uri)
        return result, err

    async def account(self, address):
        """ Get an account.
        refer: https://binance-chain.github.io/api-reference/dex-api/paths.html#apiv1accountaddress
        """
        uri = "/api/v1/account/{address}".format(address=address)
        result, err = await self.request("GET", uri)
        return result, err

    async def account_sequence(self, address):
        """ Get an account sequence.
        refer: https://binance-chain.github.io/api-reference/dex-api/paths.html#apiv1accountaddresssequence
        """
        uri = "/api/v1/account/{address}/sequence".format(address=address)
        result, err = await self.request("GET", uri)
        return result, err

    async def tx(self, hash_):
        """ Get a transaction.
        @param hash_ transaction ID
        refer: https://binance-chain.github.io/api-reference/dex-api/paths.html#apiv1txhash
        """
        uri = "/api/v1/tx/{hash_}?format=json".format(hash_=hash_)
        result, err = await self.request("GET", uri)
        return result, err

    async def tokens(self):
        """ Get tokens list.
        refer: https://binance-chain.github.io/api-reference/dex-api/paths.html#apiv1tokens
        """
        uri = "/api/v1/tokens"
        result, err = await self.request("GET", uri)
        return result, err

    async def markets(self):
        """ Get market pairs.
        refer: https://binance-chain.github.io/api-reference/dex-api/paths.html#apiv1markets
        """
        uri = "/api/v1/markets"
        result, err = await self.request("GET", uri)
        return result, err

    async def fees(self):
        """ Obtain trading fees information.
        refer: https://binance-chain.github.io/api-reference/dex-api/paths.html#apiv1fees
        """
        uri = "/api/v1/fees"
        result, err = await self.request("GET", uri)
        return result, err

    async def depth(self, symbol, limit):
        """ Get the order book.
        @param symbol Market pair symbol, e.g. NNB-0AD_BNB
        @param limit The limit of results. Allowed limits [5, 10, 20, 50, 100, 500, 1000]
        refer: https://binance-chain.github.io/api-reference/dex-api/paths.html#apiv1depth
        """
        uri = "/api/v1/depth"
        params = {
            "symbol": symbol,
            "limit": limit
        }
        result, err = await self.request("GET", uri, params)
        return result, err

    async def broadcast(self, body, sync=None):
        """ Broadcast a transaction.
        @param sync Synchronous broadcast
        @param body binary transaction
        refer: https://binance-chain.github.io/api-reference/dex-api/paths.html#apiv1broadcast
        """
        uri = "/api/v1/broadcast"
        if sync:
            params = {"sync": sync}
        else:
            params = {}
        headers = {
            "content-type": "text/plain"
        }
        result, err = await self.request("GET", uri, params=params, data=body, headers=headers)
        return result, err

    async def klines(self, symbol, interval, limit=300, start=None, end=None):
        """ Get candlestick bars.
        @param symbol Market pair symbol, e.g. NNB-0AD_BNB
        @param interval interval. Allowed value [1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M]
        @param limit The limit of results. default 300; max 1000.
        @param start start time in Milliseconds
        @param end end time in Milliseconds
        refer: https://binance-chain.github.io/api-reference/dex-api/paths.html#apiv1klines
        """
        uri = "/api/v1/klines"
        params = {
            "symbol": symbol,
            "interval": interval
        }
        if limit:
            params["limit"] = limit
        if start:
            params["startTime"] = start
        if end:
            params["endTime"] = end
        result, err = await self.request("GET", uri, params)
        return result, err

    async def orders_closed(self, address, offset=0, limit=500, symbol=None, side=None, status=None, start=None,
                            end=None, total=0):
        """ Get closed orders.
        @param address the owner address
        @param offset start with 0; default 0.
        @param symbol Market pair symbol, e.g. NNB-0AD_BNB
        @param limit The of results. default 500; max 1000.
        @param side order side. 1 for buy and 2 for sell.
        @param status order status list. Allowed value [Ack, PartialFill, IocNoFill, FullyFill, Canceled, Expired,
                    FailedBlocking, FailedMatching]
        @param start start time in Milliseconds
        @param end end time in Milliseconds
        @param total total number required, 0 for not required and 1 for required; default not required,
                    return total=-1 in response
        refer: https://binance-chain.github.io/api-reference/dex-api/paths.html#apiv1ordersclosed
        """
        uri = "/api/v1/orders/closed"
        params = {
            "address": address,
            "offset": offset,
            "limit": limit,
            "total": total
        }
        if symbol:
            params["symbol"] = symbol
        if side:
            params["side"] = side
        if status:
            params["status"] = status
        if start:
            params["start"] = start
        if end:
            params["end"] = end
        result, err = await self.request("GET", uri, params)
        return result, err

    async def orders_open(self, address, offset=0, limit=500, symbol=None, total=0):
        """ Get open orders.
        @param address the owner address
        @param offset start with 0; default 0.
        @param symbol Market pair symbol, e.g. NNB-0AD_BNB
        @param limit The of results. default 500; max 1000.
        @param total total number required, 0 for not required and 1 for required; default not required,
                    return total=-1 in response
        refer: https://binance-chain.github.io/api-reference/dex-api/paths.html#apiv1ordersopen
        """
        uri = "/api/v1/orders/open"
        params = {
            "address": address,
            "offset": offset,
            "limit": limit,
            "total": total
        }
        if symbol:
            params["symbol"] = symbol
        result, err = await self.request("GET", uri, params)
        return result, err

    async def order(self, order_id):
        """ Get an order.
        @param order_id order id
        refer: https://binance-chain.github.io/api-reference/dex-api/paths.html#apiv1ordersid
        """
        uri = "/api/v1/orders/{order_id}".format(order_id=order_id)
        result, err = await self.request("GET", uri)
        return result, err

    async def ticker_24hr(self, symbol=None):
        """ Get a market ticker.
        @param symbol Market pair symbol, e.g. NNB-0AD_BNB
        refer: https://binance-chain.github.io/api-reference/dex-api/paths.html#apiv1ticker24hr
        """
        uri = "/api/v1/ticker/24hr"
        if symbol:
            params = {"symbol": symbol}
        else:
            params = None
        result, err = await self.request("GET", uri, params)
        return result, err

    async def trades(self, address=None, symbol=None, buyer_order_id=None, seller_order_id=None, side=None, height=None,
                     quote_asset=None, offset=0, limit=500, start=None, end=None, total=0):
        """ Get market trades.
        @param address the owner address
        @param symbol Market pair symbol, e.g. NNB-0AD_BNB
        @param buyer_order_id buyer order id
        @param seller_order_id seller order id
        @param side order side. 1 for buy and 2 for sell.
        @param height block height
        @param quote_asset quote asset
        @param offset start with 0; default 0.
        @param limit default 500; max 1000.
        @param start start time in Milliseconds
        @param end end time in Milliseconds
        @param total total number required, 0 for not required and 1 for required; default not required,
                    return total=-1 in response
        refer: https://binance-chain.github.io/api-reference/dex-api/paths.html#apiv1trades
        """
        uri = "/api/v1/trades"
        params = {
            "offset": offset,
            "limit": limit,
            "total": total
        }
        if address:
            params["address"] = address
        if symbol:
            params["symbol"] = symbol
        if buyer_order_id:
            params["buyerOrderId"] = buyer_order_id
        if seller_order_id:
            params["sellerOrderId"] = seller_order_id
        if symbol:
            params["symbol"] = symbol
        if side:
            params["side"] = side
        if height:
            params["height"] = height
        if quote_asset:
            params["quoteAsset"] = quote_asset
        if start:
            params["start"] = start
        if end:
            params["end"] = end
        result, err = await self.request("GET", uri, params)
        return result, err

    async def transactions(self, address, block_height=None, side=None, offset=None, limit=None, start=None, end=None,
                           tx_asset=None, tx_type=None):
        """ Gets a list of transactions. Multisend transaction is not available in this API.
        @param address the owner address
        @param block_height blockHeight
        @param side transaction side. Allowed value [RECEIVE, SEND]
        @param offset offset
        @param limit list limit
        @param start start time in Milliseconds
        @param end end time in Milliseconds
        @param tx_asset txAsset
        @param tx_type transaction type. Allowed value [NEW_ORDER, ISSUE_TOKEN, BURN_TOKEN, LIST_TOKEN, CANCEL_ORDER,
                    FREEZE_TOKEN, UN_FREEZE_TOKEN, TRANSFER, PROPOSAL, VOTE,MINT, DEPOSIT]
        refer: https://binance-chain.github.io/api-reference/dex-api/paths.html#apiv1transactions
        """
        uri = "/api/v1/transactions"
        params = {
            "address": address
        }
        if block_height:
            params["blockHeight"] = block_height
        if side:
            params["side"] = side
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if start:
            params["startTime"] = start
        if end:
            params["endTime"] = end
        if tx_asset:
            params["txAsset"] = tx_asset
        if tx_type:
            params["txType"] = tx_type
        result, err = await self.request("GET", uri, params)
        return result, err

    async def request(self, method, uri, params=None, body=None, data=None, headers=None):
        """ HTTP request
        @param method HTTP Method, GET / POST / DELETE / PUT
        @param uri HTTP request uri
        @param params HTTP request query params
        """
        url = urljoin(self._host, uri)
        try:
            response = await self._session.get(url, params=params, json=body, data=data, headers=headers,
                                               timeout=self._timeout, proxy=self._proxy)
            if response.status != 200:
                print("method:", method, "url:", url, "response status:", response.status)
                text = await response.text()
                return None, text
            result = await response.json()
        except Exception as e:
            print(e)
            return None, e
        return result, None
