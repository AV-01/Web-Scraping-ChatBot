import streamlit as st
import os
from openai import AzureOpenAI
import json

# streamlit run "C:\Users\aryav\IdeaProjects\Web Scraping ChatBot\azure_openai_experiment.py"

endpoint = "https://newtestchatbot91.openai.azure.com/"
deployment = "gpt-35-turbo"
search_endpoint = "https://testrhs.search.windows.net"
search_key = "censored"
search_index = "censored"
subscription_key = "censored"

# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(
    azure_endpoint = endpoint,
    api_key = subscription_key,
    api_version = "2024-05-01-preview",
)


st.header("RHS Chatbot(With Azure OpenAI)")
user_question = st.text_input("Type your question here")
if user_question:
    question_to_ask = user_question

    completion = client.chat.completions.create(
        model=deployment,
        messages= [
        {
            "role": "system",
            "content": "You are an AI chatbot that lives on the Rocklin High School website, more commonly referred to as \"RHS\". Answer questions people have! When people refer to \"you\", they're usually referring to Rocklin High School"
        },
        {
            "role": "user",
            "content": f"{question_to_ask}"
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
    response = json.loads(completion.to_json())
    print(response)
    st.write(response["choices"][0]["message"]["content"])
