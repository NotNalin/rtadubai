import requests

URL = "https://www.rta.ae/wps/portal/rta/ae/home/!ut/p/z1/04_Sj9CPykssy0xPLMnMz0vMAfIjo8zi_QwMTNwNTAx93EPNDAwcQ4MCA8O8gowNXMz1w_Wj9KNASgIMLTycDAx9DIxDnIBKAkO8Ai29PD0MjaEKDHAARwP94NQ8_YLs7DRHR0VFAE1hpMw!/p0/IZ7_KG402B82M83EB0Q64NN5ER3GR6=CZ6_N004G041LGU600AURQQVJR30D7="


def findstop(keyword, *, lang="en", limit=10):
    data = {
        "KeyedValue": keyword,
        "languageVal": lang,
    }
    response = requests.post(URL + "NJstopfinder=/", data=data).json()

    raw = response["stopFinder"]["points"]
    stops = []
    if len(raw) == 1:
        raw = raw["point"]
        stop = {}
        stop["id"] = raw["stateless"]
        stop["name"] = raw["name"]
        stop["coords"] = raw["ref"]["coords"]
        stops.append(stop)
        return stops

    for i in raw:
        if limit > 0:
            stop = {}
            stop["id"] = i["stateless"]
            stop["name"] = i["name"]
            stop["coords"] = i["ref"]["coords"]
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
                    self.id = id
                    self.name = name
                    self.coords = coords
                    raise ValueError("Not all required parameters are provided")
            else:
                raise ValueError("Either name or stop is required")

        self.id = stop["id"]
        self.name = stop["name"]
        self.coords = stop["coords"]

    def __repr__(self):
        return f"Stop : {self.name}"
