import requests 

US_CODE_API_URL = "https://www.e-pity.pl/cms/inc/1/us/apiJson.php"


def get_us_code(post_code):
    response = requests.get(US_CODE_API_URL, params={"us_postal": post_code, "us_search": True})
    response_data = response.json()
    return response_data[0].get("us_code")