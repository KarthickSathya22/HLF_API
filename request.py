"""
Input Description:
------------------

I.  Field           Value   Placeholder

1.  MARITAL STATUS	2750	MARRIED
    MARITAL STATUS	2751	UNMARRIED
    
2.  No of dependants.

3.  TYPE OF RESIDENCE	2755	OWN
    TYPE OF RESIDENCE	2756	RENTED/LEASED
    
4.  Number of staying year in current residence.

5.  Borrowers Property Value.

6.  PRODUCT CATEGORY    1784    LOAN AGAINST PROPERTY
    PRODUCT CATEGORY    926     CAR
    PRODUCT CATEGORY    912     MULTI UTILITY VEHICLE
    PRODUCT CATEGORY    945     VIKRAM
    PRODUCT CATEGORY    1402    TRACTOR
    PRODUCT CATEGORY    1373    USED VEHICLES
    PRODUCT CATEGORY    1672    TIPPER
    PRODUCT CATEGORY    1664    FARM EQUIPMENT
    PRODUCT CATEGORY    1541    TWO WHEELER
    PRODUCT CATEGORY    634     INTERMEDIATE COMMERCIAL VEHICLE
    PRODUCT CATEGORY    527     HEAVY COMMERCIAL VEHICLE
    PRODUCT CATEGORY    528     CONSTRUCTION EQUIPMENTS
    PRODUCT CATEGORY    529     THREE WHEELERS
    PRODUCT CATEGORY    530     LIGHT COMMERCIAL VEHICLES
    PRODUCT CATEGORY    531     SMALL COMMERCIAL VEHICLE
    PRODUCT CATEGORY    738     MEDIUM COMMERCIAL VEHICLE
    PRODUCT CATEGORY    783     BUSES

7. Brand    1       Others
   Brand    1360    HONDA
   Brand    1542    HERO
   Brand    1544    HMSI
   Brand    1547    YAMAHA
   Brand    1546    SUZUKI
   Brand    1647    TVS
   Brand    1549    ROYAL ENFIELD
   
8. Industry Type    1782    SALARIED
   Industry Type    1783    SELF EMPLOYEED
   Industry Type    603     AGRICULTURE
   Industry Type    604     PASSENGER TRANSPORTATION
   Industry Type    605     CONSTRUCTION
   Industry Type    875     INFRASTRUCTURE
   Industry Type    876     CEMENT
   Industry Type    877     OIL AND GAS
   Industry Type    878     GOVERNMENT CONTRACT
   Industry Type    879     OTHERS
   Industry Type    658     MINE

9. Tenure Count.

10. Installment Count.

11. Vehicle Price.

12. Initial Payment Amount.

13. Interest Amount.

14. Monthly Total Inflow.

15. HLF Score.

16. Borrower's Age.

17. Banking Period Detail   0     New Account
    Banking Period Detail   2     <3 Month Old
    Banking Period Detail   4     >3 Month Old
    Banking Period Detail   7     >6 Month Old

18. Employment Stability    1   Salaried with over 1 year
    Employment Stability    2   Salaried with over 6 Months
    Employment Stability    3   Salaried less than 6 Months
    

19. Geo Limit   1     Less than 15 Km
    Geo Limit   2     More than 15 Km

20. Gender  M    Male
    Gender  F    Female
    
21. File (Uploading Bank Statement to get average closing balance).

22. cibil (XMl Statement to get Cibil Score).
"""

#Importing Libraries:
import requests

#Rest-API URL:
#url = "http://127.0.0.1:5000/predict_tw_api"
url = "https://hlf-api.herokuapp.com/predict_tw_api"

#Parameters of Request or (Input to the prediction model):
payload = {
    "martial_status": "2750",
    "dependants": "1",
    "residence": "2755",
    "staying_year": "10",
    "assetvalue": "150000",
    "productcat": "926",
    "brand": "1360",
    "industrytype": "1782",
    "tenure": "12",
    "instalcount": "12",
    "chasasset": "80000",
    "chasinitial": "20000",
    "finaninterest": "13",
    "totinflow": "12000",
    "score": "800",
    "age": "30",
    "bank_detail": "2",
    "stability": "2",
    "geo": "1",
    "gender": "M",
    "pan": "AHFHOFJPFJOI3",
    "clobal": "10200",
    "cibil": "900"
}

#Uploading Bank Statement and XMl Statement:
files = [
  ('file', open('C:/Users/ESFITA-USER/Bank Statement Analysis/60426339_1585958532965.pdf','rb')),
  ('cibil', open('C:/Users/ESFITA-USER/Cibil/Downloads/PJ00039769.xml','rb'))
]

#Post request to the URL: 
response = requests.request("POST", url,data = payload, files = files).json()

#Printing response:
print(response)