import streamlit as st
from transformers import pipeline, logging

logging.set_verbosity_error()


def summarization_func(text_input,pipeline_instance):
    
    if not text_input or not text_input.strip():
        return ""

    output = pipeline_instance(
        text_input,
        max_new_tokens=int(len(text_input)/2),
        do_sample=True,
        num_beams=5,
        length_penalty=0.7,
        repetition_penalty=1.5
    )

    return output[0]["summary_text"]


if __name__ == "__main__":
    text_input = "any input"
    obj = summarization_func(text_input)
    print(obj)