import datetime

import requests
from bs4 import BeautifulSoup

import rtadubai.rta_captcha as rta_captcha

URL = "https://www.rta.ae/wps/portal/rta/ae/home/!ut/p/z1/04_Sj9CPykssy0xPLMnMz0vMAfIjo8zi_QwMTNwNTAx93EPNDAwcQ4MCA8O8gowNXMz1w_Wj9KNASgIMLTycDAx9DIxDnIBKAkO8Ai29PD0MjaEKDHAARwP94NQ8_YLs7DRHR0VFAE1hpMw!/p0/IZ7_KG402B82M83EB0Q64NN5ER3GR6=CZ6_N004G041LGU600AURQQVJR30D7"


DUBAI_CODE = {
    'A': 11, 'B': 12, 'C': 13, 'D': 14, 'E': 15, 'F': 16, 'G': 17, 'H': 18, 'I': 19, 'J': 20, 'K': 21, 'L': 22, 'M': 23,
    'N': 63, 'O': 64, 'P': 65, 'Q': 66, 'R': 67, 'S': 68, 'T': 69, 'U': 70, 'V': 71, 'W': 72, 'X': 73, 'Y': 74, 'Z': 75,
    'AA': 86, 'CR': 89, 'WHITE': 5
}

ABUDHABI_CODE = {
    '1': 36, '2': 76, '3': 77, '4': 49, '5': 10, '6': 41, '7': 42, '8': 43, '9': 44, '10': 45, '11': 46, '12': 78,
    '13': 79, '14': 80, '15': 81, '16': 82, '17': 84, '18': 88, '50': 85,
    'RED': 1, 'GREEN': 2, 'BLUE': 3, 'GRAY': 4
}

SHARJAH_CODE = {
    '0': 5, '1': 25, '2': 26, '3': 83,
    'WHITE': 5, 'ORANGE': 6, 'BROWN': 24, '': 5
}

AJMAN_CODE = {
    'A': 11, 'B': 12, 'C': 13, 'D': 14, 'E': 15, 'F': 16, 'H': 18, 'K': 21,
    'WHITE': 5, 'ORANGE': 6
}

UAQ_CODE = {
    'A': 11, 'B': 12, 'C': 13, 'D': 14, 'E': 15, 'F': 16, 'G': 17, 'H': 18, 'I': 19, 'J': 20, 'K': 21, 'L': 22, 'M': 23,
    'X': 73, 'WHITE': 5
}

RAK_CODE = {
    'A': 11, 'B': 12, 'C': 13, 'D': 14, 'I': 19, 'K': 21, 'M': 23, 'N': 63, 'S': 68, 'V': 71, 'X': 73, 'Y': 74, 'Z': 75,
    'WHITE': 5, 'BLACK': 7, 'CLASSIC': 87, 'QALA': 7
}

FUJAIRAH_CODE = {
    'A': 11, 'B': 12, 'C': 13, 'D': 14, 'E': 15, 'F': 16, 'G': 17, 'H': 18, 'I': 19, 'J': 20, 'K': 21, 'L': 22, 'M': 23,
    'O': 64, 'P': 65, 'R': 67, 'S': 68, 'T': 69, 'V': 71, 'X': 73, 'Z': 75,
    'WHITE': 5
}

AREA_CODES = {
    1: DUBAI_CODE,
    2: ABUDHABI_CODE,
    3: SHARJAH_CODE,
    4: AJMAN_CODE,
    5: UAQ_CODE,
    6: RAK_CODE,
    7: FUJAIRAH_CODE
}

class Plates:
    dubai = list(DUBAI_CODE)
    abudhabi = list(ABUDHABI_CODE)
    sharjah = list(SHARJAH_CODE)
    ajman = list(AJMAN_CODE)
    uaq = list(UAQ_CODE)
    rak = list(RAK_CODE)
    fujairah = list(FUJAIRAH_CODE)

AREAS = {
    1: 'Dubai',
    2: 'Abu Dhabi',
    3: 'Sharjah',
    4: 'Ajman',
    5: 'Umm Al Quwain',
    6: 'Ras Al Khaimah',
    7: 'Fujairah'
}

def plates(area):
    int(area)
    if area in AREA_CODES:
        return list(AREA_CODES[area])
    else:
        raise ValueError('Invalid Area Code')

def expiry(plate):
    if plate[0].isalpha() and len(plate) <= 6:
        plate_code = plate[0]
        plate_no = plate[1:]
    elif plate[0].isalpha() and plate[1].isalpha() and len(plate) <= 7:
        plate_code = plate[0:2]
        plate_no = plate[2:]

    data = {"plateCode": plate_code.upper(), "plateNo": plate_no, "captchaResponse": rta_captcha.CAPTCHA}
    r = requests.post(URL + "=NJgetVehicleDetails=/", data=data)
    response = BeautifulSoup(r.text, "html.parser")
    date = response.find("strong", class_="font-weight-bolder font-size-18")
    if date is None:
        raise ValueError(response.find("b").text)
    return datetime.datetime.date(datetime.datetime.strptime(date.text, "%d-%B-%Y")).strftime("%d/%m/%Y")


def balance_plate(plate, number):
    if number.startswith("+971"):
        number = number[4:]
    elif number.startswith("971"):
        number = number[3:]
    elif number.startswith("00971"):
        number = number[5:]
    elif number.startswith("05"):
        number = number[1:]

    if plate[0].isalpha() and len(plate) <= 6:
        plate_code = plate[0]
        plate_no = plate[1:]
    elif plate[0].isalpha() and plate[1].isalpha() and len(plate) <= 7:
        plate_code = plate[0:2]
        plate_no = plate[2:]

    if plate_code.upper() in DUBAI_CODE:
        plate_code = DUBAI_CODE[plate_code.upper()]

    data = {
        "salikSearchType": "MobileAndPlate",
        "salikPlateCode": plate_code,
        "salikPlateNo": plate_no,
        "salikMobileCountryCode": "971",
        "salikMobileNo": number,
        "captchaResponse": rta_captcha.CAPTCHA,
    }
    r = requests.post(URL + "=NJgetSalikBalance=/", data=data)
    response = BeautifulSoup(r.text, "html.parser")
    balance = response.find("strong", class_="font-weight-bolder font-size-18")
    if balance is None:
        raise ValueError(response.find("b").text)
    return balance.text[:-2]


def balance_account(account, pin):
    data = {
        "salikSearchType": "AccountAndPin",
        "salikAccountNo": account,
        "salikPinNo": pin,
        "captchaResponse": rta_captcha.CAPTCHA,
    }
    r = requests.post(URL + "=NJgetSalikBalance=/", data=data)
    response = BeautifulSoup(r.text, "html.parser")
    balance = response.find("strong", class_="font-weight-bolder font-size-18")
    if balance is None:
        raise ValueError(response.find("b").text)
    return balance.text[:-2]


def balance(code, number, mobile_number, *, area=1):
    mobile_number = str(mobile_number)
    if mobile_number.startswith("+971"):
        mobile_number = mobile_number[4:]
    elif mobile_number.startswith("971"):
        mobile_number = mobile_number[3:]
    elif mobile_number.startswith("00971"):
        mobile_number = mobile_number[5:]
    elif mobile_number.startswith("05"):
        mobile_number = mobile_number[1:]

    if not mobile_number.startswith("5") or len(mobile_number) != 9:
        raise ValueError("Invalid mobile number")

    if area not in AREA_CODES:
        raise ValueError("Invalid area code")

    if not code.upper() in AREA_CODES[area]:
        raise ValueError("Invalid plate code")
    else:
        code = AREA_CODES[area][code.upper()]

    data = {
        "PlateSourceId": area,
        "PlateCategoryId": 1,
        "PlateColorId": code,
        "PlateNumber": number,
        "PlateCountry": "AE",
        "MobileCountryCode": "971",
        "MobileNumber": mobile_number,
        "language": "en",
    }
    response = requests.post("https://www.salik.ae/surface/financial/balanceenquiry", data=data).json()
    if response["Valid"]:
        return response["SalikCredit"]
    else:
        try:
            raise ValueError(response["BusinessErrorMessage"])
        except KeyError:
            raise ValueError("Unknown error occurred\n Plase make an issue on https://github.com/NotNalin/rtadubai/issues")
