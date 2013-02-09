#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import pymysql
from datetime import datetime

conn = pymysql.connect(host='localhost', user='root', passwd='root', db='mysql')
cur = conn.cursor()
cur.execute("SELECT `last_price_changed` FROM gw2spidy.item  WHERE `last_price_changed` >0 ORDER BY `item`.`last_price_changed` DESC")
rows = cur.fetchall()
itemage = [(datetime.now() - r[0]).seconds/(60*60) for r in rows]


cur.execute("SELECT updated FROM gw2spidy.recipe WHERE updated > 0 ORDER BY recipe.updated DESC")
rows = cur.fetchall()
recipeage = [(datetime.now() - r[0]).seconds/(60*60) for r in rows]

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
plt.hist(itemage, bins=40)
plt.hist(recipeage, bins=40)
plt.savefig(os.path.dirname(sys.argv[0]) + '/../webroot/assets/img/freshness.png', transparent=True)