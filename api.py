# -*- coding: utf-8 -*-
"""
Created on Tue May 19 17:14:55 2020
@author: ESFITA-USER
"""
"""
#Two Wheeler Input Data:
In cibil we need to upload xml file.
In clobal we need to Bank Statement.
{
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
#Commercial Vehicle:
{
    "martial_status": "2750",
    "dependants": "1",
    "residence": "2755",
    "staying_year": "10",
    "profile": "2693",
    "segment": "2693",
    "market_load": "566",
    "tot_years": "10",
    "asset": "150000",
    "productcat": "926",
    "brand": "564",
    "industrytype": "1782",
    "tenure": "12",
    "instalcount": "12",
    "chasasset": "80000",
    "chasinitial": "20000",
    "finaninterest": "13",
    "availed_loan": "0",
    "totincome": "12000",
    "totexpense": "100",
    "score": "800",
    "vehicle": "1",
    "vehicle_age": "0",
    "age": "30",
    "od": "1000",
    "bank_period":"1",
    "bank_detail": "2",
    "stability": "2",
    "fleet": "7",
    "gender": "M",
    "pan": "AHFHOFJPFJOI3",
    "clobal": "10200",
    "cibil": "900"
}
"""
# Importing Libraries:
import pandas as pd
import dateutil
import datetime
import tabula
import numpy as np
from flask import Flask, request,jsonify,Response
import pickle

app = Flask(__name__)

#Loading a model:
model_tw = pickle.load(open('model_tw_iso.pkl', 'rb'))
model_tw_ntc = pickle.load(open('model_tw_ntc_sig.pkl', 'rb'))
model_cv = pickle.load(open('model_cv_iso.pkl', 'rb'))
model_scv = pickle.load(open('model_scv_iso.pkl', 'rb'))

@app.route('/predict_tw_api',methods=['POST','GET'])
def predict_tw():
    '''
    For rendering results on HTML GUI
    '''
    predict_request = []
    res = []
    
    status = request.json["martial_status"]
    married = {2750:"Married",2751:"Un Married"}
    predict_request.append(status)
    res.append(married.get(int(status)))
    
    dep = request.json["dependants"]
    predict_request.append(dep)
    res.append(dep)
    
    resi = request.json["residence"]
    residence = {2755:"Own",2756:"Rent"}
    predict_request.append(resi)
    res.append(residence.get(int(resi)))
    
    year = request.json["staying_year"]
    predict_request.append(year)
    res.append(year)
    
    #Uploading Bank Stmt file:
    file = request.json['clobal']
    clobal =  float(file)
    predict_request.append(clobal)
    res.append(clobal)

    asset = request.json["assetvalue"]
    predict_request.append(float(asset))
    res.append("{:,}".format(float(asset)))
    
    cat = request.json["productcat"]
    prod_cat = {1784:"LOAN AGAINST PROPERTY",
            926:"CAR",
            912:"MULTI UTILITY VEHICLE",
            945:"VIKRAM",
            1402:"TRACTOR",
            1373:"USED VEHICLES",
            1672:"TIPPER",
            1664:"FARM EQUIPMENT",
            1541:"TWO WHEELER",
            634:"INTERMEDIATE COMMERCIAL VEHICLE",
            527:"HEAVY COMMERCIAL VEHICLE",
            528:"CONSTRUCTION EQUIPMENTS",
            529:"THREE WHEELERS",
            530:"LIGHT COMMERCIAL VEHICLES",
            531:"SMALL COMMERCIAL VEHICLE",
            738:"MEDIUM COMMERCIAL VEHICLE",
            783:"BUSES"}
    predict_request.append(cat)
    res.append(prod_cat.get(int(cat)))
    
    brand = request.json["brand"]
    brand_type = {1:"Others",
                  1360:"HONDA",
                  1542:"HERO", 
                  1544:"HMSI",
                  1547:"YAMAHA",
                  1546:"SUZUKI",
                  1647:"TVS",
                  1549:"ROYAL ENFIELD"
                  }
    predict_request.append(brand)
    res.append(brand_type.get(int(brand)))
    
    indus = request.json["industrytype"]
    ind_cat = {1782:"SALARIED",1783:"SELF EMPLOYEED",603:"AGRICULTURE",
     604:"PASSENGER TRANSPORTATION",605:"CONSTRUCTION",875:"INFRASTRUCTURE",
     876:"CEMENT",877:"OIL AND GAS",878:"GOVERNMENT CONTRACT",879:"OTHERS",658:"MINE"}
    predict_request.append(indus)
    res.append(ind_cat.get(int(indus)))
    
    tenure = request.json["tenure"]
    predict_request.append(tenure)
    res.append(tenure)
    
    instal = request.json["instalcount"]
    predict_request.append(instal)
    res.append(instal)
    
    chasasset = request.json["chasasset"]
    predict_request.append(chasasset)
    res.append(chasasset)
    
    chasinitial = request.json["chasinitial"]
    predict_request.append(float(chasinitial))
    res.append("{:,}".format(float(chasinitial)))
    
    chasfin = float(chasasset) - float(chasinitial)
    predict_request.append(float(chasfin))
    res.append("{:,}".format(int(chasfin)))
    
    fininter = request.json["finaninterest"]
    predict_request.append(fininter)
    res.append(fininter)
    
    interestamount = (int(chasfin)*(int(tenure)/12)*(float(fininter)))/100
    emi = (int(chasfin)+int(interestamount))/int(tenure)
    predict_request.append(int(emi))
    res.append("{:,}".format(int(emi)))
    
    inflow = request.json["totinflow"]
    predict_request.append(float(inflow))
    res.append("{:,}".format(float(inflow)))
    
    score = request.json["score"]
    predict_request.append(score)
    res.append(score)
    
    
    cibil = request.json['cibil']
    predict_request.append(cibil)
    res.append(cibil)
    
    age = request.json["age"]
    predict_request.append(age)
    res.append(age)
    
    #############################################
    #l2v,af,gross,bk,es,am,gl
    loan = (int(chasfin)*100/float(chasasset)) 
    if (loan<85):
        loan_to_value = 120
    elif ((loan>=85) and (loan <=90)):
        loan_to_value = 100
    elif (loan>90):
        loan_to_value = 50
    predict_request.append(loan_to_value)
    res.append(loan_to_value)
    l2v = (15/loan_to_value)*100
    
    
    brand = int(brand)
    # Approved Models (Hero /Honda/Suzuki  - All Products)
    if ((brand == 1360) | (brand == 1542) | (brand == 1544) | (brand == 1546)):
        asset_finance = 100
    
    # Unapproved Models (Only Yahama, TVS and Royal Enfield Bike Variants) with PM Approval:
    elif ((brand == 1547) | (brand == 1647) | (brand == 935) | (brand == 1549)):  
        asset_finance = 50
    
    else:
        asset_finance = -100
    predict_request.append(asset_finance)
    res.append(asset_finance)
    af = (10/asset_finance)*100
    
    gi = float(inflow)*12
    if gi > 12000:
        grossincome = 100
    elif gi > 8000 and gi<=12000:
        grossincome = 70
    elif gi >= 5000 and gi<=8000:
        grossincome = 50
    elif gi < 5000:
        grossincome = -50    
    predict_request.append(int(grossincome))
    res.append(grossincome)
    gross = (20/grossincome)*100
    
    bank = request.json["bank_detail"]
    old = {0:"New Account",2:"<3 Month Old",4:">3 Month Old",7:">6 Month Old"}
    res.append(old.get(int(bank)))
    
    flag = False
    #>1 time ABB, >6 months old bank account and >3 yrs in Rented House:
    if ((emi > int(clobal)) & (int(bank) > 6) & ((int(resi) == 2756) & (int(year) > 3))):
        banking = 100
        flag = True
    
    #>1 time ABB & > 6 months old bank account and >2 yrs in Rented House
    if not flag:
        if ((emi > int(clobal)) & (int(bank) > 6) & ((int(resi) == 2756) & (int(year) > 2))):
            banking = 80
            flag = True
    
    # >1 time ABB & >3 months old bank account and >2 yrs in Rented House
    if not flag:
        if ((emi > int(clobal)) & (int(bank) > 3) & ((int(resi) == 2756) & (int(year) > 2))):
            banking = 60
            flag = True
    
    #ABB is less than 1 time or new bank acccount but Borrower has own house:
    if not flag:
        if ((emi > int(clobal)) | ((int(bank) == 0) & (int(resi) == 2755))):
            banking = 100
            flag = True
    
    #CIBIL score is >600:        
    if not flag:
        if (int(cibil)>600):
            banking = 100
            flag = True
    
    #<3 months old bank account or <1 time ABB or <2 yrs in Rented House
    if not flag:
        if ((emi < int(clobal)) | (int(bank) < 3) | ((int(resi) == 2756) & (int(year) < 2))):
            banking = -100
            flag = True         
    predict_request.append(banking)
    res.append(banking)
    bk = (30/banking)*100
    
    stability = request.json["stability"]
    stability_type = {1:"Salaried with over 1 year",
                      2:"Salaried with over 6 Months",
                      3:"Salaried less than 6 Months"}
    res.append(stability_type.get(int(stability)))
    if (int(stability) == 1):
        stab = 100
    if (int(stability) == 2):
        stab = 80
    if (int(stability) == 3):
        stab = -80    
    predict_request.append(stab)
    res.append(stab)
    es = (15/stab)*100
    
    #Age between 21 and 50 years, Married with No Dependents:
    if (((int(age) >= 21) & (int(age) <= 50)) & ((int(status) == 2750) & (int(dep) == 0))):
        age_martial = 120
    
    #Age between 21 and 50 years, Married with Dependents:
    elif (((int(age) >= 21) & (int(age) <= 50)) & ((int(status) == 2750) & (int(dep) != 0))):
        age_martial = 100
    
    #Age between 51 and 62 years, Married with No Dependents:
    elif (((int(age) >= 51) & (int(age) <= 62)) & ((int(status) == 2750) & (int(dep) == 0))):
        age_martial = 80
    
    #Age between 51 and 62 years, Married with Dependents:
    elif (((int(age) >= 51) & (int(age) <= 62)) & ((int(status) == 2750) & (int(dep) != 0))):
        age_martial = 60
    
    #Age between 21 and 40 years, Unmarried:
    elif (((int(age) >= 21) & (int(age) <= 40)) & (int(status) == 2751)):
        age_martial = 100
    
    # Age between 18 and 21, Above 62 and Age between 41 and 60 Unmarried
    elif (((int(age) >= 18) & (int(age) <= 21)) | ((int(age) >= 62)) | (((int(age) >= 41) & (int(age) <= 60)) & (int(status) == 2751))):
        age_martial = 0
    predict_request.append(age_martial)
    res.append(age_martial)
    am = (10/age_martial)*100
    
    geo = request.json["geo"]
    geo_type = {1:"Less than 15 Km",
                2:"More than 15 Km"}
    res.append(geo_type.get(int(geo)))
    if (int(geo) == 1):
        geo_lim = 1
    else: 
        geo_lim = 0 
    predict_request.append(geo_lim)
    res.append(geo_lim)
    gl = geo_lim
    ####################################################################3
    gender_dict = {'M':[0,1],'F':[1,0]}
    cate = request.json["gender"]
    if cate == 'M':
        res.append('Male')
    else:
        res.append('Female')
        
    res.append(request.json["pan"])
    predict_request.extend(gender_dict.get(cate))
    predict_request = list(map(float,predict_request))
    predict_request = np.array(predict_request)
    prediction = model_tw.predict_proba([predict_request])[0][-1]
    output = int((1 - prediction)*100)
    if output < 50:
        condition = 'Risky'
    if output >= 50 and output <= 69:
        condition = 'Barely Acceptable'
    if output >= 70 and output <=89:
        condition = 'Medium'
    if output >= 90 and output <= 99:
        condition = 'Good'
    if output == 100:
        condition = 'Superior'
        
    #l2v,af,gross,bk,es,am,gl
    return jsonify(prediction = output,result_category = condition,Total_Score_Earned_A = l2v+af ,Total_Score_Earned_B = gross+bk,Total_Score_Earned_C = es+am ,geolimit=gl)


@app.route('/predict_tw_ntc_api',methods=['POST','GET'])
def predict_tw_ntc():
    '''
    For rendering results on HTML GUI
    '''
    predict_request = []
    res = []
    
    age = request.json["age"]
    predict_request.append(age)
    res.append(age)
    
    year = request.json["staying_year"]
    predict_request.append(year)
    res.append(year)
    
    inflow = request.json["totinflow"]
    predict_request.append(float(inflow))
    res.append("{:,}".format(float(inflow)))
    
    dep = request.json["dependants"]
    predict_request.append(dep)
    res.append(dep)
    
    chasasset = request.json["chasasset"]
    predict_request.append(chasasset)
    res.append(chasasset)
    
    chasinitial = request.json["chasinitial"]
    predict_request.append(float(chasinitial))
    res.append("{:,}".format(float(chasinitial)))
    
    chasfin = float(chasasset) - float(chasinitial)
    predict_request.append(float(chasfin))
    res.append("{:,}".format(int(chasfin)))
    
    fininter = request.json["finaninterest"]
    predict_request.append(fininter)
    res.append(fininter)
    
    tenure = request.json["tenure"]
    interestamount = (int(chasfin)*(int(tenure)/12)*(float(fininter)))/100
    emi = (int(chasfin)+int(interestamount))/int(tenure)
    predict_request.append(int(emi))
    res.append("{:,}".format(int(emi)))

    
    predict_request.append(tenure)
    res.append(tenure)
    
    od = request.json["od"]
    predict_request.append(od)
    res.append(od)
    
    cibil = request.json['cibil']
    predict_request.append(cibil)
    res.append(cibil)
    
    instal = request.json["instalcount"]
    predict_request.append(instal)
    res.append(instal)
    
    brand = request.json["brand"]
    brand_type = {1:[0,0,0,0,0,0,0,0],
                  1360:[0,1,0,0,0,0,0,0],
                  1542:[1,0,0,0,0,0,0,0], 
                  1544:[0,1,0,0,0,0,0,0],
                  1547:[0,0,0,0,0,0,0,1],
                  1546:[0,0,0,0,0,1,0,0],
                  1647:[0,0,0,0,0,0,1,0],
                  1549:[0,0,0,0,1,0,0,0]
                  }
    predict_request.extend(brand_type.get(int(brand)))
    
    gender_dict = {'M':[0,1],'F':[1,0]}
    cate = request.json["gender"]
    predict_request.extend(gender_dict.get(cate))
    
    status = request.json["martial_status"]
    married = {2750:[1,0],2751:[0,1]}
    predict_request.extend(married.get(int(status)))
    
    resi = request.json["residence"]
    residence = {2755:[1,0],2756:[0,1]}
    predict_request.extend(residence.get(int(resi)))
    
    pincode = request.json["pincode"]
    pin_type = {380001:  [1,0,0,0,0,0,0,0,0,0],
                  733134:[0,1,0,0,0,0,0,0,0,0],
                  518002:[0,0,1,0,0,0,0,0,0,0], 
                  492001:[0,0,0,1,0,0,0,0,0,0],
                  382340:[0,0,0,0,1,0,0,0,0,0],
                  462001:[0,0,0,0,0,1,0,0,0,0],
                  533101:[0,0,0,0,0,0,1,0,0,0],
                  201301:[0,0,0,0,0,0,0,1,0,0],
                  480001:[0,0,0,0,0,0,0,0,1,0],
                  534201:[0,0,0,0,0,0,0,0,0,1]
                  }
       
    if int(pincode) in pin_type:
        predict_request.extend(pin_type.get(int(pincode)))
    else:
        predict_request.extend([0,0,0,0,0,0,0,0,0,0])
        
    check_bounce = request.json["chequeBounce"]
    predict_request.append(check_bounce)
    res.append(check_bounce)
    
    close_balance = request.json["clobal"]
    predict_request.append(close_balance)
    res.append(close_balance)
    
    ####################################################################
    predict_request = list(map(float,predict_request))
    predict_request = np.array(predict_request)
    print(model_tw_ntc.predict_proba([predict_request]))
    prediction  = model_tw_ntc.predict_proba([predict_request])[0][0]
    output = float(prediction * 100)
    print(output)
    
    if float(output) < 50:
        condition = 'Risky'
    if float(output) >= 50 and output < 70:
        condition = 'Barely Acceptable'
    if float(output) >= 70 and float(output) <90:
        condition = 'Medium'
    if float(output) >= 90 and float(output) < 100:
        condition = 'Good'
    if float(output) == 100:
        condition = 'Superior'
        
    return jsonify(prediction = output,result_category = condition)


@app.route('/predict_cv_api',methods=['POST','GET'])
def predict_cv():
    '''
    For rendering results on HTML GUI
    '''
    predict_request = []
    res = []
    
    status = request.json["martial_status"]
    married = {2750:"Married",2751:"Un Married"}
    predict_request.append(status)
    res.append(married.get(int(status)))
    
    dep = request.json["dependants"]
    predict_request.append(dep)
    res.append(dep)
    
    resi = request.json["residence"]
    residence = {2755:"Own",2756:"Rent"}
    predict_request.append(resi)
    res.append(residence.get(int(resi)))
    
    year = request.json["staying_year"]
    predict_request.append(year)
    res.append(year)
    
    age = request.json["age"]
    predict_request.append(age)
    res.append(age)
    
    indus = request.json["industrytype"]
    ind_cat = {1782:"Salaried",1783:"Self Employeed",603:"Agriculture",
     604:"Passenger Transportation",605:"Construction",875:"Infrastructure",
     876:"Cement",877:"Oil and Gas",878:"Government Contract",879:"Others",658:"Mine"}
    predict_request.append(indus)
    res.append(ind_cat.get(int(indus)))
    
    profile = request.json["profile"]
    pro_cat = {2692:"Captive Class",2693:"Retail Class",2694:"Strategy Class"}
    predict_request.append(profile)
    res.append(pro_cat.get(int(profile)))
    
    segment = request.json["segment"]
    seg_cat = {2695:"First Time Buyer",
            2696:"First Time Buyer Plus",
            2697:"Medium Fleet Operators",
            2698:"Small Fleet Operators"}
    predict_request.append(segment)
    res.append(seg_cat.get(int(segment)))
    
    market = request.json["market_load"]
    market_cat = {566:"Market Load",568:"Own Contract",569:"Attached To Fleet Operator"}
    predict_request.append(market)
    res.append(market_cat.get(int(market)))
    
    years = request.json["tot_years"]
    predict_request.append(years)
    res.append(years)
    
    asset = request.json["asset"]
    predict_request.append(asset)
    res.append(int(asset))
    
    
    cat = request.json["productcat"]
    prod_cat = {1784:"Loan Against Property",
            926:"Car",
            912:"Multi Utility Vehicle",
            945:"Vikram",
            1402:"Tractor",
            1373:"Used Vehicles",
            1672:"Tipper",
            1664:"Farm Equipment",
            1541:"Two Wheeler",
            634:"Intermediate Commercial Vehicle",
            527:"Heavy Commercial Vehicle",
            528:"Construction Eqquipments",
            529:"Three Wheelers",
            530:"Light Commercial Vehicle",
            531:"Small Commercial Vehicle",
            738:"Medium Commercial Vehicle",
            783:"Busses"}
    predict_request.append(cat)
    res.append(prod_cat.get(int(cat)))
    
    brand = request.json["brand"]
    brand_type = {
           564:"Ashok Leyland",
           565:"Tata Motors",
           740:"Caterpillar",
           739:"Ace",
           741:"Escorts Ltd",
           743:"JCB",
           744:"L&T-Komatsu",
           745:"L&T-Case",
           723:"Eicher Motors",
           815:"JCBL",
           904:"Hyundai Construction Equipments Ltd",
           1377:"ELGI",
           1433:"Ajax Fiori Engineering Ltd",
           1476:"Hercles",
           1416:"Mahindra Navistar Automotives Ltd",
           1501:"Mahindra Construction Equpiment",
           1620:"Dossan",
           1623:"Liugong",
           1638:"Kobelco Construction Equipment Ltd",
           1639:"Sany",
           1659:"Tata Hitachi",
           1681:"Case New Holland",
           1693:"Volvo",
           1380:"Kirloskar",
           1710:"Action Construction Equipment Ltd",
           1758:"Wirtgen India Ltd",
           1760:"Komatsu Ltd",
           1768:"L&T Case Equipment Ltd",
           1778:"Tata Hitachi Construction Machinery Ltd",
           1781:"Larsen & Tourbo Ltd",
           1816:"Atlas Copco Ltd",
           1839:"Scania Commercial Vehicles",
           1848:"KYB Conmat",
           1861:"Man Trucks Ltd",
           1864:"Sany Heavy Industry Ltd",
           1868:"Jackson Ltd",
           1985:"Bharat Benz",
           2143:"Bull Machines Ltd",
           2149:"Terex India Ltd",
           2399:"Rock Master",
           2420:"Vermeer",
           2424:"Jiangsu Dilong Heavy Machinery Ltd",
           2818:"Dynapac Road Constrcution Ltd",
           2886:"Kesar Road Equipments"}
    predict_request.append(brand)
    res.append(brand_type.get(int(brand)))
    
    tenure = request.json["tenure"]
    predict_request.append(tenure)
    res.append(tenure)
    
    instal = request.json["instalcount"]
    predict_request.append(instal)
    res.append(instal)
    
    chasasset = request.json["chasasset"]
    predict_request.append(chasasset)
    res.append(int(chasasset))
    
    chasinitial = request.json["chasinitial"]
    predict_request.append(chasinitial)
    res.append(int(chasinitial))
    
    chasfin = int(chasasset) - int(chasinitial)
    predict_request.append(chasfin)
    res.append(int(chasfin))
    
    fininter = request.json["finaninterest"]
    predict_request.append(fininter)
    res.append(fininter)
    
    interestamount = (int(chasfin)*(int(tenure)/12)*(float(fininter)))/100
    emi = (int(chasfin)+int(interestamount))/int(tenure)
    predict_request.append(int(emi))
    res.append(int(emi))
    
    gross_loan = request.json["availed_loan"]
    predict_request.append(gross_loan)
    res.append(int(gross_loan))
    
    income = request.json["totincome"]
    predict_request.append(income)
    res.append(int(income))
    
    expense = request.json["totexpense"]
    predict_request.append(expense)
    res.append(int(expense))
    
    surplus = int(income) - int(expense)
    predict_request.append(surplus)
    res.append(int(surplus))
    
    s1 = request.json["vehicle"]
    s1_cat = {"1":"New Vehicle","2":"Used Vehicle"}
    res.append(s1_cat.get(s1))
    if (int(s1) == 1):
        predict_request.append(0)
        res.append(0)
    else:
        veh_age = request.json["vehicle_age"]
        predict_request.append(veh_age)
        res.append(veh_age)
    
    clobal = request.json["clobal"]
    predict_request.append(int(clobal))
    res.append(int(clobal))
    
    score = request.json["score"]
    predict_request.append(score)
    res.append(score)
    
    another_score = request.json["cibil"]
    predict_request.append(another_score)
    res.append(another_score)
    
    ###############################
    #Loan to Value:
    loan = ((int(chasfin)*100)/int(chasasset))
    if (loan<75):
        loan_to_value = 100
        predict_request.append(100)
        res.append(100)
    elif ((loan>=75) and (loan <=80)):
        loan_to_value = 75
        predict_request.append(75)
        res.append(75)
    elif (loan>80):
        loan_to_value = 0
        predict_request.append(0)
        res.append(0)
     
    if  loan_to_value != 0:    
        l2v = (20/loan_to_value)*100
    else:
        l2v = 0                                #l2v,col,dues,banks,ep
        
    #Collateral
    if int(asset) > (2*chasfin):
        collateral = 120
        predict_request.append(120)
        res.append(120)
    elif int(asset) == (2*chasfin):
        collateral = 75
        predict_request.append(75)
        res.append(75)    
    elif int(asset) == chasfin:
        collateral = 40
        predict_request.append(40)
        res.append(40)    
    else:
        collateral = 0
        predict_request.append(0)
        res.append(0)
        
    if collateral != 0:
        col = (40/collateral)*100
    else:
        col = 0
    
    #OverDue:    
    overdue = request.json["od"]
    od = [1 if int(overdue) != 0 else 0][0]
    od_cat = {0:"No",1:"Yes"}
    res.append(od_cat.get(int(od)))
    if int(od) == 0:
        due = 100
        predict_request.append(100)
        res.append(100)
    elif int(od) == 1:
        due = 0
        predict_request.append(0)
        res.append(0)
        
    if due !=0:
        dues = (10/due)*100
    else:
        dues = 0
    
    #Banking
    bank_p = request.json["bank_period"]
    bank_p_cat = {1:"More than 3 years",
                  2:"Between 1 to 3 years",
                  3:"More than 6 months",
                  4:"Less than 6 months"}
    res.append(bank_p_cat.get(int(bank_p)))
    if int(bank_p) == 1:
        bank = 100
        predict_request.append(100)
        res.append(100)
    elif int(bank_p) == 2:
        bank = 50
        predict_request.append(50)
        res.append(50)
    elif int(bank_p) == 3:
        bank = 0
        predict_request.append(0)
        res.append(0)
    elif int(bank_p) == 4:
        bank = -50
        predict_request.append(-50)
        res.append(-50)
        
    if bank != 0:
        banks = (10/bank)*100
    else:
        banks = 0
        
    
    #Earning Potential:    
    if int(market) == 569 and int(segment) == 2697:
        potential = 60
        predict_request.append(60)
        res.append(60)
    
    elif int(market) == 569 and int(segment) == 2698:
        potential = 25
        predict_request.append(25)
        res.append(25)
            
    elif int(market) == 566:
        potential = 0
        predict_request.append(0)
        res.append(0)
    
    elif int(market) == 568:
        potential = 80
        predict_request.append(80)
        res.append(80)
        
    else:
        potential = 0
        predict_request.append(0)
        res.append(0)
        
    if potential !=0:
        ep = (20/potential)*100
    else:
        ep = 0
       
    ##############################
    
    gender_dict = {'M':[0,1],'F':[1,0]}
    cate = request.json["gender"]
    if cate == 'M':
        res.append('Male')
    else:
        res.append('Female')
    res.append(request.json["pan"])
    
      
    if int(segment) == 2695:
        res.append(0)
    else:
        #Getting fleet size:
        fleet = request.json["fleet"] 
        res.append(fleet)
        
    predict_request.extend(gender_dict.get(cate))
    print(len(predict_request))
    predict_request = list(map(float,predict_request))
    predict_request = np.array(predict_request)
    prediction = model_cv.predict_proba([predict_request])[0][-1]
    output = int((1 - prediction)*100)
    if output < 60:
        condition = 'Risky'
    if output >= 60 and output <= 70:
        condition = 'Barely Acceptable'
    if output >= 71 and output <= 80:
        condition = 'Medium'
    if output >= 81 and output <=90:
        condition = 'Good'
    if output > 90:
        condition = 'Superior'
        
    #l2v,col,dues,banks,ep
    return jsonify(prediction=output,result_category = condition,Total_Score_Earned_A = l2v ,Total_Score_Earned_B = ep+banks,Total_Score_Earned_C = dues,Total_Score_Earned_D = col)

@app.route('/predict_scv_api',methods=['POST','GET'])
def predict_scv():
    '''
    For rendering results on HTML GUI
    '''
    predict_request = []
    res = []
    
    status = request.json["martial_status"]
    married = {2750:"Married",2751:"Un Married"}
    predict_request.append(status)
    res.append(married.get(int(status)))
    
    dep = request.json["dependants"]
    predict_request.append(dep)
    res.append(dep)
    
    resi = request.json["residence"]
    residence = {2755:"Own",2756:"Rent"}
    predict_request.append(resi)
    res.append(residence.get(int(resi)))
    
    year = request.json["staying_year"]
    predict_request.append(year)
    res.append(year)
    
    age = request.json["age"]
    predict_request.append(age)
    res.append(age)
    
    indus = request.json["industrytype"]
    ind_cat = {1782:"Salaried",1783:"Self Employeed",603:"Agriculture",
     604:"Passenger Transportation",605:"Construction",875:"Infrastructure",
     876:"Cement",877:"Oil and Gas",878:"Government Contract",879:"Others",658:"Mine"}
    predict_request.append(indus)
    res.append(ind_cat.get(int(indus)))
    
    profile = request.json["profile"]
    pro_cat = {2692:"Captive Class",2693:"Retail Class",2694:"Strategy Class"}
    predict_request.append(profile)
    res.append(pro_cat.get(int(profile)))
    
    segment = request.json["segment"]
    seg_cat = {2695:"First Time Buyer",
            2696:"First Time Buyer Plus",
            2697:"Medium Fleet Operators",
            2698:"Small Fleet Operators"}
    predict_request.append(segment)
    res.append(seg_cat.get(int(segment)))
    
    market = request.json["market_load"]
    market_cat = {566:"Market Load",568:"Own Contract",569:"Attached To Fleet Operator"}
    predict_request.append(market)
    res.append(market_cat.get(int(market)))
    
    asset = request.json["asset"]
    predict_request.append(asset)
    res.append(int(asset))
    
    years = request.json["tot_years"]
    predict_request.append(years)
    res.append(years)
    
    cat = request.json["productcat"]
    prod_cat = {1784:"Loan Against Property",
            926:"Car",
            912:"Multi Utility Vehicle",
            945:"Vikram",
            1402:"Tractor",
            1373:"Used Vehicles",
            1672:"Tipper",
            1664:"Farm Equipment",
            1541:"Two Wheeler",
            634:"Intermediate Commercial Vehicle",
            527:"Heavy Commercial Vehicle",
            528:"Construction Eqquipments",
            529:"Three Wheelers",
            530:"Light Commercial Vehicle",
            531:"Small Commercial Vehicle",
            738:"Medium Commercial Vehicle",
            783:"Busses"}
    predict_request.append(cat)
    res.append(prod_cat.get(int(cat)))
    
    brand = request.json["brand"]
    brand_type = {746:"Mahindra",
                  747:"Piaggio",
                  564:"Ashok Leyland",
                 1437:"Atul Auto",
                  821:"Maruti Suzuki",
                  816:"Bajaj Auto",
                  908:"Atul Shakti",
                  742:"Force Motors",
                  723:"Eicher Motors",
                 1654:"Continental Engines Ltd",
                 1341:"Hyundai Motors",
                 1491:"Renault",
                 2035:"Lohia Industries",
                 1342:"Ford India Ltd",
                 1523:"Maruthi",
                 1415:"Nissan",
                 1407:"API Motors Ltd",
                 1330:"JSA",
                 1420:"Toyota Motors",
                  935:"TVS Motors",
                 2034:"Pasupathi Vehicles Ltd",
                  724:"Swaraj Mazda Ltd",
                 1440:"Scooter India Ltd",
                  914:"Toyota Kirloskar Motors",
                 1404:"Chevrolet",
                 1391:"Volswagen",
                 1360:"Honda Motors"}
    predict_request.append(brand)
    res.append(brand_type.get(int(brand)))
    
    tenure = request.json["tenure"]
    predict_request.append(tenure)
    res.append(tenure)
    
    instal = request.json["instalcount"]
    predict_request.append(instal)
    res.append(instal)
    
    chasasset = request.json["chasasset"]
    predict_request.append(chasasset)
    res.append(int(chasasset))
    
    chasinitial = request.json["chasinitial"]
    predict_request.append(chasinitial)
    res.append(int(chasinitial))
    
    chasfin = int(chasasset) - int(chasinitial)
    predict_request.append(chasfin)
    res.append(int(chasfin))
    
    fininter = request.json["finaninterest"]
    predict_request.append(fininter)
    res.append(fininter)
    
    interestamount = (int(chasfin)*(int(tenure)/12)*(float(fininter)))/100
    emi = (int(chasfin)+int(interestamount))/int(tenure)
    predict_request.append(int(emi))
    res.append(int(emi))
    
    gross_loan = request.json["availed_loan"]
    predict_request.append(gross_loan)
    res.append(int(gross_loan))
    
    income = request.json["totincome"]
    predict_request.append(income)
    res.append(int(income))
    
    expense = request.json["totexpense"]
    predict_request.append(expense)
    res.append(int(expense))
    
    surplus = int(income) - int(expense)
    predict_request.append(surplus)
    res.append(int(surplus))
    
    s1 = request.json["vehicle"]
    s1_cat = {"1":"New Vehicle","2":"Used Vehicle"}
    res.append(s1_cat.get(s1))
    if (int(s1) == 1):
        predict_request.append(0)
        res.append(0)
    else:
        veh_age = request.json["vehicle_age"]
        predict_request.append(veh_age)
        res.append(veh_age)
    
    clobal = request.json["clobal"]
    predict_request.append(int(clobal))
    res.append(int(clobal))
    
    score = request.json["score"]
    predict_request.append(score)
    res.append(score)
    
    another_score = request.json["cibil"]
    predict_request.append(another_score)
    res.append(another_score)
    
    ###############################
    #Loan to Value:
    loan = ((int(chasfin)*100)/int(chasasset))
    if (loan<75):
        loantovalue = 100
        predict_request.append(100)
        res.append(100)
    elif ((loan>=75) and (loan <=80)):
        loantovalue = 75
        predict_request.append(75)
        res.append(75)
    elif (loan>80):
        loantovalue = 0
        predict_request.append(0)
        res.append(0)
    
    if loantovalue != 0:
        l2v = (20/loantovalue)*100
    else:
        l2v = 0
        
    #Collateral
    if int(asset) > (2*chasfin):
        collateral = 120
        predict_request.append(120)
        res.append(120)
    elif int(asset) == (2*chasfin):
        collateral = 75
        predict_request.append(75)
        res.append(75)    
    elif int(asset) == chasfin:
        collateral = 40
        predict_request.append(40)
        res.append(40)    
    else:
        collateral = 0
        predict_request.append(0)
        res.append(0)
        
    if collateral != 0:
        col = (40/collateral)*100
    else:
        col = 0
    
    #OverDue:    
    overdue = request.json["od"]
    od = [1 if int(overdue) != 0 else 0][0]
    od_cat = {0:"No",1:"Yes"}
    res.append(od_cat.get(int(od)))
    if int(od) == 0:
        due = 100
        predict_request.append(100)
        res.append(100)
    elif int(od) == 1:
        due = 0
        predict_request.append(0)
        res.append(0)
    
    if due != 0:
        dues = (10/due)*100
    else:
        dues = 0 
    
    #Banking
    bank_p = request.json["bank_period"]
    bank_p_cat = {1:"More than 3 years",
                  2:"Between 1 to 3 years",
                  3:"More than 6 months",
                  4:"Less than 6 months"}
    res.append(bank_p_cat.get(int(bank_p)))
    if int(bank_p) == 1:
        bank = 100
        predict_request.append(100)
        res.append(100)
    elif int(bank_p) == 2:
        bank = 50
        predict_request.append(50)
        res.append(50)
    elif int(bank_p) == 3:
        bank = 0
        predict_request.append(0)
        res.append(0)
    elif int(bank_p) == 4:
        bank = -50
        predict_request.append(-50)
        res.append(-50)
        
    if bank != 0:
        banks = ep = (10/bank)*100
    else:
        banks = 0
    
    #Earning Potential:    
    if int(market) == 569 and int(segment) == 2697:
        potential = 60
        predict_request.append(60)
        res.append(60)
    
    elif int(market) == 569 and int(segment) == 2698:
        potential = 25
        predict_request.append(25)
        res.append(25)
            
    elif int(market) == 566:
        potential = 0
        predict_request.append(0)
        res.append(0)
    
    elif int(market) == 568:
        potential = 80
        predict_request.append(80)
        res.append(80)
    
    else:
        potential = 0
        predict_request.append(0)
        res.append(0)
        
    if potential != 0:
        ep = (20/potential)*100
    
    else:
        ep = 0
       
    ##############################
    
    gender_dict = {'M':[0,1],'F':[1,0]}
    cate = request.json["gender"]
    if cate == 'M':
        res.append('Male')
    else:
        res.append('Female')
    res.append(request.json["pan"])
    
      
    if int(segment) == 2695:
        res.append(0)
    else:
        #Getting fleet size:
        fleet = request.json["fleet"] 
        res.append(fleet)
        
    predict_request.extend(gender_dict.get(cate))
    print(len(predict_request))
    predict_request = list(map(float,predict_request))
    predict_request = np.array(predict_request)
    prediction = model_scv.predict_proba([predict_request])[0][-1]
    output = int((1 - prediction)*100)
    if output < 60:
        condition = 'Risky'
    if output >= 60 and output <= 70:
        condition = 'Barely Acceptable'
    if output >= 71 and output <= 80:
        condition = 'Medium'
    if output >= 81 and output <=90:
        condition = 'Good'
    if output > 90:
        condition = 'Superior' 
        
    #l2v,col,dues,banks,ep
    return jsonify(prediction=output,result_category = condition,Total_Score_Earned_A = l2v ,Total_Score_Earned_B = ep+banks,Total_Score_Earned_C = dues,Total_Score_Earned_D = col)

#Function to read all bank statements:
def bank_stmt_readers(file,bank):
    """
    This function going to read bank statements using tabula-py
    """
    #Reading *.PDF Statement: 
    tables = tabula.read_pdf(file,pages="all")
    #If we found a table:
    if(len(tables) != 0):
    
        #Combining all tables that are get Extracted: 
        table = []
        for i in tables:
            table.extend(i.values.tolist())
        #Read all tables as dataframe:
        df = pd.DataFrame(table)
        #Make all the None values are Null Values:
        df[df.values == None] = np.nan
        #Removing Null values date records: 
        df = df[df.iloc[:,0].notnull()]
        #Reset Dataframe Index:
        df.reset_index(drop=True,inplace=True)
        #Hashtable for Each Bank:
        banks = {"axis":{"date_col_index":0,"bal_col_index":5,
                         "columns":['tran_Date', 'chq_No', 'particulars', 'debit', 'credit', 'balance'],
                         "narration_col_index":2
                        },
                 "hdfc":{"date_col_index":0,"bal_col_index":6,
                         "columns":['tran_Date', 'particulars', 'chq_No', 'value_Date', 'debit','credit', 'balance'],
                         "narration_col_index":1
                        },
                 "icici":{"date_col_index":2,"bal_col_index":7,
                          "columns":["serial_No","value_Date",'tran_Date',"chq_No","particulars","debit","credit","balance"],
                          "narration_col_index":4
                         },
                 "iob":{"date_col_index":0,"bal_col_index":6,
                        "columns":['tran_Date', 'chq_No', 'particulars', 'cod', 'debit', 'credit', 'balance'],
                        "narration_col_index":2
                       },
                 "lakshmi_vilas":{"date_col_index":0,"bal_col_index":5,
                                  "columns":['tran_Date',"value_Date","particulars","chq_No","amount","balance"],
                                  "narration_col_index":2
                                 },
                "andhra_bank":{"date_col_index":0,"bal_col_index":5,
                                  "columns":['tran_Date',"chq_No",'particulars',"debit","credit","balance"],
                                  "narration_col_index":2
                                 }
                }
        #Gettitng date column index for correspoding bank:
        date_col_index = banks[bank].get("date_col_index")
        #Extracting Records that contain Date:
        index = []
        for i in range(len(df.iloc[:,0])):
            try:
                if(dateutil.parser.parse(df.iloc[i,date_col_index])):
                    index.append(True)
            except:
                index.append(False)
        #Filtering Records that contain Date:
        df = df[index]
        #Parse date column:
        df.iloc[:,date_col_index] = df.iloc[:,date_col_index].apply(dateutil.parser.parse, dayfirst=True)
        #Reset Dataframe Index:
        df.reset_index(drop=True,inplace=True)
        #Gettitng balance column index for correspoding bank:
        bal_col_index = banks[bank].get("bal_col_index")
        #Applying Mask:
        if(bank != "axis"):
            if(df.shape[1] > bal_col_index+1):
                for i in range(len(df)):
                    if(str(df.iloc[i,bal_col_index+1]) != "nan"):
                        df.iloc[i,bal_col_index] = df.iloc[i,bal_col_index+1]
        ####################################################################               
        #If the Balance column is missed:                
        value_to_null = []
        try:
            if(df.iloc[:,bal_col_index].isnull().sum() >1):
                for i in range(len(df)):
                    if(str(df.iloc[i,bal_col_index]) == "nan"):
                        start = bal_col_index
                        while(str(df.iloc[i,start]) == "nan"):
                            start = start - 1
                        df.iloc[i,bal_col_index] = df.iloc[i,start]
                        value_to_null.append([i,start])
                        
        except IndexError:
            df["new"] = np.nan
            #Filling null valued balance column: 
            value_to_null = []
            if(df.iloc[:,bal_col_index].isnull().sum() >=1):
                for i in range(len(df)):
                    if(str(df.iloc[i,bal_col_index]) == "nan"):
                        start = bal_col_index
                        while(str(df.iloc[i,start]) == "nan"):
                            start = start - 1
                        df.iloc[i,bal_col_index] = df.iloc[i,start]
                        value_to_null.append([i,start])
        ###################################################################
        #Apply filter:
        df = df.iloc[:,:bal_col_index+1]
        #Applying Regular Expression to parse Balance to avoid RS,MRP,INR:
        bal_list = []
        import re
        try:
            for i in range(len(df[bal_col_index])):
                bal_list.append(re.findall("(?i)(?:(?:RS|INR|MRP)\.?\s?)(\d+(:?\,\d+)?(\,\d+)?(\.\d{1,2})?)",df[bal_col_index][i])[0][0])
            df.iloc[:,bal_col_index] = bal_list
        except:
            pass
        #Paring Closing balance:
        df.iloc[:,bal_col_index] = df.iloc[:,bal_col_index].astype(str)
        vals = []
        for i in df.iloc[:,bal_col_index]:
            vals.append("".join(i.split(",")))
        df.iloc[:,bal_col_index] = vals
        #TypeCasting Closing Balance:
        df.iloc[:,bal_col_index] = pd.to_numeric(df.iloc[:,bal_col_index],errors='coerce')
        #Return resultant dataframe:
        df.columns = banks[bank].get("columns")
        #Paring Date:
        df.iloc[:,date_col_index] = df.iloc[:,date_col_index].astype(str)
        #Gettitng description column index for correspoding bank:
        narration_col_index = banks[bank].get("narration_col_index")
        narration = []
        for i in df.iloc[:,narration_col_index]:
            narration.append(re.sub('[^A-Za-z0-9]+', ' ', i))
        df.iloc[:,narration_col_index] = narration
        #Handling Null values(According to hdfc1.pdf)(Combined values removing)
        if(df.iloc[:,bal_col_index].isnull().sum() >= 1):
            for i in range(len(df)):
                if(str(df.iloc[i,bal_col_index]) == "nan"):
                    start = bal_col_index
                    while(str(df.iloc[i,start]) == "nan"):
                        start = start - 1
                    if(len(str(df.iloc[i,start]).split()) > 1):
                        df.iloc[i,bal_col_index] = str(df.iloc[i,start]).split()[-1]
                        df.iloc[i,start] = str(df.iloc[i,start]).split()[0]
        df.to_csv("test.csv",index = False)
        #Filling Null values of transactions:
        df.iloc[:,:-4] = df.iloc[:,:-4].fillna("-")
        df.iloc[:,-4:] = df.iloc[:,-4:].fillna(0)
        #Handling Date dd-mm-YYYY
        for i in np.arange(len(df.iloc[:,date_col_index])):
            df.iloc[i,date_col_index] = datetime.datetime.strptime(str(df.iloc[i,date_col_index]), "%Y-%m-%d").strftime("%d-%m-%Y")
        response = "success"
    #If we not found table: 
    else:
        df = pd.DataFrame() 
        response = "failed"
    #Return Dataframe and Status Code:
    return df,response

@app.route('/bank_stmt_api',methods=['POST','GET'])
def bank_stmt():
    '''
    For rendering results on HTML GUI
    '''
    Statement = request.files["file"]
    print(Statement)
    Name = request.form["name"]
    print(Name)
    result,code = bank_stmt_readers(Statement,Name)
    if(code == "success"):
        return jsonify(status_Code = code,transactions = result.to_dict(orient="records"))
    else:
        return jsonify(status_Code = code)

if __name__ == "__main__":
    app.run(debug=True)