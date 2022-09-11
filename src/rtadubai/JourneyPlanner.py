import requests
from bs4 import BeautifulSoup

import rtadubai.rta_captcha as rta_captcha

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



def findroute(fromstop: Stop, tostop: Stop):
    data = {
        "originHidden": fromstop.id,
        "destHidden": tostop.id,
        "captchaResponse": rta_captcha.CAPTCHA,
    }

    r = requests.post(URL + "NJgetTripSummary=/", data=data)
    response = BeautifulSoup(r.text, "html.parser")

    error = response.find("div", class_="mt-3 p-4")
    if error is not None:
        raise ValueError(error.text)

    data = dict((i[0], i[1].strip()) for i in [i.text.replace("\t", "").strip().split("\r\n") for i in response.find_all("p")])

    stops = []
    for i in response.find_all("li"):
        d = i.find_all("span", class_="jp_col")
        time = d[0].text.strip()
        stop = d[1].find(class_="jp_tmode_station").text.strip()

        try:
            method = d[1].find(class_="icon").get("xlink:href").split("#")[-1]
            duration = d[1].find(class_="jp_duration").text.replace("min", "").strip()
        except:
            method = None
            duration = None

        try:
            mode = d[1].find(class_="jp_tmode").text.strip()
        except:
            mode = None

        stops.append(
            {
                "time": time,
                "stop": stop,
                "method": method,
                "duration": duration,
                "mode": mode,
            }
        )

    data["stops"] = stops
    return data


def departures(stop: Stop):
    data = {"departureStopHidden": stop.id, "captchaResponse": rta_captcha.CAPTCHA}

    r = requests.post(URL + "NJgetDepartureBoard=/", data=data)
    response = BeautifulSoup(r.text, "html.parser")

    raw = [i.text.split("\n") for i in response.find_all("li")]
    methodlist = [i.get("xlink:href").split("#")[-1] for i in response.find_all("use")]

    data = []
    for i in raw:
        l = []
        for j in i:
            n = j.strip()
            if n != "":
                l.append(n)
        data.append(l)

    transports = []
    for i in range(len(data)):
        transport = {
            "Mode": data[i][0],
            "Type": methodlist[i],
            "Destination": data[i][1],
            "Platform": data[i][2].split()[1],
            "Time": data[i][3],
        }

        if len(data[i]) == 5:
            if data[i][4] == "On time":
                transport["Delay"] = None
            else:
                transport["Delay"] = data[i][4].split()[1]
        else:
            transport["Delay"] = None
        transports.append(transport)

    return transports
