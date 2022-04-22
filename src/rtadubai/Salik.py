import requests
import datetime
from bs4 import BeautifulSoup

captcha = "03AGdBq24OjYCEGdTLnTXbrCBkXqkRK-1CttobNTMZa-GTnJuu7PivfE1M73l2RJH2f8SD_YM7uh4ZDXU8tUlk_I36a0qJnYkVZHC_Lj1DLADiUe_KpCLTIegJhCO49aSeT6jfU2v3JH7diE-DSg_ZuECRXtHt7jeJMNHqhpY9EzsAKjueU4jDq3pnBcpfb0uavhULE_gZGSjG-iv4P_YTbWsHnHGsPNzSZeykEn3ToHMy0WtwNillGrqO6U5kqll22xsS"
url = 'https://www.rta.ae/wps/portal/rta/ae/home/!ut/p/z1/04_Sj9CPykssy0xPLMnMz0vMAfIjo8zi_QwMTNwNTAx93EPNDAwcQ4MCA8O8gowNXMz1w_Wj9KNASgIMLTycDAx9DIxDnIBKAkO8Ai29PD0MjaEKDHAARwP94NQ8_YLs7DRHR0VFAE1hpMw!/p0/IZ7_KG402B82M83EB0Q64NN5ER3GR6=CZ6_N004G041LGU600AURQQVJR30D7=NJgetVehicleDetails=/'


def soup(r):
    return BeautifulSoup(r.text, 'html.parser')


def Expiry(plate):
    if plate[0].isalpha() and len(plate) <= 6:
        plate_code = plate[0]
        plate_no = plate[1:]
    elif plate[0].isalpha() and plate[1].isalpha() and len(plate) <= 7:
        plate_code = plate[0:2]
        plate_no = plate[2:]

    data = {
        'plateCode': plate_code,
        'plateNo': plate_no,
        'captchaResponse': captcha
    }
    response = soup(requests.post(url, data=data))
    date = response.find(
        'strong', class_='font-weight-bolder font-size-18')
    if date is None:
        return response.find('b').text
    return datetime.datetime.date(datetime.datetime.strptime(date.text, '%d-%B-%Y')).strftime('%d/%m/%Y')
