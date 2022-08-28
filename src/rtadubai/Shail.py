from datetime import datetime, timedelta, timezone
import requests
import json
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


def departures(stop: Stop):
    data = {
        "departureLine": stop.name,
        "departureStateless": stop.id,
        "departureCoords": stop.coords,
    }
    response = requests.post(URL + "NJdepartureBoardShailRev=/", data=data)
    soup = BeautifulSoup(response.text, "html.parser")

    d = soup.find(class_="jp_departure_result")
    if d is None:
        if soup.find(class_="errorTxt") is not None:
            raise ValueError(soup.find(class_="errorTxt").text)

    d = d.find_all("div", class_="jp_departure_item")
    transports = []
    for i in d:
        raw = i.find_all(class_="jp_info")
        transports.append(
            {
                "mode": i.find(class_="jp_tmode").text.strip(),
                "type": i.find("use").get("xlink:href").split("#")[-1],
                "direction": raw[0].b.text.strip(),
                "scheduled_time": raw[1].b.text.strip(),
                "estimated_time": raw[2].b.text.strip(),
                "status": raw[3].b.text.strip(),
            }
        )
    return transports


def journey_planner(
    fromstop: Stop,
    tostop: Stop,
    time=datetime.now(timezone(timedelta(hours=4))),
    *,
    depart_or_arrive="D",
    metro=True,
    bus=True,
    tram=True,
    waterbus=True,
    avoidchanges=False,
):

    if depart_or_arrive not in ["D", "A"]:
        raise ValueError("depart_or_arrive must be either D or A")
    

    data = {
        "origin": fromstop.name,
        "originStateless": fromstop.id,
        "originCoords": fromstop.coords,
        "destination": tostop.name,
        "destinationStateless": tostop.id,
        "destinationCoords": tostop.coords,
        "departing": time.strftime("%d/%m/%Y %I:%M %p"),
        "departorarrive": depart_or_arrive,
        "jp_plan_dl_depart_hour": time.strftime("%I"),
        "jp_plan_dl_depart_min": time.strftime("%M"),
        "jp_plan_dl_depart_merd": time.strftime("%p"),
        "jp_plan_dl_arrive_hour": time.strftime("%I"),
        "jp_plan_dl_arrive_min": time.strftime("%M"),
        "jp_plan_dl_arrive_merd": time.strftime("%p"),
    }
    if metro:
        data["metro"] = "metro"
    if bus:
        data["bus"] = "bus"
    if tram:
        data["tram"] = "tram"
    if waterbus:
        data["waterbus"] = "waterbus"
    if avoidchanges:
        data["avoidchanges"] = "avoidchanges"

    response = requests.post(URL + "NJfindTripShailRev=/", data=data)
    soup = BeautifulSoup(response.text, "html.parser")
    raw = soup.find(class_="jp_container_results")
    jps = raw.find_all(class_="jp_container_result")
    journeys = []
    for i in jps:
        times = []
        stops = []
        methods = []
        modes = []
        durations = []
        for j in i.find_all("li"):
            time_ = j.find(class_="jp_row").b.text.strip()
            stop = j.find(class_="jp_tmode_station").text.strip()
            try:
                method = j.find(class_="icon").get("xlink:href").split("#")[-1]
            except AttributeError:
                method = None
            try:
                mode = j.find(class_="jp_tmode").b.text.strip()
            except AttributeError:
                if method == "walk":
                    mode = "walk"
                else:
                    mode = None
            try:
                duration = j.find(class_="jp_duration").text.strip()
            except AttributeError:
                duration = None
            times.append(time_)
            stops.append(stop)
            if method:
                methods.append(method)
            if mode:
                modes.append(mode)
            if duration:
                durations.append(duration)
        starttime = times.pop(0)
        startstop = stops.pop(0)
        d = i.find(class_="jp_more_info").find_all("b")
        duration, amount, starttime, endtime = [k.text.strip() for k in d]
        jp = []
        for j in range(len(times)):
            jp.append({
                "time": times[j],
                "stop": stops[j],
                "method": methods[j],
                "mode": modes[j],
                "duration": durations[j],
            })
        journeys.append({
            "starttime": starttime,
            "endtime": endtime,
            "startstop": startstop,
            "duration": duration,
            "amount": amount,
            "journeys": jp
        })
    return journeys


# a = journey_planner(Stop("Rashidiya bus station"), Stop("Al gubhaibha bus station"))
# print(json.dumps(a[0], indent=4))
