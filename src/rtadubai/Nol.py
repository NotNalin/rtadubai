from bs4 import BeautifulSoup
import requests


captcha = "03AGdBq24OjYCEGdTLnTXbrCBkXqkRK-1CttobNTMZa-GTnJuu7PivfE1M73l2RJH2f8SD_YM7uh4ZDXU8tUlk_I36a0qJnYkVZHC_Lj1DLADiUe_KpCLTIegJhCO49aSeT6jfU2v3JH7diE-DSg_ZuECRXtHt7jeJMNHqhpY9EzsAKjueU4jDq3pnBcpfb0uavhULE_gZGSjG-iv4P_YTbWsHnHGsPNzSZeykEn3ToHMy0WtwNillGrqO6U5kqll22xsS"

# NOT TO BE USED IN YOUR CODE
# Used for getting data from www.rta.ae and parsing it into a BeautifulSoup object
# Type 1 is for getting balance and Type 2 is for getting transactions
# Used by other functions to reduce code
def soup(type, nol):
    if type == 1:
        url = "https://www.rta.ae/wps/portal/rta/ae/public-transport/nol/nol-how/!ut/p/z1/jY_RCoIwGIWfxQeI_ZtD5uWWsbncbObKdhNeRAhlXUTPX3gRCGWeuwPfB-eggBoU-vbZndtHd-vby7sfQnJcSwpEMGJYni3BVcnOmFphJjDajwGoyhS49pnNLAEmKQpzfLvBTAnABcS1AO5drV2qc4XjeT78CIf_fhgjXx4MgAWgEigumClXwLFWpSSOSP0BJj4MwMTI7alH96v3DXT5gkfRC6bULQc!/p0/IZ7_KG402B82M8IDC0QR6VMMTH1O90=CZ6_KG402B82M8IDC0QR6VMMTH18B1=NJgetNolCardBalancePTA=/"
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
    if soup(1, nol).find('h4') is None:
        return True
    else:
        return False


def CardBalance(nol):
    response = soup(1, nol)
    if response.find('h4') is None: 
        bal = response.find('div', class_='d-block mt-lg-0')
        return bal.text
    return response.find("h4").text


def BalanceRaw(nol):
    response = soup(1, nol)
    if response.find('h4') is None: 
        bal = response.find_all('div', class_='d-block mt-lg-0')
        return {
            'NolID': nol,
            'Error': False,
            'ErrorMsg': "",
            'Card Balance': bal[0].text,
            'Pending Balance': bal[1].text,
            'Warning': response.find('h5').text
            }
    return {
        'Error': True,
        'ErrorMsg': response.find("h4").text
        }



def Recent(nol, no=1):
    response = TransactionsRaw(nol)
    if type(response) is list:
        if no > len(response):
            return {
                "Error" : True,
                "ErrorMsg" : "Number given is greater than the number of transactions"
            }
        elif no <= 0:
            return {
                "Error" : True,
                "ErrorMsg" : "Invalid Number Given"
            }
        else:
            return response[no-1]
    return response


def TransactionsRaw(nol):
    response = soup(2, nol)
    if response.find(id='nolhasErr') is None:
        data = response.find_all('span', class_='DataList')
        Date = response.find_all('div', class_='col col-lg-5 col-sm-5 col-md-5 vcenter col-xs-8 ss-table__col')
        noTransactions = int(len(Date)/2)
        ReturnList = []
        for i in range(noTransactions):
            ReturnList.append({
                "NolID": nol,
                "Error": False,
                "ErrorMsg": "",
                "Date" : Date[1+i*2].text.strip(),
                "Time" : data[0+i*3].text,
                "Type" : data[1+i*3].text,
                "Amount" : data[2+i*3].text
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
