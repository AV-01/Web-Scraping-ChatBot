import azure.functions as func
import logging
from openai import AzureOpenAI
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


# Hidden variables that contain API Keys


@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    messages = req.params.get('messages')
    if not messages:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            messages = req_body.get('messages')

            client = AzureOpenAI(
                azure_endpoint = endpoint,
                api_key = subscription_key,
                api_version = "2024-05-01-preview",
            )
            completion = client.chat.completions.create(
                model=deployment,
                messages= messages,
                # past_messages=10,
                max_tokens=800,
                temperature=0,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None,
                stream=False
            ,
                extra_body={
                "data_sources": [{
                    "type": "azure_search",
                    "parameters": {
                        "endpoint": f"{search_endpoint}",
                        "index_name": "newrhsaiindex",
                        "semantic_configuration": "default",
                        "query_type": "vector_semantic_hybrid",
                        "fields_mapping": {},
                        "in_scope": True,
                        "role_information": "You are an AI chatbot that lives on the Rocklin High School website, more commonly referred to as \"RHS\". Answer questions people have! When people refer to \"you\", they're usually referring to Rocklin High School",
                        "filter": None,
                        "strictness": 3,
                        "top_n_documents": 5,
                        "authentication": {
                        "type": "api_key",
                        "key": f"{search_key}"
                        },
                        "embedding_dependency": {
                        "type": "deployment_name",
                        "deployment_name": "text-embedding-ada-002"
                        }
                    }
                    }]
                },
                response_format={ "type": "json_object" }
            )
            response = json.loads(completion.to_json())
            return func.HttpResponse(
             json.dumps(response),
             status_code=200,
             mimetype="application/json"
        )
    if messages:
        messages = req.params.get('messages')
        client = AzureOpenAI(
            azure_endpoint = endpoint,
            api_key = subscription_key,
            api_version = "2024-05-01-preview",
        )
        completion = client.chat.completions.create(
            model=deployment,
            messages= [
                    {
                        "role": "system",
                        "content": "You are an AI chatbot that lives on the Rocklin High School website, more commonly referred to as \"RHS\". Answer questions people have! When people refer to \"you\", they're usually referring to Rocklin High School"
                    },
                    {
                        "role": "user",
                        "content": f"{messages}"
                    }
                ],
            # past_messages=10,
            max_tokens=800,
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False
        ,
            extra_body={
            "data_sources": [{
                "type": "azure_search",
                "parameters": {
                    "endpoint": f"{search_endpoint}",
                    "index_name": "newrhsaiindex",
                    "semantic_configuration": "default",
                    "query_type": "vector_semantic_hybrid",
                    "fields_mapping": {},
                    "in_scope": True,
                    "role_information": "You are an AI chatbot that lives on the Rocklin High School website, more commonly referred to as \"RHS\". Answer questions people have! When people refer to \"you\", they're usually referring to Rocklin High School",
                    "filter": None,
                    "strictness": 3,
                    "top_n_documents": 5,
                    "authentication": {
                    "type": "api_key",
                    "key": f"{search_key}"
                    },
                    "embedding_dependency": {
                    "type": "deployment_name",
                    "deployment_name": "text-embedding-ada-002"
                    }
                }
                }]
            },
            response_format={ "type": "json_object" }
        )
        response = json.loads(completion.to_json())["choices"][0]["message"]["content"]
        return func.HttpResponse(
             f"{response}",
             status_code=200
        )
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )