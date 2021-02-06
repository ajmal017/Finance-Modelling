


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
wb = xlrd.open_workbook(r'C:\Users\Hamzah\Documents\Python files\NASDAQ_tickers.xlsx')

wb_tickers=wb.sheet_by_index(0)
N=wb_tickers.nrows
pd.set_option('display.max_columns', None)  

#create start and end dates
start_date="2020-01-01"
end_date="2020-12-10"

#Create tickers subset to create combinations
n_tickers=50
total_tickers=[]
for a in range(1,n_tickers+1):
    total_tickers.append(wb_tickers.row_values(a)[0])

market_data=pd.DataFrame()
for j in range(0,n_tickers):
    data=yf.download(total_tickers[j],start_date,end_date)
    market_data[total_tickers[j]]=data.Close

RMBK=market_data.pct_change(fill_method='ffill')

# Create benchmark
bench='SPY'
benchmark=pd.DataFrame()
data=yf.download(bench,start_date,end_date)
benchmark[bench]=data.Close
benchmark=benchmark.pct_change(fill_method='ffill')
b_mean=benchmark.mean()
b_sd=benchmark.std()

#In case want to send manual return benchmark
b_mean[0]=0.005
b_sd[0]=0.02
# define number of securities in portfolio
p=4

#Define weights
weights=[]
for weight in range(0,p):
    weights.append(1/p)


# Creating potential combinations
c=p
master_combination=itertools.combinations(total_tickers,c)
combinations=[]
for combo in master_combination:
    combinations.append(combo)

class portfolio_sd:
    def __init__(self,weights,combo,RMBK):
        self.weights=weights
        self.combo=combo
        self.RMBK=RMBK
    def portfolio_return(self):
        portfolio_build=pd.DataFrame()
        portfolio=pd.DataFrame()
        for ticker,weights in zip(self.combo,self.weights):
            portfolio_build[ticker]=self.RMBK[ticker]*weight
        portfolio=portfolio_build.sum(axis=1)
        port_return=portfolio.mean()
        return port_return
    def stock_var(self):
        stock_var=[]
        for w,tick in zip(self.weights,self.combo):
            sd_tick=self.RMBK[tick].std()
            stock_var.append((w**2)*(sd_tick**2))
        return sum(stock_var)
    def cov(self):
        portfolio_weights={}
        for s,w in zip(self.combo,self.weights):
            portfolio_weights[s]=w
        tc=2
        tc_master_combination=itertools.combinations(self.combo,tc)
        p_combinations=[]
        for p_com in tc_master_combination:
            p_combinations.append(p_com)
        sum_cov=[]
        for mini_combo in p_combinations:
            mini_port=pd.DataFrame()
            for sec in mini_combo:
                mini_port[sec]=RMBK[sec]
            correlation=mini_port.corr()
            covar=2*portfolio_weights[mini_combo[0]]*portfolio_weights[mini_combo[1]]*(correlation[sec][0])*(mini_port[mini_combo[0]].std())*(mini_port[mini_combo[1]].std())
            sum_cov.append(covar)
        return sum(sum_cov)
    def sigma(self):
        sd=(self.stock_var()+self.cov())**(1/2)
        return sd


# Create portfolio
possibles={}
for combo in combinations:
    portfolio=portfolio_sd(weights,combo,RMBK)
    if portfolio.portfolio_return()>b_mean[0] and portfolio.sigma()<b_sd[0]:
        possibles[combo]=portfolio.portfolio_return(),portfolio.sigma()
    print(combo)
print("possible number of winners are: ",len(possibles)/len(combinations))
