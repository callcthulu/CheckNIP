import requests as r
import pandas as pd

#set proxy setting
ifproxy = 0
###File input
#NIPdf = pd.read_csv("C:/Users/oleli/Desktop/NIPlist.txt", names=["NIP"])
#NIPdf.insert(1,"RawVATUE",None)
###Test intput - comment for SQL Server
NipList = ["PL7630003498","PL8730006829","PT504220560","DE111628131","GB195929307"]
SQL_in = pd.DataFrame({"VATUE":NipList})
SQL_in.insert(1,"RawVATUE",None)
###SQL Server input
NIPdf = SQL_in
NIPdf.insert(2,"GateResponse",None)
NIPdf.insert(3, "GateTextResponse",None)
NIPdf.insert(4,"Response",None)
NIPdf.insert(5,"CompanyName",None)
NIPdf.insert(6,"CompanyAddress",None)
NIPdf.insert(7,"CompanyType",None)

#Send NIP and get response
url = "http://ec.europa.eu/taxation_customs/vies/services/checkVatService"
headers = {"content-type": "text/xml",
           "SOAPAction" : ""
           }
body = """ <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
            <s:Body>
                <checkVatApprox xmlns="urn:ec.europa.eu:taxud:vies:services:checkVat:types">
                <countryCode>%s</countryCode>
                <vatNumber>%s</vatNumber>
                </checkVatApprox>
             </s:Body>
            </s:Envelope>";

"""
if ifproxy:
    proxy ={"<past proxy here>"}
else:
    proxy = None

for n, vatUe in enumerate(NIPdf["VATUE"]):
    prefix = vatUe[0:2]
    NIP = vatUe[2:]
    response = r.post(url
                      ,data=(body % (prefix, NIP,))
                      ,headers=headers
                      , proxies=proxy
                      )
    NIPdf.at[n,"GateResponse"] = response.status_code #response http status code
    NIPdf.at[n,"GateTextResponse"] = r.status_codes._codes[response.status_code][0] #response http code description
    if response.status_code == 200:
        NIPdf.at[n, "Response"] = response.text.split("<valid>",1)[1].split("</valid>",1)[0]
        if "</traderName>" in response.text:
            NIPdf.at[n, "CompanyName"] = response.text.split("<traderName>", 1)[1].split("</traderName>", 1)[0]
        if "</traderAddress>" in response.text:
            NIPdf.at[n, "CompanyAddress"] = response.text.split("<traderAddress>", 1)[1].split("</traderAddress>", 1)[0]
        if "</traderCompanyType>" in response.text:
            NIPdf.at[n, "CompanyType"] = response.text.split("<traderCompanyType>", 1)[1].split("</traderCompanyType>", 1)[0]
        if NIPdf.at[n, "CompanyType"] == "---":
            NIPdf.at[n, "CompanyType"] = None

###SQL Server oputput
SQL_out = NIPdf
###print output
#print(NIPdf.head())
