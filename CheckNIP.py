import requests as r
import pandas as pd

#set proxy setting
ifproxy = 0
###File connector -comment for SQL Server Connector
#SQL_in = pd.read_csv("C:/Users/oleli/Desktop/NIPlist.txt", names=["NIP"])
###Test
NipList = ["7630003498","8730006829","1111111111"]
SQL_in = pd.DataFrame({"NIP":NipList})
###Common:
SQL_in.insert(1,"RawNIP",None)
###SQL Server:
NIPdf = SQL_in
NIPdf.insert(2,"GateResponse",None)
NIPdf.insert(3, "GateTextResponse",None)
NIPdf.insert(4,"MFResponse",None)
NIPdf.insert(5,"MFTextResponse",None)

#Send NIP and get response
url = "https://sprawdz-status-vat.mf.gov.pl"
headers = {"content-type": "text/xml",
           "SOAPAction" : "http://www.mf.gov.pl/uslugiBiznesowe/uslugiDomenowe/AP/WeryfikacjaVAT/2018/03/01/WeryfikacjaVAT/SprawdzNIP"
           }
body = """ <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                xmlns:ns="http://www.mf.gov.pl/uslugiBiznesowe/uslugiDomenowe/AP/WeryfikacjaVAT/2018/03/01">
                 <soapenv:Header/>
                 <soapenv:Body>
                 <ns:NIP>%s</ns:NIP>
                 </soapenv:Body>
                </soapenv:Envelope>
"""
if ifproxy:
    proxy ={"<past proxy here>"}
else:
    proxy = None

for n, NIP in enumerate(NIPdf["NIP"]):
    response = r.get(url
                      ,data=(body % (NIP,))
                      ,headers=headers
					  ,proxies=proxy
                      )
    NIPdf.at[n,"GateResponse"] = response.status_code #response http status code
    NIPdf.at[n,"GateTextResponse"] = r.status_codes._codes[response.status_code][0] #response http code description
    if response.status_code == 200:
        NIPdf.at[n, "MFResponse"] = response.text.split("<Kod>",1)[1].split("</Kod",1)[0] #response letter from mf gate
        NIPdf.at[n, "MFTextResponse"] = response.text.split("<Komunikat>",1)[1].split("</Komunikat",1)[0] #response text from mf gate

###SQL Server output
#SQL_out = NIPdf
###print output
print(NIPdf["MFTextResponse"].str.slice(45,100,1))