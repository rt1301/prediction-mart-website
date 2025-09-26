import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

# Page configuration
st.set_page_config(page_title="PredictionMart", page_icon="📈", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .tagline {
        font-size: 1.2rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .context-line {
        font-size: 1rem;
        color: #9ca3af;
        font-style: italic;
        margin-bottom: 3rem;
    }
    .persona-card {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        margin-bottom: 1rem;
    }
    .section-divider {
        margin: 3rem 0;
        border-top: 2px solid #e5e7eb;
    }
    .nav-button {
        width: 100%;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Copy variables
TITLE = "PredictionMart — Trade the Future, Transparently"
TAGLINE = "Democratizing foresight across Asia. PredictionMart lets you invest in the likelihood of real-world events in tech, trade, economics, and geopolitics—turning collective intelligence into transparent market prices."
CONTEXT_LINE = "Incorporated from **Dubai or Singapore** for regulatory clarity; initial focus on East & West Asia with a strong emphasis on **India**."

PERSONAS = {
    "Retail Trader Rahul": {
        "goals": "Learn fast, act on news, see clear probabilities.",
        "markets": "Elections, cricket-adjacent policy/economy news, Big Tech launches.",
        "why": "Simple \"price ≈ probability,\" transparent $1 settlement, intuitive UI."
    },
    "Analyst Ayesha": {
        "goals": "Pressure-test theses, track macro/tech expectations, quantify sentiment.",
        "markets": "Interest rate decisions, chip supply chains, AI product timelines.",
        "why": "Aggregated beliefs in one number; movable capital to reflect conviction."
    },
    "Policy Student Sunil": {
        "goals": "Understand how markets synthesize information; practice evidence-based reasoning.",
        "markets": "Trade agreements, energy transitions, regulatory milestones.",
        "why": "Hands-on learning with verifiable outcomes and clear payoffs."
    }
}

WHAT_IS_TEXT = """
A **prediction market** lets people trade contracts linked to **verifiable future events**.

Most markets are **binary** ("Yes/No"). A **Yes** share pays **$1** if the event occurs, **$0** if not.

The **price** (between $0.00 and $1.00) is interpreted as the **probability** the event will occur.

Example: If "Will Apple ship an on-device AI iPhone by June 2026?" trades at **$0.22**, the market implies a **22%** chance.

After resolution, contracts **settle**: holders of the correct side receive **$1 per share**; the other side gets **$0**.
"""

HOW_IT_WORKS_STEPS = [
    "**Sign up** → Create an account.",
    "**Deposit funds** → Add ₹ or $ balance (jurisdiction permitting).",
    "**Pick an event** → Browse tech, trade, economics, geopolitics.",
    "**Buy shares** → Choose **Yes** or **No** based on your view.",
    "**Trade or hold** → You can sell before resolution or hold to settlement.",
    "**Settle** → When the event resolves, correct shares pay **$1**; profits are credited."
]

FAQ_ITEMS = [
    ("Is this investment advice?", "No. This site is for **information and education** where applicable."),
    ("Where is PredictionMart available?", "Availability depends on jurisdiction. We are initially set up from **Dubai or Singapore**."),
    ("What determines market resolution?", "Each market uses **public, verifiable sources** and clear rules to resolve outcomes."),
    ("Risks:", "Market prices can change rapidly; you can lose some or all of your investment. Fees and rules vary by region."),
    ("Disclaimer:", "Nothing here is a solicitation or an offer. Check your local laws before participating.")
]

# YouTube video ID (configurable)
YOUTUBE_VIDEO_ID = "dQw4w9WgXcQ"

# Helper functions
def format_currency(amount, currency="$", rate=83.0):
    """Format currency with proper symbol and conversion"""
    if currency == "₹":
        converted_amount = amount * rate
        return f"₹{converted_amount:,.2f}"
    else:
        return f"${amount:,.2f}"

def format_percentage(value):
    """Format percentage with 2 decimal places"""
    return f"{value:.2%}"

# Sidebar navigation
with st.sidebar:
    st.header("Navigation")
    
    # Navigation buttons that jump to sections
    if st.button("🎯 Mission", key="nav_mission", help="Jump to Mission section"):
        st.markdown('<script>document.getElementById("mission").scrollIntoView();</script>', unsafe_allow_html=True)
    
    if st.button("👥 Personas", key="nav_personas"):
        st.markdown('<script>document.getElementById("personas").scrollIntoView();</script>', unsafe_allow_html=True)
    
    if st.button("❓ What Is", key="nav_what_is"):
        st.markdown('<script>document.getElementById("what-is").scrollIntoView();</script>', unsafe_allow_html=True)
    
    if st.button("⚙️ How It Works", key="nav_how"):
        st.markdown('<script>document.getElementById("how-it-works").scrollIntoView();</script>', unsafe_allow_html=True)
    
    if st.button("📊 Examples", key="nav_examples"):
        st.markdown('<script>document.getElementById("examples").scrollIntoView();</script>', unsafe_allow_html=True)
    
    if st.button("🔧 Widgets", key="nav_widgets"):
        st.markdown('<script>document.getElementById("widgets").scrollIntoView();</script>', unsafe_allow_html=True)
    
    if st.button("❔ FAQ", key="nav_faq"):
        st.markdown('<script>document.getElementById("faq").scrollIntoView();</script>', unsafe_allow_html=True)

# Main content
# Hero section
st.markdown('<a id="mission"></a>', unsafe_allow_html=True)
st.markdown(f'<h1 class="main-header">{TITLE}</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="tagline">{TAGLINE}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="context-line">{CONTEXT_LINE}</p>', unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Personas section
st.markdown('<a id="personas"></a>', unsafe_allow_html=True)
st.header("👥 Our Users")

for persona_name, details in PERSONAS.items():
    st.markdown(f"""
    <div class="persona-card">
        <h4>{persona_name}</h4>
        <p><strong>Goals:</strong> {details['goals']}</p>
        <p><strong>Typical markets:</strong> {details['markets']}</p>
        <p><strong>Why PredictionMart:</strong> {details['why']}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# What is a Prediction Market section
st.markdown('<a id="what-is"></a>', unsafe_allow_html=True)
st.header("❓ What Is a Prediction Market?")
st.markdown(WHAT_IS_TEXT)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# How It Works section
st.markdown('<a id="how-it-works"></a>', unsafe_allow_html=True)
st.header("⚙️ How It Works")

for i, step in enumerate(HOW_IT_WORKS_STEPS, 1):
    st.markdown(f"{i}. {step}")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Examples section
st.markdown('<a id="examples"></a>', unsafe_allow_html=True)
st.header("📊 Example Transactions")

# Currency selector for examples
currency_col1, currency_col2 = st.columns([1, 4])
with currency_col1:
    currency = st.selectbox("Currency:", ["$", "₹"], key="examples_currency")

# Example A
st.subheader("Example A — Buy \"Yes\" and Hold to Settlement")
price_a = 0.40
investment_a = 100
shares_a = investment_a / price_a
max_payout_a = shares_a * 1.0
profit_a = max_payout_a - investment_a
loss_a = 0 - investment_a

example_a_data = {
    "Metric": ["Price", "Investment", "Shares Purchased", "Max Payout if Correct", "Profit if Correct", "Loss if Incorrect"],
    "Value": [
        f"${price_a:.2f}",
        format_currency(investment_a, currency),
        f"{shares_a:.2f}",
        format_currency(max_payout_a, currency),
        format_currency(profit_a, currency),
        format_currency(loss_a, currency)
    ]
}
st.dataframe(pd.DataFrame(example_a_data), hide_index=True)

# Example B
st.subheader("Example B — Buy \"Yes\" and Sell Before Settlement")
buy_price_b = 0.60
sell_price_b = 0.75
investment_b = 100
shares_b = investment_b / buy_price_b
proceeds_b = shares_b * sell_price_b
pnl_b = proceeds_b - investment_b

example_b_data = {
    "Metric": ["Buy Price", "Investment", "Shares Purchased", "Sell Price", "Proceeds", "P&L (before fees)"],
    "Value": [
        f"${buy_price_b:.2f}",
        format_currency(investment_b, currency),
        f"{shares_b:.2f}",
        f"${sell_price_b:.2f}",
        format_currency(proceeds_b, currency),
        format_currency(pnl_b, currency)
    ]
}
st.dataframe(pd.DataFrame(example_b_data), hide_index=True)

# Example C (Optional)
st.subheader("Example C — \"No\" Intuition (Optional)")
st.markdown("""
You can express a "No" view by buying the **No** contract when available (pays $1 if the event does **not** occur).

If **No** trades at **$0.68**, it implies a **32%** chance of "Yes." Mechanics mirror the Yes side.
""")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Widgets section
st.markdown('<a id="widgets"></a>', unsafe_allow_html=True)
st.header("🔧 Interactive Widgets")

# Widget 1: Payoff Calculator
st.subheader("Payoff Calculator")

widget_col1, widget_col2 = st.columns([1, 1])

with widget_col1:
    # Widget inputs
    share_price = st.slider("Share Price", min_value=0.01, max_value=0.99, value=0.40, step=0.01)
    
    # Currency toggle for widget
    widget_currency = st.selectbox("Currency:", ["$", "₹"], key="widget_currency")
    
    if widget_currency == "$":
        investment_amount = st.number_input("Investment Amount ($)", min_value=0.01, value=100.0, step=1.0)
    else:
        investment_amount_inr = st.number_input("Investment Amount (₹)", min_value=0.83, value=8300.0, step=83.0)
        investment_amount = investment_amount_inr / 83.0  # Convert to USD for calculations
    
    fee_percent = st.slider("Optional Fee (%)", min_value=0.0, max_value=2.0, value=0.0, step=0.1)

with widget_col2:
    # Widget outputs
    st.subheader("Results")
    
    # Validation
    if investment_amount <= 0:
        st.error("❌ Investment amount must be greater than 0")
    elif share_price < 0.01 or share_price > 0.99:
        st.warning("⚠️ Price should be between $0.01 and $0.99")
    else:
        # Calculate results
        fee_rate = fee_percent / 100
        investment_after_entry_fee = investment_amount * (1 - fee_rate)
        shares_purchased = investment_after_entry_fee / share_price
        max_payout_gross = shares_purchased * 1.0
        max_payout_after_exit_fee = max_payout_gross * (1 - fee_rate)
        breakeven_probability = share_price
        profit_if_correct = max_payout_after_exit_fee - investment_amount
        loss_if_incorrect = -investment_amount
        
        # Display results
        st.metric("Shares Purchased", f"{shares_purchased:.2f}")
        st.metric("Max Payout if Correct", format_currency(max_payout_after_exit_fee, widget_currency))
        st.metric("Breakeven Probability", format_percentage(breakeven_probability))
        st.metric("Profit if Correct", format_currency(profit_if_correct, widget_currency))
        st.metric("Loss if Incorrect", format_currency(loss_if_incorrect, widget_currency))
        
        # Optional ROI visualization
        if st.checkbox("Show ROI vs Price Chart"):
            price_range = [round(max(0.01, share_price - 0.20), 2) + i*0.01 for i in range(41)]
            roi_data = []
            for p in price_range:
                shares = investment_after_entry_fee / p
                payout = shares * 1.0 * (1 - fee_rate)
                roi = (payout - investment_amount) / investment_amount * 100
                roi_data.append({"Price": p, "ROI (%)": roi})
            
            roi_df = pd.DataFrame(roi_data)
            chart = alt.Chart(roi_df).mark_line(color='blue').add_selection(
                alt.selection_interval()
            ).encode(
                x=alt.X('Price:Q', scale=alt.Scale(domain=[min(price_range), max(price_range)])),
                y='ROI (%):Q',
                tooltip=['Price:Q', 'ROI (%):Q']
            ).properties(
                width=400,
                height=200,
                title="ROI vs Share Price"
            )
            
            # Add vertical line for current price
            current_price_line = alt.Chart(pd.DataFrame([{"Price": share_price, "ROI (%)": 0}])).mark_rule(color='red', strokeDash=[5, 5]).encode(x='Price:Q')
            
            st.altair_chart(chart + current_price_line, use_container_width=True)

# Widget 2: YouTube Embed
st.subheader("Explainer Video")
youtube_url = f"https://www.youtube.com/embed/{YOUTUBE_VIDEO_ID}"
st.markdown(f'''
<iframe width="560" height="315" src="{youtube_url}" 
frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
allowfullscreen></iframe>
''', unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# FAQ section
st.markdown('<a id="faq"></a>', unsafe_allow_html=True)
st.header("❔ FAQ & Disclaimer")

for question, answer in FAQ_ITEMS:
    st.subheader(question)
    st.markdown(answer)
    st.markdown("")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Footer
current_year = datetime.now().year
st.markdown("---")
col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("**Contact:** [hello@predictionmart.example](mailto:hello@predictionmart.example)")
with col2:
    st.markdown(f"**©** {current_year} PredictionMart. All rights reserved.")