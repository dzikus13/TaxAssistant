
import requests
import json
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.decorators import api_view, action, permission_classes
from .llm import OpenAIConnector, StopSessionException
from .models import Session, Interaction
from xml_generator.models import TaxForm

US_CODE_API_URL = "https://www.e-pity.pl/cms/inc/1/us/apiJson.php"


@api_view(["POST"])
def process_input(request):
    data = json.loads(request.body)
    session_id = data["session_id"]
    prompt = data["prompt"]
    session, created = Session.objects.get_or_create(id=session_id)
    if created:
        ai_connector = OpenAIConnector()  # TODO: system prompt
        topic = ai_connector.discover_topic(prompt)
        session.topic = topic
        session.save()
    else:
        topic = session.topic
    tax_form = TaxForm.objects.get(name=topic)
    ai_connector = OpenAIConnector(tax_form.system_prompt)
    interactions = session.interaction_set.all().order_by("created_at")
    try:
        ai_response = ai_connector.get_gpt_response(prompt, interactions)
    except StopSessionException:
        session.status = 
    interaction = Interaction(
        session=session,
        user_input=prompt,
        respose=ai_response
    )
    interaction.save()
    return JsonResponse({
        "status": "success",
        "result": ai_response,
        "session_status": session.get_status()
    })


@api_view(["GET"])
def get_us_code(request):
    data = request.GET
    try:
        response = requests.get(US_CODE_API_URL, params={"us_postal": data.get("post_code"), "us_search": True})
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
