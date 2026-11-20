import json
import html
import re
import requests
import streamlit as st

st.set_page_config(
    page_title = "Zomato/ Swiggy review Analyzer",
    page_icon = "🍔",
    layout = "wide"
)

OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"



st.markdown("""
<style>

/* ===== GLOBAL THEME ===== */
.stApp {
    background:
        radial-gradient(ellipse at top left, #25172b 0%, transparent 40%),
        linear-gradient(135deg, #0b1020 0%, #111827 55%, #090d18 100%);
    color: #f1f5f9;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* ===== MAIN CONTENT ===== */
.block-container {
    max-width: 1200px;
    padding: 2.5rem 2rem 4rem 2rem;
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #151827 0%, #0c1020 100%);
    border-right: 1px solid #292d42;
}

[data-testid="stSidebar"] * {
    color: #e2e8f0;
}

/* ===== HERO SECTION ===== */
.hero {
    text-align: center;
    padding: 42px 24px;
    margin-bottom: 30px;
    background: linear-gradient(
        135deg,
        rgba(225, 29, 72, 0.18),
        rgba(124, 58, 237, 0.13)
    );
    border: 1px solid rgba(244, 63, 94, 0.30);
    border-radius: 24px;
    box-shadow: 0 15px 45px rgba(0, 0, 0, 0.22);
}

.hero-title {
    font-size: 38px;
    font-weight: 800;
    letter-spacing: -1px;
    margin-bottom: 12px;
    background: linear-gradient(90deg, #fb7185, #fda4af, #c4b5fd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    color: #b7c0d4;
    font-size: 16px;
    line-height: 1.7;
}

/* ===== SECTION HEADINGS ===== */
h1, h2, h3 {
    color: #f8fafc !important;
    font-weight: 750 !important;
}

h2 {
    border-bottom: 1px solid #292d42;
    padding-bottom: 12px;
}

/* ===== METRIC CARDS ===== */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #1a2033, #121827);
    border: 1px solid #303750;
    border-radius: 18px;
    padding: 22px 20px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    transition: all 0.25s ease;
}

[data-testid="stMetric"]:hover {
    border-color: #fb7185;
    transform: translateY(-3px);
}

[data-testid="stMetricLabel"] {
    color: #aab5cc !important;
}

[data-testid="stMetricValue"] {
    color: #fb7185 !important;
    font-weight: 800;
}

/* ===== TEXT AREAS & INPUTS ===== */
.stTextArea textarea,
.stTextInput input,
.stNumberInput input {
    background-color: #151b2b !important;
    color: #f8fafc !important;
    border: 1px solid #39435c !important;
    border-radius: 14px !important;
    padding: 14px !important;
}

.stTextArea textarea:focus,
.stTextInput input:focus {
    border-color: #fb7185 !important;
    box-shadow: 0 0 0 2px rgba(251, 113, 133, 0.15);
}

/* ===== BUTTONS ===== */
.stButton > button,
.stFormSubmitButton > button {
    background: linear-gradient(135deg, #e11d48, #be123c);
    color: white !important;
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    font-weight: 700;
    transition: all 0.2s ease;
    box-shadow: 0 6px 18px rgba(225, 29, 72, 0.20);
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: linear-gradient(135deg, #fb7185, #e11d48);
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(225, 29, 72, 0.32);
}

/* ===== SELECTBOX ===== */
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background-color: #151b2b;
    border-color: #39435c;
    border-radius: 12px;
    color: #f8fafc;
}

/* ===== DATAFRAMES ===== */
[data-testid="stDataFrame"] {
    border: 1px solid #303750;
    border-radius: 14px;
    overflow: hidden;
}

/* ===== CHART CONTAINERS ===== */
[data-testid="stVegaLiteChart"],
[data-testid="stPlotlyChart"] {
    background: rgba(21, 27, 43, 0.75);
    border: 1px solid #303750;
    border-radius: 16px;
    padding: 10px;
}

/* ===== STATUS MESSAGES ===== */
[data-testid="stAlert"] {
    border-radius: 14px;
    border: 1px solid #39435c;
}

/* ===== CUSTOM BADGE ===== */
.ai-badge {
    display: inline-block;
    background: rgba(251, 113, 133, 0.12);
    color: #fda4af;
    padding: 7px 14px;
    border: 1px solid rgba(251, 113, 133, 0.35);
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 16px;
}

/* ===== CUSTOM CARDS ===== */
.custom-card {
    background: linear-gradient(145deg, #1a2033, #121827);
    border: 1px solid #303750;
    border-radius: 18px;
    padding: 24px;
    margin-bottom: 18px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.card-title {
    color: #fda4af;
    font-size: 18px;
    font-weight: 750;
    margin-bottom: 10px;
}

.card-description {
    color: #aab5cc;
    font-size: 14px;
    line-height: 1.7;
}

/* ===== DIVIDER ===== */
hr {
    border-color: #292d42;
    margin: 28px 0;
}

/* ===== FOOTER ===== */
.footer {
    text-align: center;
    color: #77839d;
    font-size: 12px;
    padding: 28px 0 10px 0;
}

/* ===== HIDE DEFAULT DECORATIONS ===== */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="ai-badge">✦ AI-POWERED ANALYTICS</div>
    <div class="hero-title">🍽️ Zomato Review Analyzer</div>
    <div class="hero-subtitle">
        Turn customer feedback into meaningful insights.
        Explore sentiment, discover customer pain points,
        and understand restaurant review trends.
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Reviews", "1,250", "+12.5%")

with col2:
    st.metric("Positive Reviews", "78.4%", "+4.2%")

with col3:
    st.metric("Negative Reviews", "8.6%", "-1.8%")


st.markdown("""
<div class="footer">
    Zomato Review Analytics · Built with Python & Streamlit
</div>
""", unsafe_allow_html=True)

def check_ollama_connection():
    try:
        response = requests.get(
            "http://localhost:11434",
            timeout=5
        )
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def extract_json(text):
    try:
        return json.loads(text)
    except Exception:
        pass

    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    raise ValueError("No valid JSON found in the text.")


def analyze_review_with_ollama(review_text, output_language, model_name, temperature):
    system_prompt = '''
you are an expert restaurant review analyst.
you convert the unstructured customer review into clean structured buisiness reports.
Return valid JSON only.
NO Markdown
NO explanation outside of JSON.
'''
    user_prompt = f'''
analyze the following restaurant review from Zomato or Swiggy or google reviews.requests.
REVIEWS:
{review_text}

return only valid JSON with the following keys:
{{
"overall_sentiment": "positive/negative/neutral",
"estimated_review_rating": "1-5",
"one_line_summary": "short summary of the review in one line",
"summary": "short summary of the review in 2-3 lines",
"top_positive_aspects": ["list of positive aspects mentioned in the review"],
"top_negative_aspects": ["list of negative aspects mentioned in the review"],
"customer_pain_points": ["list of customer pain points mentioned in the review"],
"business_recommendations": ["list of actionable business recommendations based on the review"],
"best_for": ["families", "couples", "solo diners", "friends", "business meetings", "date nights", "special occasions"]
}}

output language: {output_language}
keep the output concise and to the point, avoid unnecessary details.request.
'''
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False,
        "options": {"temperature": temperature}
    }

    response = requests.post(
        OLLAMA_CHAT_URL,
        json=payload,
        timeout=180
    )
    response.raise_for_status()

    raw_response = response.json()["message"]["content"]
    return extract_json(raw_response)



def show_analysis_result(result):
    """Display the AI analysis as a styled report."""

    sentiment = str(
        result.get("overall_sentiment", "neutral")
    ).strip().lower()
    sentiment = html.escape(sentiment)

    sentiment_styles = {
        "positive": ("#064e3b", "#34d399", "😊"),
        "negative": ("#4c0519", "#fb7185", "😟"),
        "neutral": ("#312e81", "#c4b5fd", "😐"),
    }

    bg, accent, emoji = sentiment_styles.get(
        sentiment,
        ("#312e81", "#c4b5fd", "📊")
    )

    rating = html.escape(str(result.get("estimated_review_rating", "N/A")))
    summary = html.escape(str(result.get("summary", "No summary available.")))
    one_line = html.escape(str(result.get("one_line_summary", "")))

    st.markdown("""
    <style>
    .report-card {
        background: linear-gradient(135deg, #171d30, #111827);
        border: 1px solid #303750;
        border-radius: 16px;
        padding: 22px;
        margin: 12px 0;
    }
    .report-heading {
        color: #fda4af;
        font-size: 19px;
        font-weight: 700;
        margin-bottom: 12px;
    }
    .report-item {
        background: #20283b;
        border-radius: 10px;
        padding: 11px 14px;
        margin: 7px 0;
        color: #e2e8f0;
    }
    .report-muted {
        color: #aab5cc;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("## 📊 Review Intelligence Report")

    # Sentiment banner
    st.markdown(
        f"""
        <div style="
            background:{bg};
            border:1px solid {accent};
            border-radius:16px;
            padding:20px;
            margin:12px 0;">
            <div style="color:{accent};font-size:13px;
                        font-weight:700;">
                OVERALL SENTIMENT
            </div>
            <div style="font-size:28px;font-weight:800;
                        color:white;margin:6px 0;">
                {emoji} {sentiment.title()}
            </div>
            <div style="color:#e2e8f0;">
                {one_line}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Rating and sentiment cards
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div class="report-card">
                <div class="report-muted">⭐ Estimated Rating</div>
                <div style="font-size:30px;font-weight:800;
                            color:#fbbf24;">
                    {rating} / 5
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="report-card">
                <div class="report-muted">🎯 Main Insight</div>
                <div style="font-size:18px;font-weight:700;
                            color:#fda4af;">
                    {sentiment.title()} Experience
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Summary
    st.markdown(
        f"""
        <div class="report-card">
            <div class="report-heading">📝 Review Summary</div>
            <div style="color:#e2e8f0;line-height:1.7;">
                {summary}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    def show_list(title, key, icon, color):
        items = result.get(key, [])

        if isinstance(items, str):
            items = [items]

        if not items:
            items = ["No specific details identified."]

        st.markdown(
            f'<div class="report-card">'
            f'<div class="report-heading" style="color:{color};">'
            f'{icon} {title}</div>',
            unsafe_allow_html=True
        )

        for item in items:
            safe_item = html.escape(str(item))
            st.markdown(
                f'<div class="report-item">• {safe_item}</div>',
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # Positive and negative insights
    col1, col2 = st.columns(2)

    with col1:
        show_list(
            "Positive Aspects",
            "top_positive_aspects",
            "👍",
            "#34d399"
        )

    with col2:
        show_list(
            "Negative Aspects",
            "top_negative_aspects",
            "👎",
            "#fb7185"
        )

    show_list(
        "Customer Pain Points",
        "customer_pain_points",
        "⚠️",
        "#fbbf24"
    )

    show_list(
        "Business Recommendations",
        "business_recommendations",
        "💡",
        "#60a5fa"
    )

    show_list(
        "Best Suited For",
        "best_for",
        "🍽️",
        "#c4b5fd"
    )

    # Downloadable analysis
    st.download_button(
        "⬇️ Download Analysis (JSON)",
        data=json.dumps(result, indent=2, ensure_ascii=False),
        file_name="review_analysis.json",
        mime="application/json",
        use_container_width=True
    )



# ===== APP STATE =====

if "review_history" not in st.session_state:
    st.session_state["review_history"] = []

if "temperature" not in st.session_state:
    st.session_state["temperature"] = 0.2


# ===== SIDEBAR NAVIGATION AND SETTINGS =====

with st.sidebar:
    st.markdown("## 🍽️ Zomato AI")
    st.caption("Review Intelligence Platform")
    st.markdown("---")

    page = st.radio(
        "NAVIGATION",
        [
            "🏠 Dashboard",
            "🔍 Analyze Review",
            "📊 Sentiment Analytics",
            "📁 Review History",
            "⚙️ Settings"
        ],
        key="navigation_page"
    )

    st.markdown("---")
    st.markdown("### 🎯 Analysis Options")

    analysis_type = st.selectbox(
        "Analysis Mode",
        ["Sentiment Analysis", "Aspect-Based Analysis"]
    )

    st.checkbox("Show visualizations", value=True, key="show_charts")

    st.markdown("---")
    st.markdown("### 🌡️ AI Temperature")

    temperature = st.slider(
        "Adjust creativity",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state["temperature"],
        step=0.1,
        key="temperature",
        help="Lower values give more consistent results. Higher values allow more variation."
    )

    st.caption(f"Current temperature: {temperature:.1f}")
    st.markdown("---")
    st.caption("Powered by Python, Streamlit & Ollama")


# ===== DASHBOARD =====

history = st.session_state["review_history"]

if page == "🏠 Dashboard":
    st.title("🏠 Dashboard")
    st.write("Welcome to your Zomato Review Analytics platform.")

    total = len(history)
    positive = sum(
        1 for item in history
        if str(item["result"].get("overall_sentiment", "")).lower() == "positive"
    )
    negative = sum(
        1 for item in history
        if str(item["result"].get("overall_sentiment", "")).lower() == "negative"
    )
    neutral = total - positive - negative

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Reviews", total)
    c2.metric("Positive", positive)
    c3.metric("Negative", negative)
    c4.metric("Neutral", neutral)

    st.markdown("### 🚀 Get Started")
    st.write("Select **Analyze Review** in the sidebar to analyze customer feedback.")
    st.write("Your dashboard statistics update as you analyze reviews.")


# ===== ANALYZE REVIEW =====

elif page == "🔍 Analyze Review":
    st.title("🔍 Analyze a Review")
    st.write("Enter a restaurant review to get AI-powered insights.")

    review = st.text_area(
        "Enter customer review",
        placeholder="Example: The food was delicious, but delivery was late...",
        height=150,
        key="review_input"
    )

    if st.button(
        "✨ Analyze Review",
        use_container_width=True,
        key="run_review_analysis"
    ):
        if not review.strip():
            st.warning("Please enter a review first.")

        elif not check_ollama_connection():
            st.error(
                "Ollama is not reachable. Check that Ollama is running at "
                "http://localhost:11434."
            )

        else:
            try:
                with st.spinner("Analyzing your review with AI..."):
                    result = analyze_review_with_ollama(
                        review_text=review,
                        output_language="English",
                        model_name="llama3.2",
                        temperature=temperature
                    )

                st.session_state["review_history"].append({
                    "review": review,
                    "result": result
                })

                st.success("Review analyzed successfully!")
                show_analysis_result(result)

            except Exception as e:
                st.error(f"Analysis failed: {e}")


# ===== SENTIMENT ANALYTICS =====

elif page == "📊 Sentiment Analytics":
    st.title("📊 Sentiment Analytics")

    if not history:
        st.info("Analyze some reviews first. Your analytics will appear here.")
    else:
        sentiments = [
            str(item["result"].get("overall_sentiment", "neutral")).title()
            for item in history
        ]

        positive = sentiments.count("Positive")
        negative = sentiments.count("Negative")
        neutral = sentiments.count("Neutral")

        c1, c2, c3 = st.columns(3)
        c1.metric("😊 Positive", positive)
        c2.metric("😟 Negative", negative)
        c3.metric("😐 Neutral", neutral)

        if st.session_state["show_charts"]:
            st.subheader("Sentiment Distribution")
            st.bar_chart({
                "Positive": [positive],
                "Negative": [negative],
                "Neutral": [neutral]
            })

        st.subheader("Recent Reviews")
        for item in reversed(history[-5:]):
            sentiment = item["result"].get("overall_sentiment", "Neutral")
            st.write(f"**{str(sentiment).title()}** — {item['review']}")


# ===== REVIEW HISTORY =====

elif page == "📁 Review History":
    st.title("📁 Review History")

    if not history:
        st.info("No reviews analyzed yet.")
    else:
        for index, item in enumerate(reversed(history), start=1):
            result = item["result"]
            sentiment = result.get("overall_sentiment", "Neutral")
            rating = result.get("estimated_review_rating", "N/A")

            with st.expander(
                f"Review {len(history) - index + 1} — "
                f"{str(sentiment).title()} — Rating: {rating}/5"
            ):
                st.write(item["review"])
                st.write("**Summary:**", result.get("summary", "Not available."))

                if st.button(
                    "View Full Analysis",
                    key=f"view_history_{len(history) - index}"
                ):
                    st.session_state["selected_history_result"] = result

        if "selected_history_result" in st.session_state:
            st.divider()
            show_analysis_result(
                st.session_state["selected_history_result"]
            )

        st.download_button(
            "⬇️ Download Review History",
            data=json.dumps(
                [
                    {
                        "review": item["review"],
                        **item["result"]
                    }
                    for item in history
                ],
                indent=2,
                ensure_ascii=False
            ),
            file_name="zomato_review_history.json",
            mime="application/json"
        )

        if st.button("🗑️ Clear Review History"):
            st.session_state["review_history"] = []
            st.session_state.pop("selected_history_result", None)
            st.rerun()


# ===== SETTINGS =====

elif page == "⚙️ Settings":
    st.title("⚙️ Settings")

    st.subheader("🌡️ AI Temperature")

    st.write(
        "Temperature controls variation in the model's responses. "
        "It does not directly control sentiment or accuracy."
    )

    st.slider(
        "Temperature range",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state["temperature"],
        step=0.1,
        key="temperature_settings"
    )

    st.info(
        f"Current setting: {st.session_state['temperature']:.1f}. "
        "This value is used for your next review analysis."
    )

    if st.button("Reset Temperature to 0.2"):
        st.session_state["temperature"] = 0.2
        st.rerun()



import streamlit as st
import pandas as pd
import plotly.express as px

def show_report(results_df):
    st.markdown("## 📑 Review Intelligence Report")
    st.caption("Zomato customer feedback analytics")

    if results_df is None or results_df.empty:
        st.info("Analyze reviews first to generate the report.")
        return

    required = {"review", "sentiment"}
    if not required.issubset(results_df.columns):
        st.error("Required columns: review, sentiment")
        return

    df = results_df.copy()
    df["sentiment"] = (
        df["sentiment"].astype(str).str.strip().str.title()
    )
    valid = ["Positive", "Negative", "Neutral"]
    df = df[df["sentiment"].isin(valid)]

    if df.empty:
        st.warning("No valid sentiment predictions found.")
        return

    counts = df["sentiment"].value_counts()
    total = len(df)

    positive = counts.get("Positive", 0)
    negative = counts.get("Negative", 0)
    neutral = counts.get("Neutral", 0)

    # Summary cards
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Reviews", f"{total:,}")
    c2.metric("Positive", f"{positive / total:.1%}")
    c3.metric("Negative", f"{negative / total:.1%}")
    c4.metric("Neutral", f"{neutral / total:.1%}")

    st.divider()

    left, right = st.columns(2)

    colors = {
        "Positive": "#34d399",
        "Negative": "#fb7185",
        "Neutral": "#a78bfa",
    }

    # Donut chart
    with left:
        st.markdown("### Sentiment Distribution")
        chart_df = pd.DataFrame({
            "Sentiment": valid,
            "Reviews": [positive, negative, neutral],
        })

        fig = px.pie(
            chart_df,
            names="Sentiment",
            values="Reviews",
            hole=0.62,
            color="Sentiment",
            color_discrete_map=colors,
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0",
            margin=dict(t=20, b=20, l=10, r=10),
        )
        st.plotly_chart(fig, use_container_width=True)

    # Bar chart
    with right:
        st.markdown("### Review Breakdown")
        fig2 = px.bar(
            chart_df,
            x="Sentiment",
            y="Reviews",
            color="Sentiment",
            color_discrete_map=colors,
            text="Reviews",
        )
        fig2.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0",
            showlegend=False,
            margin=dict(t=20, b=20, l=10, r=10),
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # Review insights
    st.markdown("### 💡 Customer Feedback")

    a, b = st.columns(2)
    with a:
        st.markdown("#### 🟢 Positive Reviews")
        st.caption(f"{positive} reviews")
        for text in df.loc[
            df["sentiment"] == "Positive", "review"
        ].dropna().head(3):
            st.success(str(text))

    with b:
        st.markdown("#### 🔴 Negative Reviews")
        st.caption(f"{negative} reviews")
        for text in df.loc[
            df["sentiment"] == "Negative", "review"
        ].dropna().head(3):
            st.error(str(text))

    st.divider()

    # Filter and display the report
    st.markdown("### 📋 Detailed Review Report")
    selected = st.selectbox(
        "Filter reviews",
        ["All", "Positive", "Negative", "Neutral"],
    )

    filtered = (
        df if selected == "All"
        else df[df["sentiment"] == selected]
    )
    st.dataframe(filtered, use_container_width=True, hide_index=True)

    st.download_button(
        "⬇️ Download Report (CSV)",
        data=df.to_csv(index=False).encode("utf-8-sig"),
        file_name="zomato_review_report.csv",
        mime="text/csv",
        use_container_width=True,
    )


if page == "📑 Review Report":
    show_report(st.session_state.get("results_df"))
st.success("Review analyzed successfully!")
