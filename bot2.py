import requests
import streamlit as st
import json, ast
import openai
from dotenv import load_dotenv  
import os
st.sidebar.success("指导你建立苹果系统上的快捷指令/捷径")
# 加载.env文件  
load_dotenv("./en1106.env")  

os.environ["OPENAI_API_TYPE"] = os.environ["Azure_OPENAI_API_TYPE1"]
os.environ["OPENAI_API_BASE"] = os.environ["Azure_OPENAI_API_BASE1"]
os.environ["OPENAI_API_KEY"] =  os.environ["key"]
os.environ["OPENAI_API_VERSION"] = os.environ["Azure_OPENAI_API_VERSION1"]
BASE_URL=os.environ["OPENAI_API_BASE"]
API_KEY=os.environ["OPENAI_API_KEY"]

CHAT_DEPLOYMENT_NAME=os.environ.get('AZURE_OPENAI_API_CHAT_DEPLOYMENT_NAME')
EMBEDDING_DEPLOYMENT_NAME=os.environ.get('AZURE_OPENAI_API_EMBEDDING_DEPLOYMENT_NAME')

openai.api_type = os.environ["OPENAI_API_TYPE"]
openai.api_base = os.environ["OPENAI_API_BASE"]
openai.api_version = "2024-02-15-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")
print([openai.api_type, openai.api_base,openai.api_version,openai.api_key,CHAT_DEPLOYMENT_NAME])

def run_conversation(question):    
    system_message = {"role":"system","content":'''你是苹果快捷指令专家。你总是用快捷指令的知识回答用户的问题。如何不能回答请如实的说不知道。
        '''}
    i=20
    messages = st.session_state.messages[-i:]
    while messages[0]=='assistant':
        i+=1
        messages = st.session_state.messages[-i:]
    
    response = openai.ChatCompletion.create(
        engine=CHAT_DEPLOYMENT_NAME,
        messages = [system_message]+messages,
        temperature=0.7,
        max_tokens=1000,
        stream=True
    ) 
    
    for chunk in response:
        if chunk.choices:
            if 'content' in chunk.choices[0].delta:
                c=chunk.choices[0].delta.content
                if c is not None:
                    yield c


if "messages" not in st.session_state:
    st.session_state.messages = []

    
for message1 in st.session_state.messages:
    with st.chat_message(message1["role"]):
        st.markdown(message1["content"])


if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        response = st.write_stream(run_conversation(prompt))
        st.session_state.messages.append({"role": "assistant", "content": response})
