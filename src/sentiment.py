from transformers import pipeline,logging
import streamlit as st

logging.set_verbosity_error()


def run_sent_pipeline(text_input,pipeline_instance):
    
    if not text_input or not text_input.strip():
        return ""
    
    output=pipeline_instance(text_input)[0]['label']
    
    return output
    
    