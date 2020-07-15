from django.shortcuts import render
from .models import Destination
from django.http import HttpResponse
from io import BytesIO
from datetime import datetime
import FundamentalAnalysis as fa, pandas as pa, matplotlib.pyplot as plt, base64, numpy as np, os
import io
import matplotlib.pyplot as plt; plt.rcdefaults()
from django.conf import settings
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import json
# Create your views here.

def add(request):

    val1 = int(request.GET['num1'])
    val2 = int(request.GET['num2'])
    res = val1 + val2

    return render(request, 'result.html', {'result':res})

def index(request):
    data_json = os.path.join(settings.BASE_DIR, 'static/styles/particles.json')
    open_json = open(data_json)

    def get_jsonparsed_data(url):
    
        response = urlopen(url)
        data = response.read().decode("utf-8")
        return json.loads(data)

    url = ("https://financialmodelingprep.com/api/v3/quote/%5EGSPC,%5EDJI,%5EIXIC?apikey=249951aad4f6272646d75bc50547168b")
    realtime = (get_jsonparsed_data(url))

    dji = realtime[0]


    dji_percentage = dji["changesPercentage"]
    dji_price = dji["price"]
    

    sp500 = realtime[1]
    sp500_percentage = sp500["changesPercentage"]
    sp500_price = sp500["price"]
    

    nasdaq = realtime[2]
    nasdaq_percentage = nasdaq["changesPercentage"]
    nasdaq_price = nasdaq["price"]
    

    context = {'open_json':open_json, 'dji_price':dji_price,'dji_percentage':dji_percentage,'sp500_price':sp500_price,'sp500_percentage':sp500_percentage,'nasdaq_price':nasdaq_price,'nasdaq_percentage':nasdaq_percentage}

    return render(request, 'index.html',context)


def destinations(request):
    return render(request, 'destinations.html')


api_key ="249951aad4f6272646d75bc50547168b"

def betaCalc(request):
    ticker = request.GET['betaTicker']
    TICKER = ticker.upper()
    profile = fa.profile(TICKER, api_key)

    x = profile.loc["beta"]
    Beta = (x[0])

    income_statement_annually = fa.income_statement(TICKER, api_key, period="annual")


    Stock_Revenue = income_statement_annually.loc["revenue"]

    namesREV = []
    yearDCF_REV = int(datetime.now().year)

    Stock_Revenue_List = Stock_Revenue.iloc[:].values
    Stock_Revenue_List.tolist()

    for i in range(len(Stock_Revenue_List)):
      namesREV.append(yearDCF_REV-i)

    Stock_Income = income_statement_annually.loc["netIncome"]
    Stock_Income_List = Stock_Income.iloc[:].values
    Stock_Income_List.tolist

    income_statement_annually = fa.income_statement(TICKER, api_key, period="quarter")

    x = income_statement_annually.loc["eps"]

    EPS_LIST = (x[0], x[1], x[2], x[3])

    TOTAL_EPS = x[0] + x[1] + x[2] + x[3]

    profile = fa.profile(TICKER, api_key)

    price = profile.loc["price"]

    PE_RATIO = price / TOTAL_EPS
    PE_LIST = PE_RATIO.values
    PE_string = str(PE_LIST)

    varA = namesREV
    varB = Stock_Revenue_List.tolist()
    varC = Stock_Income_List.tolist()

    dcf_annually = fa.discounted_cash_flow(TICKER, api_key, period="annual")

    namesDCF_X = []
    yearDCF_X = 2020

    StockPrice_DCF_X = dcf_annually.loc["Stock Price"]

    StockPrice_list_DCF_X = StockPrice_DCF_X.iloc[:].values
    

    for i in range(len(StockPrice_list_DCF_X)):
        namesDCF_X.append(yearDCF_X-i)

    StockPrice_DCF_Y = dcf_annually.loc["DCF"]
    StockPrice_list_DCF_Y = StockPrice_DCF_Y.iloc[:].values
    
    varPrice = StockPrice_list_DCF_X.tolist()
    varDCF = StockPrice_list_DCF_Y.tolist()
        
    
    context={'varA':varA,'varB':varB, 'varC':varC,'Beta':Beta, 'PE_string': PE_string, 'EPS_LIST':EPS_LIST, 'varPrice':varPrice, 'varDCF':varDCF, 'namesDCF_X':namesDCF_X}
    return render(request, "result.html",context)


