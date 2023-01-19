#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
import re
from bs4 import BeautifulSoup

import sys

BASE_URL = 'https://vendas.portaldasfinancas.gov.pt/bens/'
SALES_PAGE = 'consultaVendasCurso.action'
# /detalheVenda.action?idVenda=14&sf=0019&ano=2022
DETAILS_PAGE = 'detalheVenda.action'

BASE_PARAMS = {
    'page': '1',
    'freguesia': '',
    'concelho': '',
    'distrito': '',
    'dataMin': '',
    'maximo': '',
    'tipoConsulta': '02',
    'dataMax': '',
    'minimo': '',
    'modalidade': '',
    'tipoBem': ''
}

MAX_PAGES = 2
SLEEP = 10

def get_max_pages(url):
    PAGES = 50
    if(PAGES>MAX_PAGES):
        if PAGES>MAX_PAGES:
            return MAX_PAGES
        else:
            return PAGES
    pass


def parse_sales_main_page(url, page):
    
    print ("requesting url", url)
    print ("requesting page", page)

    params = {
        'page': page,
        'freguesia': '',
        'concelho': '',
        'distrito': '',
        'dataMin': '',
        'maximo': '',
        'tipoConsulta': '02',
        'dataMax': '',
        'minimo': '',
        'modalidade': '',
        'tipoBem': ''
    }

    markup = requests.get(url, params=params)
    soup = BeautifulSoup(markup.content, 'html.parser')
    items = soup.find_all('table',class_='w95')
    html = '<table>'
    for item in items:
        for info in item.find_all('a',href=True, limit=1):
            details_url = str('https://vendas.portaldasfinancas.gov.pt/bens/') + str(info['href'])
            print("built details url", details_url)
            if "consulta" not in details_url:
                print(parse_details_page(details_url))
                html = html + str(parse_details_page(details_url))

    html = html + '</table>'
    return html


def parse_details_page(url):

    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')

    details_html = '<tr>'

    details = '<td>' + str(soup.select("#trFotoP > th.top.left > span:nth-child(2)")[0].contents[0]) + '</td>'
    details = details + '<td>' + str(soup.select("#trFotoP > th.top.left > span:nth-child(5)")[0].contents[0]) + '</td>'
    details = details + '<td>' + str(soup.select("#trFotoP > th.top.left > span:nth-child(8)")[0].contents[0]) + '</td>'
    details = details + '<td>' + str(soup.select("#trFotoP > th.top.left > span:nth-child(11)")[0].contents[0]) + '</td>'
    details = details + '<td>' + str(soup.select("#trFotoP > th.top.left > span:nth-child(14)")[0].contents[0]) + '</td>'
    details = details + '<td>' + str(soup.select("#trFotoP > th.top.left > span:nth-child(17)")[0].contents[0]) + '</td>'
    details = details + '<td>' + str(soup.select("#dataTable > tbody > tr:nth-child(3) > td > table > tbody > tr > th")) + '</td>'
    

    details_html = details_html + details + '</tr>'

    return details_html

#
# Main funtion
#
HTML_OPEN = '<html><body><head><meta charset="UTF-8"></head>'
HTML_CLOSE = '</body></html>'

HTML_STRING = HTML_OPEN

SALES_URL = BASE_URL + SALES_PAGE

# DEBUG 
'''
HTML_STRING = HTML_STRING + parse_sales_main_page(SALES_URL,1)
'''
for i in range(1,get_max_pages(SALES_URL)):
    HTML_STRING = HTML_STRING + parse_sales_main_page(SALES_URL,i)
    time.sleep(SLEEP)
HTML_STRING = HTML_STRING + HTML_CLOSE



html_file = open("testing.html","w")
html_file.write(HTML_STRING)
html_file.close()