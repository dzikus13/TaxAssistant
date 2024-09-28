from django.test import TestCase, Client

# Create your tests here.

class AssistantTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_process_api(self):
        response = self.client.post("/api/v1/assistant/process_input/", data={"query": "Kupiłem samochod"})
        self.assertEqual(response.status_code, 200)




class ApiTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_api(self):
        response = self.client.get("/api/v1/assistant/get_us_code/", query_params={"post_code": "34-450"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        print(data)
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["results"]["us_code"], "1218")
