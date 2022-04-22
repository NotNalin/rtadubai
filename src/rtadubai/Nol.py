from bs4 import BeautifulSoup
import requests


captcha = "03AGdBq24OjYCEGdTLnTXbrCBkXqkRK-1CttobNTMZa-GTnJuu7PivfE1M73l2RJH2f8SD_YM7uh4ZDXU8tUlk_I36a0qJnYkVZHC_Lj1DLADiUe_KpCLTIegJhCO49aSeT6jfU2v3JH7diE-DSg_ZuECRXtHt7jeJMNHqhpY9EzsAKjueU4jDq3pnBcpfb0uavhULE_gZGSjG-iv4P_YTbWsHnHGsPNzSZeykEn3ToHMy0WtwNillGrqO6U5kqll22xsS"

# NOT TO BE USED IN YOUR CODE
# Used for getting data from www.rta.ae and parsing it into a BeautifulSoup object
# Type 1 is for getting balance and Type 2 is for getting transactions
# Used by other functions to reduce code


def soup(type, nol):
    if type == 1:
        url = "https://www.rta.ae/wps/portal/rta/ae/home/!ut/p/z1/04_Sj9CPykssy0xPLMnMz0vMAfIjo8zi_QwMTNwNTAx93EPNDAwcQ4MCA8O8gowNXMz1w_Wj9KNASgIMLTycDAx9DIxDnIBKAkO8Ai29PD0MjaEKDHAARwP94NQ8_YLs7DRHR0VFAE1hpMw!/p0/IZ7_KG402B82M83EB0Q64NN5ER3GR6=CZ6_N004G041LGU600AURQQVJR30D7=NJgetNolCardBalance=/"
        data = {
            'nolTagId': nol,
            'captchaResponse': captcha
        }
    elif type == 2:
        url = "https://www.rta.ae/wps/portal/rta/ae/public-transport/nol/view-history/!ut/p/z1/jY-9DoIwAISfhQcwvZZKylhEC-VPhEbsYhiMIVF0MD6_hsEBI3LbJd-X3BFLGmL79tmd20d369vLux-sd0wUBwsEy-CJDUqTLFeVxylij-xHwK7wIbUJ8zBnEIoTO8fPt1REAWgKtw4gTVnr0tdxRN15Pn5E4r9vR8j3gwHIAa7AaSqyYg1JdVQoVjKlP8DEhwGYGFmdenK_GtOgixfScV5YvGcI/p0/IZ7_KG402B82M068F0QUK5CS641067=CZ6_KG402B82M068F0QUK5CS6410I6=NJvalidateTag=/"
        data = {
            'tagId': nol,
            'captcha': captcha
        }
    return BeautifulSoup(requests.post(url, data=data).text, 'html.parser')


def isValid(nol):
    if soup(1, nol).find('b') is None:
        return True
    else:
        return False


def CardBalance(nol):
    response = soup(1, nol)
    if response.find('b') is None:
        bal = response.find('strong', class_='font-weight-bolder font-size-18')
        return bal.text
    return response.find("b").text


def Details(nol):
    response = soup(1, nol)
    r = response.find_all('strong', class_='font-weight-bolder font-size-18')
    if r is not None:
        return {
            'NolID': nol,
            'Error': False,
            'Card Balance': r[0].text + " AED",
            'Pending Balance': r[1].text + " AED",
            'Expiry Date': r[2].text
        }
    return {
        'Error': True,
        'ErrorMsg': response.find('b').text
    }


def Recent(nol, no=1):
    response = TransactionsRaw(nol)
    if type(response) is list:
        if no > len(response):
            return {
                "Error": True,
                "ErrorMsg": "Number given is greater than the number of transactions"
            }
        elif no <= 0:
            return {
                "Error": True,
                "ErrorMsg": "Invalid Number Given"
            }
        else:
            return response[no-1]
    return response


def TransactionsRaw(nol):
    response = soup(2, nol)
    if response.find(id='nolhasErr') is None:
        data = response.find_all('span', class_='DataList')
        Date = response.find_all(
            'div', class_='col col-lg-5 col-sm-5 col-md-5 vcenter col-xs-8 ss-table__col')
        noTransactions = int(len(Date)/2)
        ReturnList = []
        for i in range(noTransactions):
            ReturnList.append({
                "NolID": nol,
                "Error": False,
                "Date": Date[1+i*2].text.strip(),
                "Time": data[0+i*3].text,
                "Type": data[1+i*3].text,
                "Amount": data[2+i*3].text
            })
        return ReturnList
    return {
        "Error": True,
        "ErrorMsg": response.find(id='nolmsg')['value'].strip()
    }


def NoOfTransactions(nol):
    response = TransactionsRaw(nol)
    if type(response) is list:
        return len(response)
    return 0
