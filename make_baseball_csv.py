#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import bs4
from datetime import datetime as dt
import datetime
import csv

if __name__ == "__main__":
    output = [['date', 'carp_score', 'opponent_name', 'opponent_score']]
    for year in [2016, 2017]:
        date = dt(year,4,1)
        month_tmp = date.month
        URL = 'http://npb.jp/games/' + str(date.year) + '/' + 'schedule_' + str('{0:02d}'.format(date.month)) + '_detail.html'
        res = requests.get(URL)
        soup = bs4.BeautifulSoup(res.content, "html.parser")
        res.raise_for_status()
        while date.month < 12:
            daily_result = []
            results = soup.find_all('tr', id='date'+'{0:02d}'.format(date.month)+'{0:02d}'.format(date.day))
            if len(results[0].find('td')) <= 1:
                date += datetime.timedelta(days=1)
                if date.month != month_tmp:
                    URL = 'http://npb.jp/games/' + str(date.year) + '/' + 'schedule_' + str('{0:02d}'.format(date.month)) + '_detail.html'
                    print(URL)
                    res = requests.get(URL)
                    try:
                        res.raise_for_status()
                    except:
                        break
                    soup = bs4.BeautifulSoup(res.content, "html.parser")
                    month_tmp = date.month
                continue
            daily_result.append(date.strftime('%Y-%m-%d'))
            for result in results:
                if (result.select('.team1')[0].getText() == '広島'):
                    if len(result.select('.score1')) < 1:
                        break
                    daily_result.append(result.select('.score1')[0].getText())
                    daily_result.append(result.select('.team2')[0].getText())
                    daily_result.append(result.select('.score2')[0].getText())
                    output.append(daily_result)
                    break
                if result.select('.team2')[0].getText() == '広島':
                    if len(result.select('.score1')) < 1:
                        break
                    daily_result.append(result.select('.score2')[0].getText())
                    daily_result.append(result.select('.team1')[0].getText())
                    daily_result.append(result.select('.score1')[0].getText())
                    output.append(daily_result)
                    break
            print(daily_result)
            date += datetime.timedelta(days=1)
            if date.month != month_tmp:
                URL = 'http://npb.jp/games/' + str(date.year) + '/' + 'schedule_' + str('{0:02d}'.format(date.month)) + '_detail.html'
                print(URL)
                try:
                    res = requests.get(URL)
                except:
                    break
                res.raise_for_status()
                soup = bs4.BeautifulSoup(res.content, "html.parser")
                month_tmp = date.month

    with open('carp_games.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(output)
