# views.py

import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime

@api_view(['GET'])
def exchange_rate_api(request):
    # Get query parameters from the request (base_currency and target_currency)
    base_currency = request.GET.get('base_currency')
    target_currency = request.GET.get('target_currency')

    if not base_currency or not target_currency:
        return Response({"error": "Missing required parameters: base_currency and target_currency"}, status=400)

    # Get the current date in 'YYYYMMDD' format
    current_date = datetime.now().strftime('%Y%m%d')

    # Replace 'YOUR_API_KEY' with your actual API key
    auth_key = "sCqdNQGIog1c8b451iW63Ji4dCeLW4hR"
    
    # Construct the API URL with the required parameters
    url = f"https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={auth_key}&searchdate={current_date}&data=AP01"
    
    try:
        # Make a GET request to the external API
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for bad responses (4xx, 5xx)
        
        # Parse the JSON response
        exchange_rates = response.json()

        # Find rates for selected currencies
        base_rate = next((rate for rate in exchange_rates if rate['cur_unit'] == base_currency), None)
        target_rate = next((rate for rate in exchange_rates if rate['cur_unit'] == target_currency), None)

        if not base_rate or not target_rate:
            return Response({"error": "Invalid currency codes"}, status=400)

        return Response({
            "base_currency": base_rate,
            "target_currency": target_rate,
        })
    
    except requests.RequestException as e:
        return Response({"error": f"API request failed: {str(e)}"}, status=500)