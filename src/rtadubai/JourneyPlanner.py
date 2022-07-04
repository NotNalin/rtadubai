import requests
from bs4 import BeautifulSoup

import StopFinder

url = 'https://www.rta.ae/wps/portal/rta/ae/home/!ut/p/z1/04_Sj9CPykssy0xPLMnMz0vMAfIjo8zi_QwMTNwNTAx93EPNDAwcQ4MCA8O8gowNXMz1w_Wj9KNASgIMLTycDAx9DIxDnIBKAkO8Ai29PD0MjaEKDHAARwP94NQ8_YLs7DRHR0VFAE1hpMw!/p0/IZ7_KG402B82M83EB0Q64NN5ER3GR6=CZ6_N004G041LGU600AURQQVJR30D7='


def findroute(fromstop: StopFinder.Stop, tostop: StopFinder.Stop):
    data = {
        'originHidden': fromstop.id,
        'destHidden': tostop.id,
        'captchaResponse': '03AGdBq264lipnjgpdag6gR_oFBX7MR3KL7B0doc2CRAJaEwN-UMWa2yQStB0P8V7abbRjGYSTHMQ5jmzsPnC5kXwAOMEmMZa0eHg4yyYNVmjkLAQSMcpBxV17RDM1zpCL6Gvmz9jKcBvG2NmEdZi6QmtJm6OzIpIFkpJg6bm-yTsYyhxjwBYRMwWi4GNd-RflRLJv51LqM4palzdsY2AwymzCenq8hgNb884_xfvZ-28RUQJ-z0M15oN2gjCdVH6mfQI82SFtuf2uDW91EkppP_bY_jl-7wq215_SiPHqC8owYdRKYPNpMK4gsPLSXbu-kBN3NrabOakD5Mo3AoPzJVqbkWG_Iky4C-rIboeFeyelBQX1fSf9let27QItzN_zB3saCm1-kjlRwEGyBS7POLizaMKXUealNAr4EEUXuSwgzo_2fu66qEucrDYxvjP0jj73ZNwO3qNz',
    }
    r = requests.post(url + 'NJgetTripSummary=/', data=data)
    response = BeautifulSoup(r.text, 'html.parser')
    data = dict((i[0], i[1].strip()) for i in [i.text.replace('\t', '').strip().split('\r\n') for i in response.find_all('p')])
    stops = []
    for i in response.find_all('li'):
        d = i.find_all('span', class_='jp_col')
        time = d[0].text.strip()
        stop = d[1].find(class_='jp_tmode_station').text.strip()
        try:
            method = d[1].find(class_='icon').get('xlink:href').split('#')[-1]
            duration = d[1].find(class_='jp_duration').text.replace('min', '').strip()
        except:
            method = None
            duration = None
        try:
            mode = d[1].find(class_='jp_tmode').text.strip()
        except:
            mode = None
        stops.append({
            'time': time,
            'stop': stop,
            'method': method,
            'duration': duration,
            'mode': mode,
        })
    data['stops'] = stops
    return data