from hsnm import RESTfulAPI
from django.http import JsonResponse


def my_api_view():
    base_uri = "http://www.hotspot.yourspot.co.za"
    my_api_key = "38XG46Q3NPM63THRMB9984YJ7V6MY5QQ"
    my_api_secret = "47TY45RDHY77DDNNDNNBD7J8RDL97WQ1"
    end_point = "resellerRead"
    data = '{"id": 207}' 

    api = RESTfulAPI(base_uri, my_api_key, my_api_secret)

    endpoint = 'resellerRead'


    response = api.api_call(endpoint, data)

    if "error" in response:
        # Handle API errors
        error_message = response["error"]
        return JsonResponse({"error": error_message})

    # Process the API response data
    api_data = response

    # Perform any additional processing here

    # Return the API data as a JSON response
    print("Test")
    return JsonResponse(api_data)


