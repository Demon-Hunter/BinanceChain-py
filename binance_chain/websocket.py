# -*— coding:utf-8 -*-

"""
Binance chain Websocket Streams
https://binance-chain.github.io/api-reference/dex-api/ws-streams.html

Author: HuangTao
Date:   2019/04/03
Email:  huangtao@ifclover.com
"""

import json
import aiohttp
import asyncio
from urllib.parse import urljoin


class BinanceChainWsStream:
    """ Binance chain Websocket Streams
    """

    def __init__(self, wss=None, proxy=None, connected_callback=None):
        """ 初始化
        @param wss - websocket host, default host is wss://testnet-dex.binance.org
        @param proxy - HTTP proxy
        @param connected_callback - call this function when websocket connection connected,
                notice this function must be asynchronous, and no callback params.
        """
        self._wss = wss or "wss://testnet-dex.binance.org"
        self._proxy = proxy
        self._connected_callback = connected_callback

        self._ws = None  # websocket connection object
        self._callbacks = {}  # websocket message callback, key: topic, value: callback

        asyncio.get_event_loop().create_task(self._connect())

    def __del__(self):
        if self._ws:
            asyncio.get_event_loop().create_task(self._ws.close())

    async def _connect(self):
        session = aiohttp.ClientSession()
        url = urljoin(self._wss, "/api")
        print("wss:", url, "proxy:", self._proxy)
        self._ws = await session.ws_connect(url, proxy=self._proxy)
        if self._connected_callback:
            asyncio.get_event_loop().create_task(self._connected_callback())
        asyncio.get_event_loop().create_task(self._receive())

    async def _receive(self):
        """ 接收消息
        """
        async for msg in self.ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                try:
                    data = json.loads(msg.data)
                except:
                    data = msg.data
                asyncio.get_event_loop().create_task(self._process(data))
            elif msg.type == aiohttp.WSMsgType.BINARY:
                asyncio.get_event_loop().create_task(self._process_binary(msg.data))
            elif msg.type == aiohttp.WSMsgType.CLOSED:
                print("receive event CLOSED:", msg)
                asyncio.get_event_loop().create_task(self._connect())
                return
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print("receive event ERROR:", msg)
            else:
                print("unhandled msg:", msg)

    async def _process(self, msg):
        """ process text message that received from server node.
        @param msg - received msg
        """
        # TODO: heartbeat
        print("receive msg:", msg)
        topic = msg.get("stream")
        data = msg.get("data")
        callback = self._callbacks.get(topic)
        if callback:
            await callback(data)

    async def _process_binary(self, msg):
        """ 处理websocket上接收到的消息 binary类型
        """
        print("receive binary msg:", msg)

    async def do(self, method, topic, address=None, symbols=None, callback=None):
        """ send command to websocket server node.
        @param method - websocket command method, subscribe / unsubscribe
        @param topic - topic name
        @param address - user address
        @param symbols - list, symbol pairs
        @param callback - call this function when topic message received, notice this function must be asynchronous,
                    and has a parament `data`.
        """
        d = {
            "method": method,
            "topic": topic
        }
        if address:
            d["address"] = address
        if symbols:
            d["address"] = address
        await self._ws.send_json(d)
        self._callbacks[topic] = callback
