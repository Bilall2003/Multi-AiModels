import streamlit as st
from transformers import pipeline,logging
from summarization import summarization_func
from sentiment import run_sent_pipeline

# ------------------------------------------------------------------
# UI ONLY: page config + custom styling (no logic here)
# ------------------------------------------------------------------
st.set_page_config(page_title="Multi-AiModel", page_icon="✨", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stMarkdown, button, input, textarea {
    font-family: 'Plus Jakarta Sans', 'Segoe UI', sans-serif !important;
}

/* Hide default Streamlit menu/footer */
#MainMenu, footer {visibility: hidden;}
header[data-testid="stHeader"] {background: transparent;}

/* Moving gradient background */
.stApp {
    background: linear-gradient(125deg, #0B1020, #141B3D, #1C1745, #0F2A3F, #0B1020);
    background-size: 400% 400%;
    animation: bgShift 22s ease infinite;
}
@keyframes bgShift {
    0%   {background-position: 0% 50%;}
    50%  {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
.stApp::before {
    content:""; position:fixed; inset:-20%; z-index:0; pointer-events:none;
    background:
        radial-gradient(600px 400px at 20% 30%, rgba(108,140,255,.18), transparent 60%),
        radial-gradient(500px 380px at 80% 70%, rgba(139,92,246,.16), transparent 60%);
    animation: drift 26s ease-in-out infinite alternate;
}
@keyframes drift {
    from {transform: translate(-3%, -2%) scale(1);}
    to   {transform: translate(4%, 3%) scale(1.08);}
}
@media (prefers-reduced-motion: reduce) {
    .stApp, .stApp::before {animation: none;}
}
[data-testid="stMain"], .block-container {position: relative; z-index: 1;}
.block-container {padding-top: 2.2rem; max-width: 820px;}

/* Chat input bar transparent so gradient shows */
[data-testid="stBottom"], [data-testid="stBottom"] > div,
[data-testid="stBottomBlockContainer"] {background: transparent !important;}
[data-testid="stChatInput"] {border-radius: 16px;}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #121930 0%, #0F1527 100%);
    border-right: 1px solid rgba(255,255,255,.06);
}
[data-testid="stSidebar"] hr {border-color: rgba(255,255,255,.07);}

/* Titles */
.stApp h1 {
    font-weight: 800; letter-spacing: -.02em;
    background: linear-gradient(90deg, #F4F6FD, #9DB2FF);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}

/* Chat messages: glass cards */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,.09);
    border-radius: 16px; padding: 1rem 1.1rem; margin-bottom: .8rem;
}

[data-testid="stAlert"] {border-radius: 12px;}

/* ---------- Extra UI components ---------- */
.hero-icon {
    width:54px; height:54px; border-radius:16px; display:grid; place-items:center;
    font-size:1.7rem; margin-bottom:.8rem;
    background: linear-gradient(135deg, rgba(108,140,255,.25), rgba(139,92,246,.20));
    border: 1px solid rgba(140,160,255,.40);
    box-shadow: 0 8px 28px rgba(108,140,255,.25), inset 0 1px 0 rgba(255,255,255,.15);
}
.chip-row {margin: -.2rem 0 .9rem 0;}
.chip {
    display:inline-block; padding:.24rem .75rem; border-radius:999px; font-size:.78rem;
    font-weight:600; margin: 0 .4rem .4rem 0;
    background: rgba(108,140,255,.12); color:#B3C2FF; border:1px solid rgba(108,140,255,.30);
}
.chip.ok {background: rgba(52,211,153,.12); color:#7BE3BC; border-color: rgba(52,211,153,.32);}
.chip.ok::before {
    content:""; display:inline-block; width:7px; height:7px; border-radius:50%;
    background:#34D399; margin-right:.45rem; box-shadow:0 0 8px #34D399;
}

/* Sidebar brand */
.brand {display:flex; align-items:center; gap:.7rem; padding:.2rem 0 .2rem 0;}
.brand-logo {
    width:44px; height:44px; border-radius:13px; display:grid; place-items:center;
    background: linear-gradient(135deg,#6C8CFF,#8B5CF6); font-size:1.35rem;
    box-shadow: 0 8px 22px rgba(108,140,255,.40);
}
.brand-text {font-size:.78rem; color:#8D98B8; line-height:1.3;}
.brand-text b {display:block; font-size:1rem; color:#F2F5FF; font-weight:800;}
.side-foot {font-size:.76rem; color:#7F8AAB; line-height:1.5; margin-top:.4rem;}

/* Sidebar title/caption sit tighter */
[data-testid="stSidebar"] h1 {font-size:1.5rem;}

/* Divider with gradient */
.stApp hr {
    border: none !important; height: 1px !important;
    background: linear-gradient(90deg, rgba(108,140,255,.55), rgba(255,255,255,.06), transparent) !important;
}

/* Select box and radio */
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,.05); border: 1px solid rgba(255,255,255,.12);
    border-radius: 12px; transition: border-color .15s ease, box-shadow .15s ease;
}
[data-testid="stSelectbox"] > div > div:hover {border-color:#6C8CFF; box-shadow:0 0 0 3px rgba(108,140,255,.15);}
[data-testid="stRadio"] label {border-radius: 10px;}

/* Chat input focus glow */
[data-testid="stChatInput"] > div {
    border: 1px solid rgba(255,255,255,.14); border-radius: 16px;
    background: rgba(255,255,255,.05); backdrop-filter: blur(10px);
    transition: border-color .15s ease, box-shadow .15s ease;
}
[data-testid="stChatInput"] > div:focus-within {
    border-color:#6C8CFF; box-shadow: 0 0 0 3px rgba(108,140,255,.22);
}

/* Chat avatars */
[data-testid="stChatMessageAvatarUser"] {background: linear-gradient(135deg,#6C8CFF,#8B5CF6) !important;}
[data-testid="stChatMessageAvatarAssistant"] {background: linear-gradient(135deg,#34D399,#22A6B3) !important;}

/* Alerts: info / warning / error cards */
[data-testid="stAlert"] {
    border: 1px solid rgba(255,255,255,.10); backdrop-filter: blur(8px);
}

/* Status box in sidebar */
[data-testid="stStatus"] {
    border-radius: 14px; border: 1px solid rgba(255,255,255,.10);
    background: rgba(255,255,255,.04);
}

/* Captions */
.stApp [data-testid="stCaptionContainer"] {color:#9AA5C4;}

/* Slim scrollbar */
::-webkit-scrollbar {width: 8px;}
::-webkit-scrollbar-thumb {background: rgba(140,160,255,.30); border-radius: 8px;}
::-webkit-scrollbar-track {background: transparent;}
</style>
""", unsafe_allow_html=True)


def ui_chips(*labels):
    extra = "".join(f'<span class="chip">{l}</span>' for l in labels)
    st.markdown(
        f'<div class="chip-row"><span class="chip ok">Model ready</span>{extra}</div>',
        unsafe_allow_html=True,
    )

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
st.sidebar.markdown(
    '<div class="side-foot">Models stay in memory after the first load, so later requests are faster.</div>',
    unsafe_allow_html=True,
)
with st.sidebar.status("Initializing AI Models...") as status:
    ai_pipelines = load_all_models()
    status.update(label="AI Models Loaded!", state="complete")


# ------------------------------------------------------------------
# UI Structure (Your Original Layout)
# ------------------------------------------------------------------
st.sidebar.markdown(
    '<div class="brand"><div class="brand-logo">✨</div>'
    '<div class="brand-text"><b>AI Workspace</b>Summarize, analyze, generate</div></div>',
    unsafe_allow_html=True,
)
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
        ui_chips("distilbart-cnn-12-6")
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
        ui_chips("distilbert-sst-2")
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
            ui_chips(f"{model_Sel} effort")

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

