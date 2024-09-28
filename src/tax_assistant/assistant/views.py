
import requests
import json
from django.shortcuts import render
from django.http.response import JsonResponse
# Create your views here.
from rest_framework.decorators import api_view, action, permission_classes



US_CODE_API_URL = "https://www.e-pity.pl/cms/inc/1/us/apiJson.php"


@api_view(["POST"])
def process_input(request):
    return JsonResponse({})


@api_view(["GET"])
def get_us_code(request):
    data = request.GET
    try:
        print("data", data.get("post_code"))
        response = requests.get(US_CODE_API_URL, params={"us_postal": data.get("post_code"), "us_search": True})
        print(response.text)
        response_data = response.json()
        return JsonResponse({
            "status": "success",
            "results": {
                "us_code": response_data[0].get("us_code")
            }
        })
    except BaseException as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({
            "status": "fail",
            "error": str(e),
            "code": 400
        })
