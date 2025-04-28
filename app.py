import openai
import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain_community.llms import OpenAI
import json
import streamlit as st
import base64
import getpass

import boto3
from botocore.exceptions import ClientError


def get_secret():

    secret_name = "aws-managed-openai"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    
    except ClientError as e:
  
        raise e

    secret = get_secret_value_response['SecretString']
    secret = json.loads(secret)
    return str(secret['OPENAI_API_KEY'])

    # Your code goes here.


def prediction_pipeline(text):
    print("Inside prediction pipeline")
    text_splitter = CharacterTextSplitter(separator = '\n', chunk_size = 1000, chunk_overlap = 20)

    text_chunks = text_splitter.split_text(text)
    print(len(text_chunks))
    
    llm = OpenAI(openai_api_key = get_secret())
    docs= [Document(page_content=t) for t in text_chunks]
    chain = load_summarize_chain(llm=llm, chain_type='map_reduce', verbose = True)
    summary = chain.run(docs)
    return summary

user_input = st.text_area("Enter Text to Summarize")
button = st.button("Generate Summary")
if user_input and button:
    summary = prediction_pipeline(user_input)
    st.write("Summary :", summary)

text1= "In the heart of downtown Riverside, a once-abandoned lot has been transformed into a thriving community garden, thanks to the efforts of local volunteers. The project, which began six months ago, now boasts over 50 varieties of fruits, vegetables, and flowers.Organizers say the garden not only provides fresh produce to residents but also strengthens community bonds. “It’s more than just a garden — it’s a gathering place for everyone,” said project coordinator Maria Lopez. Weekly workshops on sustainable farming and nutrition have attracted dozens of participants, including many young students.City officials have praised the initiative, hinting that similar projects could soon sprout up in other neighborhoods. With the arrival of spring, the Riverside Community Garden is expected to see even greater growth, both in plants and in community spirit."

prediction_pipeline(text1)
