import requests
from bs4 import BeautifulSoup

URL = "https://www.rta.ae/wps/portal/rta/ae/public-transport/journeyplanner/!ut/p/z1/jY5BC8IgGIZ_kp_Oph2Vhc62uZGjzUt4iCGUdYh-fyF0bPXeXngeeJBHE_IpPOMSHvGWwuX9Z1-e9ooCkZy0vOQVCFY7vqkUtoyhYwa6HnMtATdQOAliHJwZtqbWuED-Hx--TMBv32ekA6AKKG54a3cgsNFWkYEoQz_ASmIGVhoO54Tu13GC2C8vMVd2Ng!!/p0/IZ7_KG402B82M868D0A7IT85DG1OF6=CZ6_KG402B82M868D0A7IT85DG1O77="


def findstop(keyword):
    data = {
        "KeyedValue": keyword
    }
    response = requests.post(URL + "NJstopfinderShail=/", data=data).json()
    raw = response["stopLocationOrCoordLocation"]
    stops = []
    for i in raw:
        stop = {}
        if "StopLocation" in i:
            i = i["StopLocation"]
        elif "CoordLocation" in i:
            i = i["CoordLocation"]
        else:
            print(raw)
        stop["name"] = i["name"]
        stop["id"] = i["id"]
        stop["coords"] = f'{i["lat"]},{i["lon"]}'
        stops.append(stop)
    return stops


class Stop:
    def __init__(self, name, *, stop=None):

        if stop is None:
            stop = findstop(name)[0]
        self.name = stop["name"]
        self.id = stop["id"]
        self.coords = stop["coords"]

    def __repr__(self):
        return f"Stop: {self.name}"


def departures(stop : Stop):
    data = {
        "departureLine" : stop.name,
        "departureStateless" : stop.id,
        "departureCoords" : stop.coords,
    }
    response = requests.post(URL + "NJdepartureBoardShailRev=/", data=data)
    soup = BeautifulSoup(response.text, "html.parser")

    d = soup.find(class_ = "jp_departure_result")
    if d is None:
        if soup.find(class_ = "errorTxt") is not None:
            raise ValueError(soup.find(class_ = "errorTxt").text)

    d = d.find_all("div", class_ = "jp_departure_item")
    transports = []
    for i in d:
        raw = i.find_all(class_ = "jp_info")
        transports.append({
            "mode" : i.find(class_ = "jp_tmode").text.strip(),
            "type" : i.find("use").get("xlink:href").split("#")[-1],
            "direction" : raw[0].b.text.strip(),
            "scheduled_time" : raw[1].b.text.strip(),
            "estimated_time" : raw[2].b.text.strip(),
            "status" : raw[3].b.text.strip()
        })
    return transports