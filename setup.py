# -*- coding:utf-8 -*-

from distutils.core import setup


setup(
    name="binance-chain",
    version="1.0.0",
    packages=["binance_chain", ],
    description="Binance chain python SDK",
    url="https://github.com/Demon-Hunter/BinanceChain-py",
    author="huangtao",
    author_email="huangtao@ifclover.com",
    license="MIT",
    keywords=["binance chain"],
    install_requires=[
        "aiohttp>=3.2.1",
    ],
)
