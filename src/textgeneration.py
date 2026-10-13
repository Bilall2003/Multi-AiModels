import streamlit as st
from openai import OpenAI


try:

    def low(prompt):
        
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",  
            api_key=st.secrets["OPENROUTER_API_KEY"]
        )
        
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

    prompt="Enter text"
    low(prompt)
        
    def moderate(prompt):
        
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",  
            api_key=st.secrets["OPENROUTER_API_KEY"]
        )
        
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
        
    prompt="Enter text"
    moderate(prompt)
        
    def high(prompt):
        
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",  
            api_key=st.secrets["OPENROUTER_API_KEY"]
        )

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

    prompt="Enter text"
    high(prompt)

except Exception as e:
    
    st.error(f"Something Went Wrong{e}")


