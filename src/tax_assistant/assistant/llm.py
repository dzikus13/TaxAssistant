from openai import OpenAI
import os


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


class StopSessionException(BaseException):
    pass


class OpenAIConnector:
    def __init__(self, system_prompt: str):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.LLM_MODEL = "gpt-4o-2024-08-06"
        self.temperature = 0
        self.top_p = 0
        self.system_prompt

    def build_messages(self, user_prompt, message_history):
        messages = []
        messages.append({
            "role": "system",
            "content": self.system_prompt
        })
        for item in message_history:
            messages.append({
                "role": "user",
                "content": item.prompt
            })
            messages.append({
                "role": "assistant",
                "content": item.response
            })

        messages.append({
                    "role": "user",
                    "cpmtemt": user_prompt    
                })
        return messages

    def get_gpt_response(self, user_prompt, history):
        messages = self.build_messages(user_prompt, history)
        response = self.client.chat.completions.create(
            model=self.LLM_MODEL,
            messages=messages,
            temperature=self.temperature,
            top_p=self.top_p,
            response_format="json_object"

            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "stop_chat",
                        "description": "Use this function when the user is talking about a topic unrelated to taxes",
                        "parameters": {
                            "type": "object",
                            "properties": {},
                            "additionalProperties": False,
                            "required": []
                        },
                        "strict": True
                    }
                }
            ],
            parallel_tool_calls=true,
        )

        if response.choices[0].finish_reason == "tool_calls":
            function_name = response.choices[0].message.tool_calls[0].function.name
            if function_name == "stop_chat":
                raise StopSessionException("Chat session has been ended")

        return response
    
    def discover_topic(self, prompt):
        return "pcc-3"