import streamlit as st
from openai import OpenAI


def run_gen_pipeline(prompt):

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",  # why use .streamlit or what dot means and this base url mans
        api_key=st.secrets["OPENROUTER_API_KEY"]
    )
    
    
    def low():
    
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],temperature=0.3
        )

        return response.choices[0].message.content
    low()
    
    def moderate():
    
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],temperature=0.5
        )

        return response.choices[0].message.content
    
    moderate()
    
    def high():

        response = client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],temperature=0.7
        )

        return response.choices[0].message.content
    high()


