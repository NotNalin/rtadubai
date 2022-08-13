import datetime

import requests
from bs4 import BeautifulSoup

from . import rta_captcha


URL = "https://www.rta.ae/wps/portal/rta/ae/home/!ut/p/z1/04_Sj9CPykssy0xPLMnMz0vMAfIjo8zi_QwMTNwNTAx93EPNDAwcQ4MCA8O8gowNXMz1w_Wj9KNASgIMLTycDAx9DIxDnIBKAkO8Ai29PD0MjaEKDHAARwP94NQ8_YLs7DRHR0VFAE1hpMw!/p0/IZ7_KG402B82M83EB0Q64NN5ER3GR6=CZ6_N004G041LGU600AURQQVJR30D7"

dubai_code = {'A': 11, 'B': 12, 'C': 13, 'D': 14, 'E': 15, 'F': 16, 'G': 17, 'H': 18, 'I': 19, 'J': 20, 'K': 21, 'L': 22, 'M': 23,
              'N': 63, 'O': 64, 'P': 65, 'Q': 66, 'R': 67, 'S': 68, 'T': 69, 'U': 70, 'V': 71, 'W': 72, 'X': 73, 'Y': 74, 'Z': 75,
              'AA': 86}


def soup(r):
    return BeautifulSoup(r.text, "html.parser")


def expiry(plate):
    if plate[0].isalpha() and len(plate) <= 6:
        plate_code = plate[0]
        plate_no = plate[1:]
    elif plate[0].isalpha() and plate[1].isalpha() and len(plate) <= 7:
        plate_code = plate[0:2]
        plate_no = plate[2:]

    data = {"plateCode": plate_code.upper(), "plateNo": plate_no, "captchaResponse": rta_captcha.CAPTCHA}
    response = soup(requests.post(URL + "=NJgetVehicleDetails=/", data=data))
    date = response.find("strong", class_="font-weight-bolder font-size-18")
    if date is None:
        return response.find("b").text
    return datetime.datetime.date(datetime.datetime.strptime(date.text, "%d-%B-%Y")).strftime("%d/%m/%Y")


def balance_plate(plate, number, *, AreaCode=1, PlateType=1):

    if number.startswith("+971"):
        number = number[4:]
    elif number.startswith("971"):
        number = number[3:]
    elif number.startswith("00971"):
        number = number[5:]
    elif number.startswith("05"):
        number = number[1:]

    if PlateType == 1:
        if AreaCode == 1:
            if plate[0].isalpha() and len(plate) <= 6:
                plate_code = plate[0]
                plate_no = plate[1:]
            elif plate[0].isalpha() and plate[1].isalpha() and len(plate) <= 7:
                plate_code = plate[0:2]
                plate_no = plate[2:]

            if plate_code.upper() in dubai_code:
                plate_code = dubai_code[plate_code.upper()]

    data = {
        "PlateSourceId": AreaCode,
        "PlateCategoryId": PlateType,
        "PlateColorId": plate_code,
        "PlateNumber": plate_no,
        "PlateCountry": "AE",
        "MobileCountryCode": "971",
        "MobileNumber": number,
        "language": "en"
    }
    response = requests.post("https://www.salik.rta.ae/surface/financial/balanceenquiry", data=data).json()
    if response["Valid"]:
        return response["SalikCredit"]
    else:
        return response['response']


# Havent tested this yet
def balance_account(account, pin):
    data = {
        "salikSearchType": "AccountAndPin",
        "salikAccountNo": account,
        "salikPin": pin,
        "captchaResponse": rta_captcha.CAPTCHA,
    }
    response = soup(requests.post(URL + "=NJgetSalikBalance=/", data=data))
    balance = response.find("strong", class_="font-weight-bolder font-size-18")
    if balance is None:
        return response.find("b").text
    return balance.text[:-2]
