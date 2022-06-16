import json
import requests
from bs4 import BeautifulSoup

url = 'https://www.rta.ae/wps/portal/rta/ae/home/!ut/p/z1/04_Sj9CPykssy0xPLMnMz0vMAfIjo8zi_QwMTNwNTAx93EPNDAwcQ4MCA8O8gowNXMz1w_Wj9KNASgIMLTycDAx9DIxDnIBKAkO8Ai29PD0MjaEKDHAARwP94NQ8_YLs7DRHR0VFAE1hpMw!/p0/IZ7_KG402B82M83EB0Q64NN5ER3GR6=CZ6_N004G041LGU600AURQQVJR30D7='

def findstop(keyword, lang='en'):
    data = {
        'KeyedValue': keyword,
        'languageVal': lang,
        }
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


class Stop:
    def __init__(self, name=None, coords=None, stop_id=None, stop=None):
        if stop == None:
            if name != None:
                if stop_id == None or coords==None:
                    stop = findstop(name)[0]
                elif stop_id != None and coords != None:
                    self.name = name
                    self.coords = coords
                    self.id = id
                    raise Exception('Stop: Either name, coords or id must be provided')
            
            else:
                raise Exception('Stop: Either name, coords or id must be provided')
                
        self.name = stop['name']
        self.coords = stop['coords']
        self.id = stop['id']

        

print(json.dumps(findstop("China 3")[0], indent=2))
