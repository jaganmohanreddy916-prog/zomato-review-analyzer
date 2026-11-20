# Zomato Review Analyzer

A local, AI-powered application that turns restaurant customer reviews into structured feedback reports. It uses a locally running Llama 3.2 model through Ollama and a Streamlit interface to summarize reviews, identify sentiment, extract positive and negative aspects, highlight customer pain points, and suggest business actions.

> **Project type:** Generative AI (LLM-powered text analysis). This repository does not implement an Agentic AI workflow, RAG, embeddings, or vector search.

## What the application does

A user enters a restaurant review in the Streamlit interface. The application sends that text to a locally running Ollama service. The configured `llama3.2` model generates a JSON-formatted analysis, which the application parses and displays as a report.

The requested report fields are:

- Overall sentiment: positive, negative, or neutral
- Estimated review rating (1–5)
- One-line and short summaries
- Positive aspects and negative aspects
- Customer pain points
- Business recommendations
- Suggested audience or occasion (for example, families, couples, or friends)

The interface also provides sentiment counts, a review-history view for the current session, configurable model temperature, and JSON download options.

## Features

- **Review analysis:** submit an individual restaurant review for LLM-based analysis.
- **Structured response:** prompt the model to return a predictable JSON object.
- **Sentiment report:** display the overall sentiment, estimated rating, summary, aspects, pain points, and recommendations.
- **Dashboard:** show counts of reviews analyzed in the current Streamlit session.
- **Sentiment analytics:** show positive, negative, and neutral counts, with a bar chart when enabled.
- **Review history:** revisit analyses held in the current session and download them as JSON.
- **Local model connection:** communicate with Ollama over its local HTTP API.
- **Temperature setting:** adjust response variation for subsequent model requests.

## Technology stack

| Technology | How it is used |
| --- | --- |
| Python | Application logic, request handling, JSON parsing, and data processing |
| Streamlit | Web interface, navigation, inputs, metrics, charts, session state, and downloads |
| Ollama | Runs and serves the language model locally |
| Llama 3.2 (`llama3.2`) | Generates the natural-language review analysis |
| Requests | Sends HTTP requests to the Ollama API |
| JSON | Defines the requested response structure and supports downloadable results |
| Regular expressions (`re`) | Fallback extraction of a JSON object from model output |
| Pandas | DataFrame processing in the additional report-rendering function |
| Plotly Express | Donut and bar charts in the additional report-rendering function |

## How the AI part works

This is a **prompt-based LLM application**. The model receives instructions and the review text, then generates an analysis. The application does not train or fine-tune the model.

### Request and response flow

1. **Input:** the user enters a restaurant review in the Streamlit text area.
2. **Connection check:** the application checks whether the local Ollama service responds at `http://localhost:11434`.
3. **Prompt construction:** the application creates a system instruction and a user prompt. The user prompt includes the review, the requested JSON keys, the output language, and a concise-output instruction.
4. **LLM inference:** Python sends a POST request to `http://localhost:11434/api/chat`, specifying model `llama3.2`, the messages, `stream: false`, and the selected temperature.
5. **Response extraction:** the application reads `message.content` from the Ollama response.
6. **JSON parsing:** it first tries to parse the complete response as JSON. If that fails, it uses a regular expression to find a JSON object and tries to parse that. If neither succeeds, it raises an error.
7. **Presentation:** Streamlit renders the returned fields as a review intelligence report.
8. **Session handling:** the review and its result are appended to Streamlit session state for dashboard counts and review history.

### Simplified architecture

```text
User enters a restaurant review
             |
             v
       Streamlit UI
             |
             v
   Check local Ollama service
             |
             v
 Build system + user prompts
             |
             v
 Python Requests HTTP POST
             |
             v
 Ollama local API (/api/chat)
             |
             v
       Llama 3.2
             |
             v
      Generated text
             |
             v
     JSON extraction
             |
             v
  Structured analysis result
             |
             v
 Streamlit report, history,
 analytics and JSON download
```

## AI concepts: what is and is not implemented

It is important to describe the implementation accurately.

| Concept | Used in this repository? | Explanation |
| --- | --- | --- |
| Generative AI | **Yes** | Llama 3.2 generates summaries, sentiment labels, extracted aspects, pain points, and recommendations from the review prompt. |
| Large Language Model (LLM) | **Yes** | The application calls the `llama3.2` model through Ollama. |
| Prompt engineering | **Yes** | System and user prompts specify the analysis task and desired JSON structure. |
| Structured output / JSON parsing | **Yes** | The prompt requests JSON, and Python parses the model's response. The code does not use a dedicated schema-constrained output mechanism. |
| NLP | **Yes, through the LLM** | The model interprets the natural-language review. There is no separate classical NLP pipeline in the repository. |
| Embeddings | **No** | The code does not convert reviews into embedding vectors. |
| Vector database / vector store | **No** | There is no vector database or similarity-search index. |
| Retrieval-Augmented Generation (RAG) | **No** | The application does not retrieve external documents or relevant stored reviews to provide context to the model. |
| Hugging Face Transformers pipeline | **No** | The project does not import or configure the Transformers library or a Transformers pipeline. Ollama is used to serve the model. |
| Agentic AI / autonomous agents | **No** | There are no agents, tools selected by an LLM, planning loop, task delegation, or autonomous multi-step execution. The application follows a fixed request-response flow. |
| Model training / fine-tuning | **No** | The application calls an existing model; it does not train or fine-tune it. |

### Is this an AI pipeline?

It has a straightforward application processing flow: input → prompt → model inference → JSON parsing → display. It is reasonable to call this an **LLM-powered review-analysis workflow**. It is not a RAG pipeline, an embeddings pipeline, or an agent orchestration pipeline.

## Repository structure

```text
zomato-review-analyzer/
├── app.py
├── requirements.txt
├── sample_reviews.txt
└── README.md
```

- `app.py` — Streamlit application, Ollama connectivity, prompt construction, model request, JSON parsing, result rendering, session history, and analytics/report functions.
- `requirements.txt` — Python package dependencies.
- `sample_reviews.txt` — Present in the repository but currently empty; no sample reviews are supplied in it.
- `README.md` — Project documentation.

## Prerequisites

1. Python 3.10 or later (a compatible Python environment is recommended).
2. Ollama installed and running locally.
3. The `llama3.2` model downloaded in Ollama.

Pull the model with:

```bash
ollama pull llama3.2
```

Start Ollama if it is not already running. The application expects its local service at:

```text
http://localhost:11434
```

## Installation and execution

Clone the repository:

```bash
git clone https://github.com/jaganmohanreddy916-prog/zomato-review-analyzer.git
cd zomato-review-analyzer
```

Create and activate a virtual environment (optional but recommended):

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

Open the local URL printed by Streamlit in your browser. Make sure Ollama is running and the `llama3.2` model is available before submitting a review.

## Configuration

The current application uses these settings in `app.py`:

- **Ollama endpoint:** `http://localhost:11434/api/chat`
- **Model:** `llama3.2`
- **Streaming:** disabled (`stream: false`)
- **Temperature:** adjustable in the sidebar from 0.0 to 1.0; the initial session value is 0.2.
- **Output language:** currently passed as English in the analysis call.

The model name and endpoint are currently defined directly in the source code.

## Current limitations

The README documents the code as it currently exists; it does not imply features that have not been implemented.

- Ollama must be available on the same machine as the application at the configured local endpoint.
- Only one review is sent per model request; there is no batch-processing or dataset-ingestion pipeline in the active analysis flow.
- Review history is stored in Streamlit session state. It is not a persistent database and may be lost when the session ends or resets.
- The estimated rating and generated insights are model outputs, not verified ratings or guaranteed facts.
- The model is asked to return JSON, but the response is not enforced by a JSON schema; malformed responses can fail parsing.
- The sample review text file is empty.
- The code contains additional report-rendering logic using Pandas and Plotly, but the visible sidebar navigation does not include the `Review Report` page.
- The dashboard's top-level sample metric cards are hard-coded demo values; the interactive dashboard later in the app calculates counts from the current session history.

## Possible future improvements

These are ideas for future development, not features currently present:

- Validate model responses with a defined JSON schema and safer error handling.
- Add batch review upload and CSV export.
- Persist review history in SQLite or another database.
- Add tests for Ollama connectivity, response parsing, and report generation.
- Add a configurable model selector and output language selector.
- If semantic search over a large review collection is needed, implement an embeddings model and vector store, then add retrieval before generation (RAG).
- If autonomous multi-step tasks are needed, design an explicit agent workflow with tools, state, and controlled execution.

## License

No license file is currently included in this repository. Add a license before presenting the project as open source for reuse.
