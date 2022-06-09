import json
import requests
from bs4 import BeautifulSoup

url = 'https://www.rta.ae/wps/portal/rta/ae/home/!ut/p/z1/04_Sj9CPykssy0xPLMnMz0vMAfIjo8zi_QwMTNwNTAx93EPNDAwcQ4MCA8O8gowNXMz1w_Wj9KNASgIMLTycDAx9DIxDnIBKAkO8Ai29PD0MjaEKDHAARwP94NQ8_YLs7DRHR0VFAE1hpMw!/p0/IZ7_KG402B82M83EB0Q64NN5ER3GR6=CZ6_N004G041LGU600AURQQVJR30D7='

def findstop(keyword):
    data = {'KeyedValue': keyword}
    r = requests.post(url + 'NJstopfinder=/', data=data)
    response = eval(BeautifulSoup(r.text, 'html.parser').text)
    x = 10
    l = []
    for i in response['stopFinder']['points']:
        if x > 0:
            d = {}
            d['name'] = i['name']
            d['coords'] = i['ref']['coords']
            d['id'] = i['ref']['id']
            l.append(d)
            x -= 1
    return l


# def findroute(fromstop, tostop):
#     data = {
#         'originHidden': fromstop,
#         'destHidden': tostop,
#     }
#     r = requests.post(url + 'NJgetTripSummary=/', data=data)
#     response = BeautifulSoup(r.text, 'html.parser').text
#     print(response)
    
# findroute('3502251','poiID:97641:96106345:-1:Hfw:Burj+Khalifa:Hfw:ANY:POI:494102:1211569:DMGV:dub')