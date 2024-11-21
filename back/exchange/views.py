import requests
from datetime import datetime
from django.http import JsonResponse


def exchange(request):
    API_KEY = "sCqdNQGIog1c8b451iW63Ji4dCeLW4hR"  # Replace with your actual API key
    BASE_URL = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"
    
    # Get today's date in YYYY-MM-DD format
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Fetch data from API
    params = {
        "authkey": API_KEY,
        "searchdate": today,
        "data": "AP01"
    }
    
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # Filter out only successful results (result == 1)
        filtered_data = [item for item in data if item["result"] == 1]
        
        return JsonResponse({"success": True, "rates": filtered_data})
    else:
        return JsonResponse({"success": False, "error": "Failed to fetch exchange rates"})
    
def convert_currency(request):
    amount = float(request.GET.get("amount", 0))
    from_currency = request.GET.get("from_currency", "USD")
    to_currency = request.GET.get("to_currency", "KRW")
    
    API_KEY = "sCqdNQGIog1c8b451iW63Ji4dCeLW4hR"
    BASE_URL = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"
    
    today = datetime.now().strftime('%Y-%m-%d')
    params = {
        "authkey": API_KEY,
        "searchdate": today,
        "data": "AP01"
    }
    
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        rates = {item["cur_unit"]: float(item["deal_bas_r"].replace(",", "")) for item in data if item["result"] == 1}
        
        if from_currency not in rates or to_currency not in rates:
            return JsonResponse({"success": False, "error": "Currency not supported"})
        
        # Perform conversion
        converted_amount = (amount / rates[from_currency]) * rates[to_currency]
        
        return JsonResponse({
            "success": True,
            "converted_amount": round(converted_amount, 2),
            "from_currency": from_currency,
            "to_currency": to_currency
        })
    else:
        return JsonResponse({"success": False, "error": "Failed to fetch exchange rates"})