import requests

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
        i = i["StopLocation"]
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


print(Stop("Al Ghubaiba").__dict__)
