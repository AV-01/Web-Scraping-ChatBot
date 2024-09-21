import streamlit as st
import os
from openai import AzureOpenAI
import json

endpoint = "https://newtestchatbot91.openai.azure.com/"
deployment = "gpt-35-turbo"
search_endpoint = "https://testrhs.search.windows.net"
search_key = "censored"
search_index = "censored"
subscription_key = "censored"

if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
            "role": "system",
            "content": "You are an AI chatbot that lives on the Rocklin High School website, more commonly referred to as \"RHS\". Answer questions people have! When people refer to \"you\", they're usually referring to Rocklin High School"
        })
# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(
    azure_endpoint = endpoint,
    api_key = subscription_key,
    api_version = "2024-05-01-preview",
)


# Function to handle chatbot responses
def get_chatbot_response(user_input):
    print(st.session_state.messages)
    completion = client.chat.completions.create(
        model=deployment,
        messages= 
        st.session_state.messages
    ,
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
    return response["choices"][0]["message"]["content"]

# Streamlit UI
st.title("RHS Chatbot(With Azure OpenAI)")

# Session state to keep track of conversation history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# User input
user_input = st.text_input("You: ", "")

if st.button("Send"):
    if user_input:
        # Append user message to the chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get chatbot response
        bot_response = get_chatbot_response(user_input)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

        # Clear input field
        st.rerun()

# Display messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    elif message["role"] == "assistant":
        st.markdown(f"**Bot:** {message['content']}")
