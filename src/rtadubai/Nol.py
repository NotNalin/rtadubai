import requests
from bs4 import BeautifulSoup

import rtadubai.rta_captcha as rta_captcha

URL_DETAILS = "https://www.rta.ae/wps/portal/rta/ae/home/!ut/p/z1/04_Sj9CPykssy0xPLMnMz0vMAfIjo8zi_QwMTNwNTAx93EPNDAwcQ4MCA8O8gowNXMz1w_Wj9KNASgIMLTycDAx9DIxDnIBKAkO8Ai29PD0MjaEKDHAARwP94NQ8_YLs7DRHR0VFAE1hpMw!/p0/IZ7_KG402B82MGIF8066PQMJDP1OK2=CZ6_N004G041LGU600AURQQVJR30D7=NJgetNolCardBalance=/"
URL_TRANSACTIONS = "https://www.rta.ae/wps/portal/rta/ae/public-transport/nol/view-history/!ut/p/z1/jY-9DoIwAISfhQcwvZZKylhEC-VPhEbsYhiMIVF0MD6_hsEBI3LbJd-X3BFLGmL79tmd20d369vLux-sd0wUBwsEy-CJDUqTLFeVxylij-xHwK7wIbUJ8zBnEIoTO8fPt1REAWgKtw4gTVnr0tdxRN15Pn5E4r9vR8j3gwHIAa7AaSqyYg1JdVQoVjKlP8DEhwGYGFmdenK_GtOgixfScV5YvGcI/p0/IZ7_KG402B82M068F0QUK5CS641067=CZ6_KG402B82M068F0QUK5CS6410I6=NJvalidateTag=/"


def isvalid(nol):
    nol = str(nol).replace(" ", "").strip()
    data = {"nolTagId": nol, "captchaResponse": rta_captcha.CAPTCHA}
    response = BeautifulSoup(requests.post(URL_DETAILS, data=data, headers=rta_captcha.HEADERS).text, "html.parser")
    if response.find("b") is None:
        return True
    else:
        return False


def balance(nol):
    nol = str(nol).replace(" ", "").strip()
    data = {"nolTagId": nol, "captchaResponse": rta_captcha.CAPTCHA}
    response = BeautifulSoup(requests.post(URL_DETAILS, data=data, headers=rta_captcha.HEADERS).text, "html.parser")
    if response.find("b") is None:
        bal = response.find("strong", class_="font-weight-bolder font-size-18")
        return bal.text
    raise ValueError(response.find("b").text)


def details(nol):
    nol = str(nol).replace(" ", "").strip()
    data = {"nolTagId": nol, "captchaResponse": rta_captcha.CAPTCHA}
    response = BeautifulSoup(requests.post(URL_DETAILS, data=data, headers=rta_captcha.HEADERS).text, "html.parser")
    r = response.find_all("strong", class_="font-weight-bolder font-size-18")
    if len(r) != 0:
        return {
            "id": nol,
            "balance": r[0].text,
            "pending": r[1].text,
            "expiry": r[2].text,
        }
    raise ValueError(response.find("b").text)


def recent(nol, no=1):
    response = transactions(nol)
    if len(response) == 0:
        raise ValueError("No transactions found")
    elif no > len(response):
        raise ValueError("Number given is greater than the number of transactions")
    elif no <= 0:
        raise ValueError("Invalid Number Given")
    else:
        return response[no - 1]


def transactions(nol):
    nol = str(nol).replace(" ", "").strip()
    data = {"tagId": nol, "captcha": rta_captcha.CAPTCHA}
    response = BeautifulSoup(requests.post(URL_TRANSACTIONS, data=data, headers=rta_captcha.HEADERS).text, "html.parser")

    if response.find(id="nolhasErr") is None:
        data = response.find_all("span", class_="DataList")
        date = response.find_all("div", class_="col col-lg-5 col-sm-5 col-md-5 vcenter col-xs-8 ss-table__col")
        no_transactions = int(len(date) / 2)
        transactions = []
        for i in range(no_transactions):
            transactions.append(
                {
                    "id": nol,
                    "date": date[1 + i * 2].text.strip(),
                    "time": data[0 + i * 3].text,
                    "type": data[1 + i * 3].text,
                    "amount": data[2 + i * 3].text,
                }
            )
        return transactions

    error = response.find(id="nolmsg")["value"].strip()
    if error == "No transaction found":
        return []
    else:
        raise ValueError(error)


class Card:
    def __init__(self, nol):
        if isvalid(nol):
            data = details(nol)
            self.id = data["id"]
            self.balance = data["balance"]
            self.pending = data["pending"]
            self.expiry = data["expiry"]
        else:
            raise ValueError("Invalid Nol Card")

    def __repr__(self):
        return f"Nol Card : {self.id}"

    def update(self):
        data = details(self.id)
        self.balance = data["balance"]
        self.pending = data["pending"]

    def transactions(self):
        return transactions(self.id)

    def recent(self, no=1):
        return recent(self.id, no)
