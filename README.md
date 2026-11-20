# Zomato Review Analyzer

A web application that analyzes restaurant reviews and turns customer feedback into useful insights. It uses the Llama 3.2 language model through Ollama to identify sentiment, summarize reviews, highlight positive and negative aspects, find customer pain points, and suggest improvements for restaurants.

## Features

- Analyze restaurant reviews from Zomato, Swiggy, or Google Reviews.
- Classify each review as positive, negative, or neutral.
- Generate an estimated rating out of 5.
- Create a one-line summary and a short review summary.
- Extract positive aspects, negative aspects, and customer pain points.
- Generate practical business recommendations.
- Suggest the type of customers or occasions the restaurant may be suitable for.
- View review counts and sentiment analytics.
- View previous analyses during the current app session.
- Download an individual analysis or review history as JSON.
- Adjust the LLM temperature from the settings panel.

## Technology Used

| Technology | Purpose |
| --- | --- |
| Python | Main programming language and application logic |
| Streamlit | Builds the web interface and dashboard |
| Ollama | Runs the language model locally and provides the API |
| Llama 3.2 | Understands the review text and generates the analysis |
| Prompt Engineering | Guides the model to analyze reviews and return specific fields |
| Requests | Sends review prompts to the Ollama API |
| JSON | Structures the model response and downloaded reports |
| Regular Expressions | Helps extract JSON if the model response contains extra text |
| Pandas | DataFrame operations in the report-generation code |
| Plotly | Creates charts in the report-generation code |

## How It Works

1. Enter a restaurant review in the **Analyze Review** page.
2. The application checks whether Ollama is running locally.
3. Python prepares a system prompt and a user prompt containing the review and the required output fields.
4. The prompt is sent to the Llama 3.2 model through the Ollama chat API.
5. The model generates a structured response containing sentiment, rating, summaries, aspects, pain points, recommendations, and suggested audience.
6. Python extracts and parses the JSON response.
7. Streamlit displays the result as a review analysis report.
8. The review and its result are stored in Streamlit session state so they can be viewed in the dashboard, analytics, and history pages during that session.

## Application Flow

```text
Customer Review
      |
      v
Streamlit Interface
      |
      v
Python Prompt Preparation
      |
      v
Ollama Chat API
      |
      v
Llama 3.2 Model
      |
      v
Generated JSON Response
      |
      v
Python JSON Parsing
      |
      v
Review Analysis Report
      |
      v
Dashboard / Analytics / History
```

## AI Approach

This project uses **Generative AI with a Large Language Model (LLM)**. Llama 3.2 processes the review text and generates the requested insights based on the prompts provided by the application.

Prompt engineering is used to define the analysis task and the expected JSON fields. The model is asked to return structured JSON, which the Python application parses before displaying the result.

The current implementation uses direct prompting and model inference. It does not currently use embeddings, a vector database, semantic search, Retrieval-Augmented Generation (RAG), a Hugging Face Transformers pipeline, or autonomous AI agents.

## Project Structure

```text
zomato-review-analyzer/
├── app.py
├── requirements.txt
├── sample_reviews.txt
└── README.md
```

- **app.py** – Contains the Streamlit interface, Ollama connection, prompt creation, model request, JSON parsing, result display, dashboard, analytics, and review history.
- **requirements.txt** – Lists the Python packages required to run the application.
- **sample_reviews.txt** – File reserved for sample customer reviews.
- **README.md** – Project documentation and setup instructions.

## Requirements

- Python 3.10 or later
- Ollama
- Llama 3.2 model
- Packages listed in `requirements.txt`

## Setup and Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/jaganmohanreddy916-prog/zomato-review-analyzer.git
cd zomato-review-analyzer
```

### 2. Create a virtual environment (recommended)

**Windows**

```bash
python -m venv .venv
.venv\\Scripts\\activate
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and start Ollama

Download and install Ollama from [ollama.com](https://ollama.com/).

Download the Llama 3.2 model:

```bash
ollama pull llama3.2
```

Make sure Ollama is running. The application connects to the local Ollama service at `http://localhost:11434`.

### 5. Start the Streamlit application

```bash
streamlit run app.py
```

Streamlit will display a local URL in the terminal. Open that URL in your browser to use the application.

## Deployment

The application can be run locally using Streamlit and Ollama as described above.

To host the Streamlit interface on a cloud platform, the LLM service must also be accessible to the hosted application. The current code uses `http://localhost:11434`, which refers to the machine running the app. It will not automatically connect to Ollama running on your personal computer after deploying the interface to a cloud server.

For a cloud deployment, configure the application to use a securely hosted Ollama-compatible endpoint or another accessible model-serving service. Store the endpoint in an environment variable or deployment secret rather than exposing credentials or private service details in the source code. Then deploy the Streamlit application with the required Python dependencies.

## Notes

- The model generates an estimated rating and recommendations from the review text. These are AI-generated suggestions, not verified restaurant ratings.
- Review history is stored in Streamlit session state and is not saved permanently in a database.
- The current analysis flow processes one review at a time.
- The model name and Ollama API endpoint are currently set in `app.py`.
