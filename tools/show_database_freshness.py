#!/usr/bin/env python3
# coding: utf-8

import pymysql
from datetime import datetime

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np


def dataQ(cur, query):
    cur.execute(query)
    rows = cur.fetchall()
    data = [(datetime.now() - r[0]).seconds/(60*60) for r in rows if r[0] is not None]
    print(query)
    for ppp in [0,50,70,80,90,95,99,100]:
        print('{:3d}th percentile: {:.3f}'.format(ppp, np.percentile(data, ppp)))
    return data
    
def dataQListing(cur, type):
    return dataQ(cur, 'SELECT max(listing_datetime) FROM gw2spidy.'+type+'_listing GROUP BY item_id');

print('connecting to database ' + str(datetime.now()))
conn = pymysql.connect(host='localhost', user='root', passwd='root', db='mysql')
cur = conn.cursor()
print('downloading data')
data = [dataQListing(cur, 'buy'),
        dataQListing(cur, 'sell'),
        dataQ(cur, 'SELECT updated FROM gw2spidy.recipe')]

upper = max([np.percentile(row, 95) for row in data])
plt.hist(data, bins=40, weights=[np.zeros_like(r) + 1./len(r) for r in data], range=(0, upper), rwidth=1, label=['buy','sell','recipe'])
plt.xlim((0, upper))
plt.legend()
plt.xlabel('age (in hours)')
plt.ylabel('frequency (in percent)')
plt.title('Last refresh of listings / recipes ('+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+')')

import os, sys
folder = os.path.dirname(sys.argv[0]) + '/../webroot/assets/img/'
target = folder + 'freshness.png'
plt.savefig(target, transparent=True)

import shutil
shutil.copy(target, os.path.dirname(sys.argv[0]) + '/../../galleria/img/freshness.' + str(datetime.now()).replace(':','-') + '.png')