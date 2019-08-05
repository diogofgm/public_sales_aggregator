#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup

import sys

BASE_URL = 'https://vendas.portaldasfinancas.gov.pt/bens/consultaVendasCurso.action'

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

MAX_PAGES = 5

def get_max_pages(url):
    PAGES = 50
    if(PAGES>MAX_PAGES):
        if PAGES>MAX_PAGES:
            return MAX_PAGES
        else:
            return PAGES
    pass


def parse_details(details_url):
    html_string = ''
    details_markup = requests.get(details_url)
    details_soup = BeautifulSoup(details_markup.content, 'html.parser')

    details = details_soup.find_all('table',class_='w100')
    for table in details:
        #print(table)
        html_string = html_string + table.encode('utf-8')
    return html_string

def parse_page(url,page):
    
    print "requesting url", url
    print "requesting page", page

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

    markup = requests.get(BASE_URL, params=params)
    soup = BeautifulSoup(markup.content, 'html.parser')
    tabela = soup.find_all('td',class_='info-table-title')

    for linha in tabela:
        for info in linha.find_all('a',href=True):
            
            details_url = 'https://vendas.portaldasfinancas.gov.pt/bens/'+info['href']
            parse_details(details_url)
                 
    return parse_details(details_url)


#
# Main funtion
#
HTML_OPEN = '<html><body><head><meta charset="UTF-8"></head>'
HTML_CLOSE = '</body></html>'

HTML_STRING = HTML_OPEN

for i in range(0,get_max_pages(BASE_URL)):
    HTML_STRING = HTML_STRING + parse_page(BASE_URL,i)

HTML_STRING = HTML_STRING + HTML_CLOSE


Html_file= open("testing.html","w")
Html_file.write(HTML_STRING)
Html_file.close()