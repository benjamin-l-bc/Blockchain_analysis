# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 23:10:00 2018

@author: v-beshi
"""



import requests
import json
import pandas as pd
import pyodbc
con=pyodbc.connect('DRIVER={SQL Server};SERVER=Server;DATABASE=DB;UID=ID;PWD=pwd')

def getblockinfo(a,b):
#input the data from which block range you want to collect.
    for blocks in range(a,b):
        url="https://chain.api.btc.com/v3/block/{block}/tx".format(block=blocks)
		#connect to btc.com
        tx= requests.request("GET", url)
        block_tx=json.loads(tx.text)
        height=block_tx['data']['list'][0]['block_height']
		#get height
        block_time=block_tx['data']['list'][0]['block_time']
		#get block time(timestamp)

        for i in block_tx['data']['list']:
            is_coinbase=i['is_coinbase']
            is_sw_tx=i['is_sw_tx']
        
            for from_add in i['inputs']:
                if len(from_add['prev_addresses'])!=0:
                    from_address=from_add['prev_addresses'][0]
                else:
                    from_address=None
                prev_value=-from_add['prev_value']/100000000
				#get tranfer value
                print('height={h},time={t},add={fa},value={pv}'.format(h=height,t=block_time,fa=from_address,pv=prev_value))
                cursor=con.cursor()
                cursor.execute("insert into dbo.blockchain_tx values({0},{1},'{2}',{3})".format(height,block_time,from_address,prev_value)) 
                cursor.commit()
            for to_add in i['outputs']:
                if len(to_add['addresses'])!=0:
                    to_address=to_add['addresses'][0]
                else:
                    to_address=None
                value=to_add['value']/100000000
                print('height={h},time={t},add={ta},value={v}'.format(h=height,t=block_time,ta=to_address,v=value))
                cursor=con.cursor()
                cursor.execute("insert into dbo.blockchain_tx values({0},{1},'{2}',{3})".format(height,block_time,to_address,value)) 
                cursor.commit()
                cursor.close()