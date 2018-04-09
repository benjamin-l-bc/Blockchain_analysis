# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 23:10:00 2018

@author: v-beshi
"""


import requests
import json
import pandas as pd
url="https://chain.api.btc.com/v3/block/latest/tx"
tx= requests.request("GET", url)
block_tx=json.loads(tx.text)
height=block_tx['data']['list'][0]['block_height']
block_time=block_tx['data']['list'][0]['block_time']
from_address=block_tx['data']['list'][0]['inputs'][0]['prev_addresses']
is_coinbase=block_tx['data']['list'][0]['is_coinbase']
is_sw_tx=block_tx['data']['list'][0]['is_sw_tx']
to_address=block_tx['data']['list'][0]['outputs'][0]['addresses']
value=block_tx['data']['list'][0]['outputs'][0]['value']