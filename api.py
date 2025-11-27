import requests
from dotenv import load_dotenv
import os
from datetime import datetime
from lxml import html

def getHeaders():
    cookie = os.getenv("cookie")
    headers = {
        "Cookie": f"ABCBourse={cookie}",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
    }
    return headers

def buyAction(quantity : int, id : str):
    url = "https://abcbourse.com/api/portfolio/sendOrderOpen"
    load_dotenv()
    portifID = os.getenv("portifID")
    today_date = datetime.today().strftime('%d/%m/%Y')

    payload = {
        "portifID": portifID,
        "qty": str(quantity),
        "orderQuote": "0",
        "orderDate": today_date,
        "sens": "buy",
        "shortID": id,
        "type": "mkt"
    }
    response = requests.post(url, json=payload, headers=getHeaders())
    
    if response.status_code == 200:
        print("Request successful:", response.json())
    else:
        print("Request failed with status code:", response.status_code)
    
def getInfo() -> int:
    response = requests.get("https://abcbourse.com/cotation/AFp", headers=getHeaders())
    if response.status_code == 200:
        tree = html.fromstring(response.content)
        value = tree.xpath('//*[@id="lastcx"]/text()')[0]
        print(value)
    else:
        print("Request failed with status code:", response.status_code)
    
    
def sellAction(quantity : int, idLign : str):
    url = "https://abcbourse.com/api/portfolio/sendOrder"
    load_dotenv()
    portifID = os.getenv("portifID")
    today_date = datetime.today().strftime('%d/%m/%Y')
    payload = {
        "portifID": portifID,
        "qty": str(quantity),
        "orderQuote": "0",
        "orderDate": today_date,
        "idLign": idLign,
        "type": "mkt"
    }
    response = requests.post(url, json=payload, headers=getHeaders())
    
    if response.status_code == 200:
        print("Request successful:", response.json())
    else:
        print("Request failed with status code:", response.status_code)

def getPortefeuille():
    load_dotenv()
    portifID = os.getenv("portifID")
    headers = getHeaders()
    headers["Referer"] = f"https://abcbourse.com/portif/displayp?n={portifID}"
    response = requests.get(f"https://abcbourse.com/api/portfolio/GetPortifFull?portifID={portifID}", headers=headers)
    if response.status_code == 200:
        return response.json()
    print("Request failed with status code:", response.status_code)
    return {}

def getCompany(search):
    companies = getAllCompanies()
    for c in companies:
        ok = True
        for k in search.keys():
            if c[k] != search[k]:
                ok = False
        if ok:
            return c
    return {}

def getCompaniesList(compartiment : str, letter : str):
    headers = getHeaders()
    headers["Referer"] = f"https://abcbourse.com/marches/cotation_eurolist{compartiment}"
    response = requests.get(f"https://abcbourse.com/api/general/GetMarket?marketN=eurolist{compartiment}p&letter={letter}", headers=headers)
    if response.status_code == 200:
        return response.json()['qitem']
    print("Request failed with status code:", response.status_code)
    return []

def getAllCompanies():
    companies = []
    companies += getCompaniesList('a','Ac')
    companies += getCompaniesList('a','Ei')
    companies += getCompaniesList('a','Ne')
    companies += getCompaniesList('a','Th')
    companies += getCompaniesList('b','74')
    companies += getCompaniesList('b','Fi')
    companies += getCompaniesList('b','Ro')
    companies += getCompaniesList('c','Ab')
    companies += getCompaniesList('c','Cr')
    companies += getCompaniesList('c','Pa')
    return companies
    

if __name__ == "__main__":
    # buyAction(10, "AFp")
    # sellAction(10, "2398073")
    getInfo()
    getPortefeuille()
    print(getAllCompanies())
    print(getCompany({'id':'VANTIp'}))
    