import streamlit as st
from openai import OpenAI


def run_gen_pipeline(prompt):

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",  # why use .streamlit or what dot means and this base url mans
        api_key=st.secrets["OPENROUTER_API_KEY"]
    )

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


