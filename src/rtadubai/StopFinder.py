import requests
from bs4 import BeautifulSoup

url = 'https://www.rta.ae/wps/portal/rta/ae/home/!ut/p/z1/04_Sj9CPykssy0xPLMnMz0vMAfIjo8zi_QwMTNwNTAx93EPNDAwcQ4MCA8O8gowNXMz1w_Wj9KNASgIMLTycDAx9DIxDnIBKAkO8Ai29PD0MjaEKDHAARwP94NQ8_YLs7DRHR0VFAE1hpMw!/p0/IZ7_KG402B82M83EB0Q64NN5ER3GR6=CZ6_N004G041LGU600AURQQVJR30D7='


def findstop(keyword, *, lang='en', limit=10):
    data = {
        'KeyedValue': keyword,
        'languageVal': lang,
    }
    response = requests.post(url + 'NJstopfinder=/', data=data).json()

    stops = []
    for i in response['stopFinder']['points']:
        if limit > 0:
            stop = {}
            stop['name'] = i['name']
            stop['coords'] = i['ref']['coords']
            stop['id'] = i['ref']['id']
            stops.append(stop)
            limit -= 1
    return stops


class Stop:
    
    def __init__(self, name=None, coords=None, stop_id=None, *, stop: findstop = None):
        if stop is None:
            if name != None:
                if stop_id is None or coords is None:
                    stop = findstop(name)[0]
                elif stop_id != None and coords != None:
                    self.name = name
                    self.coords = coords
                    self.id = id
                    raise ValueError('Not all required parameters are provided')
            else:
                raise ValueError('Either name or stop is required')

        self.name = stop['name']
        self.coords = stop['coords']
        self.id = stop['id']

    def __repr__(self):
        return f'Stop : {self.name}'
