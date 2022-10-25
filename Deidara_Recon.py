import sys
import os
import threading
import socket
import json
import requests
from bs4 import BeautifulSoup
import urllib.request
import multiprocessing
import pandas as pd
import time
from requests_futures.sessions import FuturesSession
import numpy as np
import urllib3
from Wappalyzer import Wappalyzer, WebPage
urllib3.disable_warnings()

df = pd.read_fwf('output', names=["Subdomains"])
df['http'] = df['Subdomains']
df['https'] = df['Subdomains']
df['http'] = 'http://' + df['http'].astype(str)
df['https'] = 'https://' + df['https'].astype(str)
record_list = df.to_dict(orient="records")
record_list

########### request function ############

def requests_logic():
    temp_list=[]
    for record_dict in record_list.copy(): 
        try:
            r = requests.head(record_dict.get('https'), verify=False)
            record_dict["status_value"]= r.status_code
            temp_list.append(record_dict)
        except requests.exceptions.ConnectionError:
            record_dict["status_value"]= "unable to request"
            temp_list.append(record_dict)  
    return temp_list      
# requests_logic()
record_list_with_status_code=requests_logic()
record_list_with_status_code


########### response function ############

def responce_logic():
    temp_list=[]
    for record_dict in record_list.copy(): 
        try:
            r = requests.head(record_dict.get('http'), verify=False)
            r.encoding
            record_dict["headers"]= (dict(r.headers))
            # record_dict["headers"]= json.dumps(dict(r.headers))
            temp_list.append((record_dict))
        except requests.exceptions.ConnectionError:
            record_dict["headers"]= "unable to request"
            temp_list.append(record_dict)  
    return temp_list
# responce_logic()
record_list_with_headers=responce_logic()
record_list_with_headers

########### Sub IP function ############
def Sub_IP():
    temp_list=[]
    for record_dict in record_list.copy(): 
        IP_A = socket.gethostbyname(record_dict.get('Subdomains'))
        record_dict["Resolved_IP"]= IP_A
        temp_list.append(record_dict)
    return temp_list
            
a = Sub_IP()
a

########### Scraping function ############
def scarpe():
    temp_list=[]
    for record_dict in record_list.copy():
       url = ((record_dict.get('http')))
       reqs = requests.get(url)
       soup = BeautifulSoup(reqs.text, 'html.parser')
       urls = []
       for link in soup.find_all('a'):
            url_list = link.get('href')
            urls.append(url_list)
            record_dict["URLs"]= urls
    temp_list.append(record_dict)
    return (temp_list)
a = scarpe()
a


