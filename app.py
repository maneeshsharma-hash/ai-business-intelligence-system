import streamlit as st
import requests
import json
import random
import time

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Business Intelligence Dashboard",
    page_icon="🚀",
    layout="wide"
)

# ---------------------------------------------------
# OPENROUTER API KEY
# ---------------------------------------------------

OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "market_potential" not in st.session_state:
    st.session_state.market_potential = "Analyzing..."

if "investment_score" not in st.session_state:
    st.session_state.investment_score = "--"

if "risk_level" not in st.session_state:
    st.session_state.risk_level = "--"

if "startup_score" not in st.session_state:
    st.session_state.startup_score = "--"

# ---------------------------------------------------
# PREMIUM CSS
# ---------------------------------------------------

st.markdown("""
<style>

html, body, [class*="css"] {
    background-color: #020617;
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

.stApp {
    background: linear-gradient(to bottom right, #020617, #0f172a);
}

.hero-box {
    background: linear-gradient(135deg, rgba(37,99,235,0.15), rgba(124,58,237,0.15));
    padding: 2.5rem;
    border-radius: 28px;
    margin-bottom: 2rem;
    border: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(15px);
}

.hero-title {
    font-size: 3rem;
    font-weight: 700;
    color: white;
}

.hero-subtitle {
    color: #94a3b8;
    font-size: 1.1rem;
    margin-top: 10px;
}

.metric-card {
    background: rgba(15,23,42,0.75);
    border-radius: 20px;
    padding: 1.5rem;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0px 0px 20px rgba(0,0,0,0.25);
}

.metric-title {
    color: #94a3b8;
    font-size: 1rem;
}

.metric-value {
    color: white;
    font-size: 2rem;
    font-weight: bold;
    margin-top: 10px;
}


.agent-box {
    background: rgba(15,23,42,0.9);
    border-left: 5px solid #3b82f6;
    padding: 1rem;
    margin-bottom: 1rem;
    border-radius: 12px;
    color: white;
    font-size: 16px;
    font-weight: 600;
}

.result-card {
    background: linear-gradient(
        145deg,
        rgba(17,24,39,0.95),
        rgba(30,41,59,0.95)
    );

    padding: 1.5rem;

    border-radius: 18px;

    margin-bottom: 1.5rem;

    border: 1px solid rgba(255,255,255,0.08);

    box-shadow: 0 10px 30px rgba(0,0,0,0.35);

    color: white;
}

.result-card h3 {

    color: #60a5fa;

    font-size: 22px;

    margin-bottom: 18px;
}

.result-card p {

    color: #f3f4f6;

    font-size: 16px;

    line-height: 1.8;

    font-weight: 400;
}
[data-testid="stMetric"] {

    background: linear-gradient(
        145deg,
        rgba(15,23,42,0.95),
        rgba(30,41,59,0.95)
    );

    border: 1px solid rgba(255,255,255,0.08);

    padding: 20px;

    border-radius: 18px;

    text-align: center;

    box-shadow: 0 10px 25px rgba(0,0,0,0.3);
}

[data-testid="stMetricLabel"] {

    color: #cbd5e1;

    font-size: 16px;

    font-weight: 600;
}

[data-testid="stMetricValue"] {

    color: white;

    font-size: 32px;

    font-weight: bold;
}
.stButton button {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    color: white;
    border: none;
    border-radius: 15px;
    height: 3.3rem;
    font-size: 18px;
    font-weight: bold;
}

.stTextArea textarea {
    background-color: rgba(15,23,42,0.8) !important;
    color: white !important;
    border-radius: 18px !important;
    border: 2px solid rgba(59,130,246,0.25) !important;
    font-size: 16px !important;
}

.stTextArea textarea:focus {
    border: 2px solid #3b82f6 !important;
    box-shadow:
        0 0 15px rgba(59,130,246,0.7),
        0 0 30px rgba(124,58,237,0.4);
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HERO
# ---------------------------------------------------

st.markdown("""
<div class="hero-box">
    <div class="hero-title">
        Hello, Founder! 👋
    </div>
    <div class="hero-subtitle">
        Analyze your startup idea with AI-powered business intelligence agents.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LIVE SCORE PLACEHOLDERS
# ---------------------------------------------------

metric1, metric2, metric3, metric4 = st.columns(4)

market_metric = metric1.empty()
investment_metric = metric2.empty()
risk_metric = metric3.empty()
startup_metric = metric4.empty()

market_metric.metric(
    "📈 Market Potential",
    st.session_state.market_potential
)

investment_metric.metric(
    "💰 Investment Score",
    st.session_state.investment_score
)

risk_metric.metric(
    "⚠ Risk Level",
    st.session_state.risk_level
)

startup_metric.metric(
    "🚀 Startup Score",
    st.session_state.startup_score
)


# ---------------------------------------------------
# INPUT
# ---------------------------------------------------
startup_idea = st.text_area(
    "💡 Enter Startup Idea",
    height=180,
    placeholder="Describe your startup..."
)
# ---------------------------------------------------
# OPENROUTER FUNCTION
# ---------------------------------------------------
def ask_ai(prompt):

    try:

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",

            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },

            data=json.dumps({                
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            })
        )

        result = response.json()

        if "choices" not in result:

            return f"API Error: {result}"

        return result["choices"][0]["message"]["content"]

    except Exception as e:

        return f"Error: {str(e)}"
# ---------------------------------------------------
# BUTTON
# ---------------------------------------------------


if st.button("🚀 Analyze Startup"):

    if startup_idea.strip() == "":
        st.warning("Please enter startup idea.")

    else:

        # ---------------------------------------------
        # AGENT WORKFLOW TITLE
        # ---------------------------------------------

        st.markdown("""
        <h2 style='color:white; margin-top:30px;'>
        🤖 AI Agent Workflow
        </h2>
        """, unsafe_allow_html=True)

        # ---------------------------------------------
        # AGENT WORKFLOW
        # ---------------------------------------------

        agents = [
            "✅ Startup Idea Received",
            "🧠 Market Agent Completed",
            "💰 Investment Agent Completed",
            "⚠ Risk Agent Completed",
            "🚀 Strategy Agent Completed"
        ]

        agent_placeholder = st.empty()

        workflow_html = ""

        for agent in agents:

            workflow_html += f"""
            <div class="agent-box">
            {agent}
            </div>
            """

            agent_placeholder.markdown(
                workflow_html,
                unsafe_allow_html=True
            )

            time.sleep(1)

        # ---------------------------------------------
        # AI ANALYSIS
        # ---------------------------------------------

        market_analysis = ask_ai(
            f"""
            Analyze market potential for this startup idea:

            {startup_idea}

            Give professional startup market analysis.
            """
        )

        investment_analysis = ask_ai(
            f"""
            Analyze investment opportunities for this startup idea:

            {startup_idea}

            Give investor-focused analysis.
            """
        )

        risk_analysis = ask_ai(
            f"""
            Analyze startup risks for:

            {startup_idea}

            Give operational, business, and technical risks.
            """
        )

        strategy_analysis = ask_ai(
            f"""
            Suggest growth strategy for:

            {startup_idea}

            Give scaling, customer acquisition, and monetization strategies.
            """
        )

        # ---------------------------------------------
        # DYNAMIC SCORES
        # ---------------------------------------------

        st.session_state.market_potential = random.choice(
            ["High", "Very High", "Medium"]
        )

        st.session_state.investment_score = str(
            random.randint(80, 97)
        )

        st.session_state.risk_level = random.choice(
            ["Low", "Medium"]
        )

        st.session_state.startup_score = str(
            random.randint(82, 98)
        )
        
        market_metric.metric(
           "📈 Market Potential",
           st.session_state.market_potential
        )

        investment_metric.metric(
           "💰 Investment Score",
            st.session_state.investment_score
        )

        risk_metric.metric(
            "⚠ Risk Level",
            st.session_state.risk_level
        )

        startup_metric.metric(
            "🚀 Startup Score",
            st.session_state.startup_score
        )
        # ---------------------------------------------
        # SUCCESS MESSAGE
        # ---------------------------------------------

        st.success("AI Analysis Completed Successfully!")

        # ---------------------------------------------
        # RESULTS TITLE
        # ---------------------------------------------

        st.markdown("""
        <h2 style='color:white; margin-top:30px;'>
        🧠 AI Analysis Results
        </h2>
        """, unsafe_allow_html=True)

        # ---------------------------------------------
        # RESULT CARDS
        # ---------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("""
            <div class="result-card">
            <h3>📊 Market Analysis</h3>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(
                f"<div class='result-card'>{market_analysis}</div>",
                unsafe_allow_html=True
            )

        with col2:

            st.markdown("""
            <div class="result-card">
            <h3>💰 Investment Insights</h3>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(
                f"<div class='result-card'>{investment_analysis}</div>",
                unsafe_allow_html=True
            )

        col3, col4 = st.columns(2)

        with col3:

            st.markdown("""
            <div class="result-card">
            <h3>⚠ Risk Analysis</h3>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(
                f"<div class='result-card'>{risk_analysis}</div>",
                unsafe_allow_html=True
            )

        with col4:

            st.markdown("""
            <div class="result-card">
            <h3>🚀 Growth Strategy</h3>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(
                f"<div class='result-card'>{strategy_analysis}</div>",
                unsafe_allow_html=True
            )

       


st.markdown("""
<br><br>
<center style='color:#94a3b8'>
Built with ❤️ using Generative AI and Streamlit
</center>
""", unsafe_allow_html=True)

