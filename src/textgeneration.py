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


# response output is like this way so:
# response.choices[0] extract list then choose message and its content

# response = {
#     "id": "abc123",
#     "choices": [
#         {
#             "index": 0,
#             "message": {
#                 "role": "assistant",
#                 "content": "Machine learning is a branch of AI that allows computers to learn patterns from data."
#             }
#         }
#     ],
#     "model": "some-free-model",
#     "usage": {
#         "prompt_tokens": 5,
#         "completion_tokens": 15
#     }
# }