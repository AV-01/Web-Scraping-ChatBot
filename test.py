import requests
import json

url = "http://localhost:7071/api/http_trigger?messages=hi"


question_to_ask = "What math classes can I take?"
messages = [
                    {
                        "role": "system",
                        "content": "You are an AI chatbot that lives on the Rocklin High School website, more commonly referred to as \"RHS\". Answer questions people have! When people refer to \"you\", they're usually referring to Rocklin High School"
                    },
                    {
                        "role": "user",
                        "content": f"{question_to_ask}"
                    }
                ]
data = {
    "messages":messages,
    "response_only": True
}

response = requests.post(url)

print("Status Code", response.status_code)

print(response.text)

# print("JSON Response ", response.text)
# response_text = response.json()
# print(response_text["choices"][0]["message"]["content"])
# formatted_text = response_text.replace("'", '"')
# print(formatted_text)
# cut_text = json.loads(formatted_text)
# print(type(cut_text))

# json_data = [json.loads(s) for s in requests.get(url).text.strip().split("\n")]
# print(json_data[0]['<some-subscriber-email>'][0]['action'])