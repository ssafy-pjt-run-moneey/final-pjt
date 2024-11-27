import requests
from datetime import datetime, timedelta
from django.http import JsonResponse

def get_latest_exchange_data(api_key, base_url):
    today = datetime.now()
    
    for i in range(7):  # Try up to 7 days back
        date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        params = {
            "authkey": api_key,
            "searchdate": date,
            "data": "AP01"
        }

        headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
        response = requests.get(base_url, headers=headers, params=params, verify=False)
        
        if response.status_code == 200:
            data = response.json()
            filtered_data = [item for item in data if item["result"] == 1]
            if filtered_data:
                return filtered_data, date
    
    return None, None

def exchange(request):
    API_KEY = "sCqdNQGIog1c8b451iW63Ji4dCeLW4hR"
    BASE_URL = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"
    
    filtered_data, date = get_latest_exchange_data(API_KEY, BASE_URL)
    
    if filtered_data:
        return JsonResponse({"success": True, "rates": filtered_data, "date": date})
    else:
        return JsonResponse({"success": False, "error": "Failed to fetch exchange rates"})

# Django views.py
def convert_currency(request):
    try:
        amount = float(request.GET.get("amount", 0))
        from_currency = request.GET.get("from_currency", "KRW")
        to_currency = request.GET.get("to_currency", "USD")
        
        API_KEY = "sCqdNQGIog1c8b451iW63Ji4dCeLW4hR"
        BASE_URL = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"
        
        filtered_data, date = get_latest_exchange_data(API_KEY, BASE_URL)
        
        if filtered_data:
            # KRW to USD
            if from_currency == "KRW" and to_currency == "USD":
                converted_amount = amount * 0.00071
            # USD to KRW
            elif from_currency == "USD" and to_currency == "KRW":
                converted_amount = amount / 0.00071
            else:
                # For other currency pairs, use the API rates
                rates = {item["cur_unit"]: float(item["deal_bas_r"].replace(",", "")) for item in filtered_data}
                if from_currency not in rates or to_currency not in rates:
                    return JsonResponse({"success": False, "error": "Currency not supported"})
                
                # Handle currencies quoted per 100 units
                from_mod = 100 if any(item["cur_unit"] == from_currency + "(100)" for item in filtered_data) else 1
                to_mod = 100 if any(item["cur_unit"] == to_currency + "(100)" for item in filtered_data) else 1
                
                if from_currency == "KRW":
                    converted_amount = (amount / rates[to_currency]) * to_mod
                else:
                    converted_amount = (amount * rates[from_currency] / from_mod)

            # Format result without trailing zeros
            converted_str = f"{converted_amount:.10f}".rstrip('0').rstrip('.')
            
            return JsonResponse({
                "success": True,
                "converted_amount": converted_str,
                "from_currency": from_currency,
                "to_currency": to_currency,
                "date": date
            })
        else:
            return JsonResponse({"success": False, "error": "Failed to fetch exchange rates"})
            
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})