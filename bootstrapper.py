# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 23:06:04 2020

@author: Hamzah
"""
import yfinance as yf
import xlsxwriter
import matplotlib.pyplot as plt
import pandas as pd
import xlrd
import os
import matplotlib.pyplot as plt
import numpy as np
import scipy
import random
import itertools
import datetime
from datetime import date
import time
from time import sleep
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *
from threading import Timer



# Directory for files
os.chdir(r"C:\Users\Hamzah\Documents\Python files")
wb = xlrd.open_workbook(r'C:\Users\Hamzah\Documents\Python files\bootstrap.xlsx')

#import excel file
data=pd.DataFrame()
data=pd.read_excel(wb,sheet_name=0)
#N=wb_tickers.nrows
pd.set_option('display.max_columns', None)  

#Input DATA which is a pandas dataframe including 3 columns: tenor, price and coupon rates. Input FREQUENCY which is the payment frequency, eg semiannual=2, Input FACE VALUE of bond, eg 100
#Example of input data frame is given below
#n	  price	  coupon
#0.5  100	4.00%
#1    100	4.30%
#1.5  100	4.50%
#2    100	4.90%




class bootstrapper:
    def __init__(self,data,frequency,face_value):
        self.data=data
        self.frequency=frequency
        self.face_value=face_value
    def spot_rates(self):
        n=len(self.data)
        pockets=[]
        spots=[]
        count=0
        for x in range(0,n):
            pocket=[]
            for y in range(0,count+1):
                pocket.append(y)
            count=count+1
            pockets.append(pocket)
        del(pockets[0])
        s_0=self.frequency*((self.face_value*(self.data['coupon'][0]/self.frequency)+self.face_value)/self.data['price'][0]-1)
        spots.append(s_0)
        for pocket in pockets:
            coupon_sum=[]
            num=len(pocket)-1
            for i in range(0,num):
                s=(((self.data['coupon'][num])/self.frequency)*self.face_value)/(1+spots[i]/self.frequency)**(i+1)
                coupon_sum.append(s)
            c=(self.data['coupon'][num]/self.frequency)*self.face_value
            current_price=self.data['price'][num]
            s_final=(((self.face_value+c)/(current_price-sum(coupon_sum)))**(1/(num+1))-1)*self.frequency
            spots.append(s_final)
        data['Spot Rates']=spots
    def binomial_pricing(self,T):
        #In construction
        Nodes={}
        for a in range(0,T):
            for b in range(0,a+1):
                Nodes[a,'_',b]=[]
        return Nodes
        

#Below is mainly for charting spot vs coupon curves, not required for class functions
fig=plt.figure()
fig.show()
ax=fig.add_subplot(111)

ax.plot(data['coupon'],label='Coupon rates')
ax.plot(data['Spot Rates'],label='Spot Rates')
plt.xlabel('tenors', fontsize=18)
plt.ylabel('rates', fontsize=16)
fig.suptitle('Rate Curves', fontsize=20)
plt.legend(loc=2)
plt.draw()

    
