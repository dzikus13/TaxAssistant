
import requests
import json
from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, action, permission_classes
from .llm import OpenAIConnector, StopSessionException
from .models import Session, Interaction, SESSION_STATUS
from .utils import get_us_code
from xml_generator.models import TaxForm


SYSTEM_PROMPT = ""

class HistoryDto:
    def __init__(self, prompt, response):
        self.prompt = prompt
        self.response = response


def combine_knowledge(metadata, values):
    results = []
    for item, value in metadata.items():
        if item in values:
            value["value"] = values[item]
        results.append({
            "field": item,
            "value": value
        })
    return results


@api_view(["POST"])
def process_input(request):
    data = json.loads(request.body)
    session_id = data["session_id"]
    prompt = data["prompt"]
    session, created = Session.objects.get_or_create(user_id=session_id)
    if created:
        ai_connector = OpenAIConnector(SYSTEM_PROMPT)  # TODO: system prompt
        topic = ai_connector.discover_topic(prompt)
        session.topic = topic
        session.save()
    else:
        topic = session.topic

    tax_form = TaxForm.objects.get(name=topic.upper())
    ai_connector = OpenAIConnector(tax_form.system_prompt)
    interactions = [ HistoryDto(item.user_input, item.response)
                     for item in session.interaction_set.all().order_by("created_at")]
    try:
        ai_response = ai_connector.get_gpt_response(prompt, interactions)
        datajson = json.loads(ai_response)
    except StopSessionException:
        session.status = "aborted"
        ai_response = "aborted"
        datajson = {"status": "aborted"}
        session.save()
    
    interaction = Interaction(
        session=session,
        user_input=prompt,
        response=ai_response,
        response_json=datajson
    )
    print(json.dumps(datajson, indent=2))
    interaction.save()
    collected_data = combine_knowledge(tax_form.metadata, session.collect_knowledge())
    if tax_form.is_ready(session.collect_knowledge()):
        tax_form.create_document(session)
        session.status = "finished"
        session.save()
    else:
        missing = tax_form.get_missing_fields(session.collect_knowledge())
        print("missinglist", missing)

    return JsonResponse({
        "status": "success",
        "result": datajson.get("answer"),
        "session_status": session.status,
        "session_collected": collected_data
    })


@api_view(["GET"])
def get_us_code(request):
    data = request.GET
    try:
        us_code = get_us_code(data["post_code"])
        return JsonResponse({
            "status": "success",
            "results": {
                "us_code": us_code
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

@api_view(["GET"])
def get_xml(request):
    data = request.GET.get("session_id")
    session = Session.objects.get(user_id=data)
    doc = session.taxforminstance_set.all().last()
    return HttpResponse(doc.xml, content_type="application/xml")