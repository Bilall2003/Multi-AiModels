import streamlit as st
from transformers import pipeline,logging
from summarization import summarization_func
from sentiment import run_sent_pipeline

# ------------------------------------------------------------------
# CRITICAL FIX: Instantiate pipelines INSIDE the cache block
# ------------------------------------------------------------------
logging.set_verbosity_error()

@st.cache_resource
def load_all_models():
    """Loads all transformers pipelines once and saves them to RAM."""
    pipelines = {}
    
    # 1. Summarization Model 
    pipelines['summarization'] = pipeline(
        "summarization",
        model="sshleifer/distilbart-cnn-12-6"
    )
    
    # 2. Sentiment Analysis Model
    pipelines['sentiment'] = pipeline(
        "text-classification", 
        model="distilbert/distilbert-base-uncased-finetuned-sst-2-english"
    )
    
    return pipelines

# Show a clean loading message instead of crashing the browser WebSocket
with st.sidebar.status("Initializing AI Models...") as status:
    ai_pipelines = load_all_models()
    status.update(label="AI Models Loaded!", state="complete")


# ------------------------------------------------------------------
# UI Structure (Your Original Layout)
# ------------------------------------------------------------------
st.sidebar.title("Multi-AiModel")
st.sidebar.caption("Powered By AI")
st.sidebar.divider()

st.sidebar.subheader("Choose Option")
options = ["Text-summarization", "sentiment-analysis", "Text-generation"]
user_sel = st.sidebar.selectbox("Select", options, label_visibility="collapsed")


try:
    # --- TEXT SUMMARIZATION ---
    if user_sel == "Text-summarization":
        text_input = st.chat_input(placeholder="Write a message here....")
        
        st.sidebar.info("Larger input take time...")
        st.title("Text-Summarization", help="https://huggingface.co/sshleifer/distilbart-cnn-12-6")
        st.caption("Start with entering your text")
        st.divider()
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if text_input:
            with st.chat_message("user"):
                st.markdown(text_input)
            st.session_state.messages.append({"role": "user", "content": text_input})

            with st.chat_message("assistant"):
                with st.spinner("Summarizing..."):                  
                    summary = summarization_func(text_input, ai_pipelines['summarization'])
                    st.markdown(summary)

            st.session_state.messages.append({"role": "assistant", "content": summary})
            st.caption("AI can make mistakes...Double check the response")

    # --- SENTIMENT ANALYSIS ---
    elif user_sel == "sentiment-analysis":
        text_input2 = st.chat_input("write here....")
            
        st.title("Sentiment-Analysis", help="https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english")
        st.divider()
        
        if 'messages2' not in st.session_state:
            st.session_state.messages2 = []
            
        for message2 in st.session_state.messages2:
           with st.chat_message(message2['role']):
                st.markdown(message2['content'])
        
        if text_input2:
            with st.chat_message("user"):
                st.markdown(text_input2)
            st.session_state.messages2.append({'role': 'user', 'content': text_input2})
            
            with st.chat_message("assistant"):
                with st.spinner("Analyzing..."):
                    sentiment = run_sent_pipeline(text_input2, ai_pipelines['sentiment'])
                    st.markdown(sentiment)
            
            st.session_state.messages2.append({'role': 'assistant', 'content': sentiment})
            
    # --- TEXT GENERATION ---
    elif user_sel == "Text-generation":
    
        
        try:
            from textgeneration import low,moderate,high

            text_input3 = st.chat_input("write here....")
            model_Sel=st.sidebar.radio("Choose model",["Low","Moderate","High"],help="Effort of model.....check more https://academy.claude.com/tutorials/choosing-the-right-effort-level-in-claude-code")
            st.sidebar.info(f"User selected: {model_Sel}")

            st.title("Text-Generation",)

            st.caption("Input a message to start chatting...")
            st.warning("Hold information till mid 2024....Can't provide latest and real time news...")
            st.divider()

            if "message3" not in st.session_state:
                st.session_state.message3 = []

            for message3 in st.session_state.message3:

                with st.chat_message(message3["role"]):
                    st.markdown(message3["content"])
                    
            if "low_count" not in st.session_state:
                st.session_state.low_count = 0

            total_low_count = 2

            if text_input3 and model_Sel == "Low":
                with st.chat_message("user"):
                    if st.session_state.low_count >= total_low_count:
                        st.warning("Limit reached.")
                        st.info(st.session_state.low_count)
                    else:
                        st.session_state.low_count += 1
                        st.markdown(text_input3)

                st.session_state.message3.append({
                    "role": "user",
                    "content": text_input3
                })

                with st.chat_message("assistant"):

                    with st.spinner("Thinking...", show_time=True):

                        generation = low(text_input3)

                        st.markdown(generation)

                st.session_state.message3.append({
                    "role": "assistant",
                    "content": generation
                })
                
                
            elif text_input3 and model_Sel=="Moderate":

                with st.chat_message("user"):
                    st.markdown(text_input3)

                st.session_state.message3.append({
                    "role": "user",
                    "content": text_input3
                })

                with st.chat_message("assistant"):

                    with st.spinner("Thinking...", show_time=True):

                        generation = moderate(text_input3)

                        st.markdown(generation)

                st.session_state.message3.append({
                    "role": "assistant",
                    "content": generation
                })
            
            elif text_input3 and model_Sel=="High":
            
                        with st.chat_message("user"):
                            st.markdown(text_input3)
            
                        st.session_state.message3.append({
                            "role": "user",
                            "content": text_input3
                        })
            
                        with st.chat_message("assistant"):
            
                            with st.spinner("Thinking...", show_time=True):
            
                                generation = high(text_input3)
            
                                st.markdown(generation)
            
                        st.session_state.message3.append({
                            "role": "assistant",
                            "content": generation
                        })
        
        except Exception as e:
            st.error(f"Something Went Wrong...Please Try again Later")
            
    else:
        st.info(f"{user_sel} is not available yet.")

except Exception as e:
    st.error(f"Something went wrong... {e}")
