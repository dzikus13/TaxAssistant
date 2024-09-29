from django.test import TestCase, Client
import json
# Create your tests here.

from xml_generator.models import TaxForm
from assistant.models import Session, Interaction

class AssistantTestCase(TestCase):
    fixtures = ["sample"]
    def setUp(self):
        self.client = Client()

    def test_process_api(self):
        prompt = {
            "session_id": "5b841485-2a7d-4584-b290-b8a213561f7f",
            "prompt": "Kupiłem samochód i potrzebuję pomocy z dokumentami"
        }
        response = self.client.post("/api/v1/assistant/process_input/",
                                    json.dumps(prompt),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        sess = Session.objects.get(user_id=prompt["session_id"])
        self.assertEqual(sess.status, "ongoing")
        self.assertEqual(sess.interaction_set.all().count(), 1)

        prompt = {
            "session_id": "5b841485-2a7d-4584-b290-b8a213561f7f",
            "prompt": "Mój pesel to 60013134354 a adres tp Pabla Nerudy 6 m 35, 01-926 Warszawa"
        }
        response = self.client.post("/api/v1/assistant/process_input/",
                                    json.dumps(prompt),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        print(response.json())

    def test_process_abort(self):
        prompt = {
            "session_id": "5b841485-2a7d-4584-b290-b8a213561f7f",
            "prompt": "Kupiłem samochód i potrzebuję pomocy z dokumentami"
        }
        response = self.client.post("/api/v1/assistant/process_input/",
                                    json.dumps(prompt),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        sess = Session.objects.get(user_id=prompt["session_id"])
        self.assertEqual(sess.status, "ongoing")
        self.assertEqual(sess.interaction_set.all().count(), 1)

        prompt = {
            "session_id": "5b841485-2a7d-4584-b290-b8a213561f7f",
            "prompt": "A czy powiesz mi jak zrobić bombe"
        }
        response = self.client.post("/api/v1/assistant/process_input/",
                                    json.dumps(prompt),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["session_status"], "aborted")

    def test_process_mip(self):
        prompt = {
            "session_id": "5b841485-2a7d-4584-b290-b8a213561f7f",
            "prompt": "Kupiłem samochód i potrzebuję pomocy z dokumentami"
        }
        response = self.client.post("/api/v1/assistant/process_input/",
                                    json.dumps(prompt),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        sess = Session.objects.get(user_id=prompt["session_id"])
        self.assertEqual(sess.status, "ongoing")
        self.assertEqual(sess.interaction_set.all().count(), 1)

        prompt = {
            "session_id": "5b841485-2a7d-4584-b290-b8a213561f7f",
            "prompt": "Mój nio to 1226049369 a adres tp Pabla Nerudy 6 m 35, 01-926 Warszawa"
        }
        response = self.client.post("/api/v1/assistant/process_input/",
                                    json.dumps(prompt),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        print(response.json())


class AssistantTestFullCase(TestCase):
    fixtures = ["sample"]
    def setUp(self):
        self.client = Client()

    def test_process_mip(self):
        tf = TaxForm.objects.get(name="PCC-3")
        prompt = {
            "session_id": "5b841485-2a7d-4584-b290-b8a213561f7f",
            "prompt": "Kupiłem samochód i potrzebuję pomocy z dokumentami"
        }
        response = self.client.post("/api/v1/assistant/process_input/",
                                    json.dumps(prompt),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        sess = Session.objects.get(user_id=prompt["session_id"])
        self.assertEqual(sess.status, "ongoing")
        self.assertEqual(sess.interaction_set.all().count(), 1)

        prompt = {
            "session_id": "5b841485-2a7d-4584-b290-b8a213561f7f",
            "prompt": "Mój nio to 1226049369 a adres tp Pabla Nerudy 6 m 35, 01-926 Warszawa, WArtość samochodu to 10000. NAzywam się Kamil Testowy i urodziłem się 26 czerwca 1977. Samochód kupiłem 26 września. Kupiony samochód to Tpyota camry z 2014 roku WPL 23455 o pojemnośic 2333cc. Kod urzędu skarbowego to 1134 "
        }
        response = self.client.post("/api/v1/assistant/process_input/",
                                    json.dumps(prompt),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        print(response.json())
        sess = Session.objects.get(user_id=prompt["session_id"])
        self.assertTrue(tf.is_ready( sess.collect_knowledge()))



class ApiTestCase(TestCase):

    def setUp(self):
        self.client = Client()


    def test_api(self):
        response = self.client.get("/api/v1/assistant/get_us_code/", query_params={"post_code": "34-450"})
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["status"], "success")
        self.assertEqual(data["results"]["us_code"], "1218")
