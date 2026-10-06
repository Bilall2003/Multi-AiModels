# 🤖 Multi-AiModels

<p align="center">
  <b>A Streamlit-based NLP application integrating multiple AI models into a single interactive interface.</b>
</p>

<p align="center">
  <a href="https://github.com/Bilall2003/Multi-AiModels">
    <img src="https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github" alt="GitHub Repository">
  </a>
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge&logo=streamlit" alt="Streamlit">
  <img src="https://img.shields.io/badge/Hugging%20Face-Transformers-yellow?style=for-the-badge&logo=huggingface" alt="Hugging Face">
  <img src="https://img.shields.io/badge/OpenRouter-API-purple?style=for-the-badge" alt="OpenRouter">
</p>

---

## 📌 Overview

**Multi-AiModels** is an interactive Natural Language Processing (NLP) application built with **Python and Streamlit**.

The project brings multiple AI-powered NLP capabilities together into a single user interface, allowing users to experiment with different models and approaches without switching between separate applications.

The application currently provides:

* 📝 **Text Summarization**
* 😊 **Sentiment Analysis**
* ✨ **Text Generation**

The project demonstrates both **local AI model inference** and **API-based Large Language Model (LLM) integration** in the same application.

---

## ✨ Features

### 📝 Text Summarization

Summarizes longer text into a shorter and more meaningful version using a pretrained Hugging Face Transformer model.

**Model:**

`sshleifer/distilbart-cnn-12-6`

**Key concepts demonstrated:**

* Transformer-based NLP
* Hugging Face Transformers
* Text preprocessing
* Sequence-to-sequence generation
* Local model inference

---

### 😊 Sentiment Analysis

Analyzes text and determines whether the sentiment is:

* 🟢 Positive
* 🔴 Negative

**Model:**

`distilbert/distilbert-base-uncased-finetuned-sst-2-english`

The model provides sentiment predictions based on the input text.

**Key concepts demonstrated:**

* Text classification
* BERT/DistilBERT
* Hugging Face pipelines
* NLP inference
* Prediction handling

---

### ✨ Text Generation

Generates natural-language responses using an LLM through the **OpenRouter API**.

The application uses the OpenAI-compatible Python SDK while directing requests to OpenRouter's API endpoint.

```python
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"]
)
```

The project currently uses:

```text
openrouter/free
```

for access to available free models.

**Key concepts demonstrated:**

* LLM API integration
* OpenAI-compatible APIs
* API authentication
* Prompt-based generation
* Secure API key management
* Response extraction

---

## 🏗️ Architecture

The application follows a hybrid AI architecture:

```text
                         ┌──────────────────────┐
                         │     Streamlit UI     │
                         └──────────┬───────────┘
                                    │
                         ┌──────────▼───────────┐
                         │   User selects task  │
                         └──────────┬───────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
       ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
       │ Summarization│      │  Sentiment   │      │ Text         │
       │              │      │  Analysis    │      │ Generation   │
       └──────┬───────┘      └──────┬───────┘      └──────┬───────┘
              │                     │                     │
              ▼                     ▼                     ▼
       Hugging Face           Hugging Face           OpenRouter
       Local Model             Local Model               API
              │                     │                     │
              └─────────────────────┼─────────────────────┘
                                    ▼
                              Streamlit Output
```

### Architecture approach

The project intentionally uses two approaches:

**Local inference**

```text
Hugging Face → Model downloaded → Inference on local environment
```

**API inference**

```text
Streamlit → OpenRouter API → Free LLM → Response → Streamlit
```

This demonstrates the practical difference between running AI models locally and consuming AI models through APIs.

---

## 🛠️ Tech Stack

| Technology                   | Purpose                                    |
| ---------------------------- | ------------------------------------------ |
| Python                    | Core programming language                  |
| Streamlit                 | Web application and UI                     |
| Hugging Face Transformers | Local NLP models                           |
| OpenRouter                | LLM API provider                           |
| OpenAI Python SDK         | OpenAI-compatible API client               |
| Streamlit Secrets         | Secure API key management                  |
| Git & GitHub              | Version control and source code management |

---

## 📂 Project Structure

```text
Multi-AiModels/
│
├── .streamlit/
│   └── secrets.toml
│
├── src/
│   ├── app.py
│   ├── sentiment.py
│   ├── summarization.py
│   └── textgeneration.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

### File responsibilities

#### `app.py`

Main Streamlit application.

Responsible for:

* User interface
* Sidebar navigation
* Model selection
* User input
* Session state
* Displaying model responses

#### `summarization.py`

Contains the summarization functionality and connects the application to the summarization pipeline.

#### `sentiment.py`

Contains the sentiment-analysis functionality.

#### `textgeneration.py`

Handles communication with the OpenRouter API and returns the generated response.

---

## 🔐 API Key Security

The OpenRouter API key is **not hard-coded into the source code**.

Instead, Streamlit Secrets is used:

```python
api_key=st.secrets["OPENROUTER_API_KEY"]
```

The secret is stored locally in:

```text
.streamlit/secrets.toml
```

The secret file is excluded from Git using:

```gitignore
.streamlit/secrets.toml
```

This prevents the API key from being accidentally committed to the public GitHub repository.

> ⚠️ Never publish API keys, passwords, tokens, or other credentials in a public repository.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Bilall2003/Multi-AiModels.git
```

### 2. Move into the project directory

```bash
cd Multi-AiModels
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the API key

Create:

```text
.streamlit/secrets.toml
```

Add:

```toml
OPENROUTER_API_KEY = "your_api_key_here"
```

### 6. Run the application

From the project root:

```bash
streamlit run src/app.py
```

The application should then open in your browser.

---

## 💡 How It Works

### Text Generation Flow

```text
User enters prompt
        ↓
Streamlit receives input
        ↓
run_gen_pipeline(prompt)
        ↓
OpenRouter API request
        ↓
Free LLM processes prompt
        ↓
API returns response
        ↓
response.choices[0].message.content
        ↓
Streamlit displays generated text
```

### Sentiment Analysis Flow

```text
User enters text
        ↓
Streamlit
        ↓
Hugging Face pipeline
        ↓
DistilBERT
        ↓
Sentiment prediction
        ↓
Streamlit output
```

### Summarization Flow

```text
User enters article/text
        ↓
Streamlit
        ↓
Hugging Face pipeline
        ↓
DistilBART
        ↓
Generated summary
        ↓
Streamlit output
```

---

## 🎯 Learning Objectives

This project was developed as a practical NLP/AI engineering project to understand how different AI technologies can be integrated into a single application.

The project covers:

* NLP model integration
* Transformer architectures
* Hugging Face pipelines
* Text classification
* Text summarization
* LLM text generation
* API integration
* OpenAI-compatible APIs
* API authentication
* Secret management
* Streamlit application development
* Session state management
* Local vs API-based inference
* Git/GitHub project management

---

## 🔮 Future Improvements

Planned improvements include:

* [ ] Add more NLP tasks
* [ ] Add named entity recognition (NER)
* [ ] Add translation
* [ ] Add configurable generation parameters
* [ ] Add model selection
* [ ] Add conversation history
* [ ] Improve error handling
* [ ] Add loading and model-status indicators
* [ ] Add Docker support
* [ ] Deploy the application publicly
* [ ] Add RAG-based question answering
* [ ] Integrate additional LLM providers
* [ ] Add evaluation metrics for generated outputs

---

## 🐳 Docker Support

Docker support can be added to make the application easier to reproduce across different environments.

A future Docker setup will package:

```text
Application
    +
Python environment
    +
Dependencies
    +
Configuration
```

into a reproducible container.

API secrets should still be supplied securely through environment variables or deployment-platform secrets rather than being placed inside the Docker image.

---

## 📸 Application

The application provides a simple interface where users can select an NLP task from the sidebar and interact with the corresponding AI model.

> Add screenshots of the **Summarization**, **Sentiment Analysis**, and **Text Generation** pages here when available.

Example:

```html
<p align="center">
  <img src="assets/summarization.png" width="80%">
</p>
```

---

## 📚 Models Used

| Task               | Model                                                        | Provider     | Execution |
| ------------------ | ------------------------------------------------------------ | ------------ | --------- |
| Summarization      | `sshleifer/distilbart-cnn-12-6`                              | Hugging Face | Local     |
| Sentiment Analysis | `distilbert/distilbert-base-uncased-finetuned-sst-2-english` | Hugging Face | Local     |
| Text Generation    | `openrouter/free`                                            | OpenRouter   | API       |

---

## ⚠️ Limitations

The application depends on the capabilities and availability of the selected models.

For text generation, the output quality can vary because `openrouter/free` is a routing option that can select from available free models.

API-based functionality also depends on:

* Internet connectivity
* API availability
* Provider rate limits
* Free-model availability

Local models require additional memory and startup time because the models need to be loaded into the local environment.

---

## 👨‍💻 Author

<p align="center">
  <b>Bilal Ahmed</b>
  <br>
  Computer Science Student | AI/ML & NLP Enthusiast
  <br><br>
  <a href="https://github.com/Bilall2003">
    <img src="https://img.shields.io/badge/GitHub-Bilall2003-black?style=for-the-badge&logo=github" alt="GitHub">
  </a>
</p>

---

## ⭐ Acknowledgements

* [Hugging Face Transformers](https://huggingface.co/docs/transformers/)
* [Streamlit](https://streamlit.io/)
* [OpenRouter](https://openrouter.ai/)
* [OpenAI Python SDK](https://github.com/openai/openai-python)

---

## 📄 License

This project is intended for educational and portfolio purposes.

If you add a specific open-source license to the repository, update this section accordingly.

---

<p align="center">
  <b>Built with Python, Streamlit, Hugging Face Transformers & OpenRouter</b>
  <br>
  ⭐ Star the repository if you find it useful!
</p>
