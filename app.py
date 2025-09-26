# ==============================================================================
# PredictionMart: A Single-Page Informational Website
#
# Author: Group A13
# Date: September 26, 2025
#
# This script creates a complete, single-page Streamlit application.
# All content, logic, and styling are self-contained in this file for
# easy deployment on platforms like Streamlit Community Cloud.
# ==============================================================================

import streamlit as st
import pandas as pd
import altair as alt
import textwrap

# --- 1. PAGE CONFIGURATION ---
# Set the page title, icon, and layout. This must be the first Streamlit
# command in the script.
st.set_page_config(
    page_title="PredictionMart | The Future of Foresight in Asia",
    page_icon="📈",
    layout="wide"
)

# --- 2. SITE CONTENT & CONFIGURATION ---
# All text content is stored in dictionaries for easy editing. Multi-line
# strings are defined using triple quotes for readability.

SITE_CONFIG = {
    "page_title": "PredictionMart | The Future of Foresight in Asia",
    "page_icon": "📈",
    "youtube_video_id": "Gv_i2i4h5f8", # Placeholder explainer video
    "footer_email": "contact@predictionmart.dev",
    "current_year": 2025
}

CONTENT = {
    "mission_header": "Mission",
    "mission_statement": "Democratizing foresight across Asia. PredictionMart lets you invest in the likelihood of real-world events in tech, trade, economics, and geopolitics—turning collective intelligence into transparent, actionable market prices.",
    "mission_subtext": """
        We believe that the price of a contract in a prediction market is the most
        accurate forecast available. Our platform, launching from Dubai and Singapore
        with an initial focus on India, provides a transparent venue to discover
        what the crowd thinks about the future.
    """,
    "personas_header": "Who Is This For?",
    "personas": [
        {"name": "Retail Trader Rahul", "icon": "👨‍💻", "description": "Follows elections, cricket tournaments, and major economic announcements. He seeks transparent probabilities and a platform with a quick learning curve to hedge his views."},
        {"name": "Analyst Ayesha", "icon": "👩‍💼", "description": "Tracks tech IPOs and macroeconomic indicators for an investment firm. She uses PredictionMart to pressure-test her forecasts and gauge real-time market sentiment."},
        {"name": "Policy Student Sunil", "icon": "🎓", "description": "Studies public policy and international relations. He explores how our markets aggregate distributed information to create powerful forecasting tools for decision-making."}
    ],
    "what_is_header": "What is a Prediction Market?",
    "what_is_explanation": """
        A prediction market is a marketplace where people can trade contracts based on the outcomes of future events. It's similar to a stock market, but instead of buying shares in a company, you buy "Yes" or "No" shares in the outcome of an event.

        The core principle is simple: **The market price of a contract directly represents the market's consensus on the probability of that event occurring.**

        - A "Yes" share trading at **₹22** or **$0.22** implies a **22%** chance of the event happening.
        - All contracts are binary (Yes/No) and resolve to either **₹0** or **₹100** ($0 or $1).
        - If the event you bet "Yes" on occurs, your shares are worth **$1** each. If it doesn't, they are worth **$0**.
    """,
    "how_it_works_header": "How It Works: Step-By-Step",
    "how_it_works_steps": [
        "**1. Sign Up & Deposit:** Create a secure account and fund it.",
        "**2. Pick an Event:** Browse markets from tech, economics, sports, and more (e.g., 'Will India's GDP growth exceed 7% this quarter?').",
        "**3. Buy or Sell Shares:** If you believe the event will happen, buy 'Yes' shares. If not, buy 'No' shares (or sell 'Yes' shares). The price reflects the current probability.",
        "**4. Watch the Market:** Prices move in real-time as new information and opinions emerge.",
        "**5. Settlement & Payout:** When the event resolves, winning shares are paid out at $1 each. For example, if you hold 100 'Yes' shares and the event happens, you receive $100."
    ],
    "examples_header": "Example Transactions",
    "example_trades": [
        {"title": "Trade A: Buying 'Yes' on a Tech Milestone", "scenario": "Market: *'Will a specific Indian tech startup reach a $10B valuation by year-end?'*. The 'Yes' shares are currently trading at **$0.40** (a 40% probability). You are bullish and decide to invest **$100**.", "calculation": {"Investment": "$100.00", "Share Price": "$0.40", "Shares Purchased": "250 ($100 / $0.40)", "Potential Payout": "**$250.00** (250 shares x $1)", "Potential Profit": "**$150.00** ($250 - $100)"}, "outcome": "If the startup hits the valuation target, your shares pay out $250. If not, your shares settle at $0, and the investment is lost."},
        {"title": "Trade B: Realizing Profit Before Settlement", "scenario": "Market: *'Will the Reserve Bank of India cut interest rates in the next meeting?'*. You buy 'Yes' shares at **$0.60**, investing **$300**. A week later, positive economic news pushes the price up to **$0.75** as market confidence grows.", "calculation": {"Initial Investment": "$300.00", "Initial Share Price": "$0.60", "Shares Purchased": "500 ($300 / $0.60)", "New Share Price": "$0.75", "Value of Holdings": "**$375.00** (500 shares x $0.75)", "Realized Profit if Sold": "**$75.00** ($375 - $300)"}, "outcome": "You can choose to sell your 500 shares at the new price of $0.75, locking in a $75 profit without waiting for the event to resolve."}
    ],
    "widgets_header": "Interactive Tools",
    "calculator_subheader": "Payoff Calculator",
    "calculator_intro": "Use this tool to understand the potential outcomes of a trade before you make it. Adjust the sliders to see how share price and investment amount affect your potential profit and loss.",
    "youtube_subheader": "Explainer Video: The Power of Prediction Markets",
    "faq_header": "FAQ & Disclaimers",
    "faq_items": {
        "Is this investment advice?": "No. All content and tools on PredictionMart are for informational and educational purposes only. We are not financial advisors.",
        "Where is this service available?": "PredictionMart is being developed for launch from business-friendly jurisdictions like Dubai or Singapore. Availability, features, and compliance measures will depend on your local regulations.",
        "What are the risks?": "Like any market, prices can be volatile. You should only invest capital that you are prepared to lose. The value of your shares can go to zero if your prediction is incorrect."
    },
    "footer_text": "PredictionMart | Turning opinion into actionable insight."
}


# --- 3. HELPER FUNCTIONS ---
# These functions handle calculations and chart creation for the interactive widgets.

def format_currency(value, currency="USD"):
    """Formats a number as a currency string."""
    return f"${value:,.2f}"

def calculate_payoff(share_price, investment_amount, fees_percent=0.0):
    """Calculates key metrics for a prediction market trade."""
    if not (0 < share_price < 1):
        return {} # Return empty dict for invalid prices
    shares_purchased = investment_amount / share_price
    max_payout = shares_purchased * 1.0
    gross_profit = max_payout - investment_amount
    fee_amount = gross_profit * (fees_percent / 100.0)
    net_profit = gross_profit - fee_amount
    loss_if_wrong = -investment_amount
    roi = (net_profit / investment_amount) * 100 if investment_amount > 0 else 0
    return {
        "shares_purchased": shares_purchased,
        "max_payout": max_payout,
        "net_profit_if_correct": net_profit,
        "loss_if_wrong": loss_if_wrong,
        "roi_if_correct_percent": roi,
        "breakeven_prob_percent": share_price * 100
    }

def create_roi_chart(investment, fee_percent):
    """Creates an Altair chart showing ROI at different winning prices."""
    prices = [p / 100.0 for p in range(5, 100, 5)]
    data = []
    for price in prices:
        result = calculate_payoff(price, investment, fee_percent)
        if result:
            data.append({'price': price, 'roi': result['roi_if_correct_percent']})
    df = pd.DataFrame(data)
    chart = alt.Chart(df).mark_line(point=True, strokeWidth=3).encode(
        x=alt.X('price:Q', title='Purchase Price', axis=alt.Axis(format='%')),
        y=alt.Y('roi:Q', title='Potential ROI (%)'),
        tooltip=[alt.Tooltip('price:Q', title='Price', format='.2f'), alt.Tooltip('roi:Q', title='Potential ROI', format='.1f')]
    ).properties(title=alt.TitleParams(text='Potential ROI vs. Share Price', anchor='middle')).interactive()
    return chart

# --- 4. STYLING ---
# Custom CSS is injected using st.markdown to improve the visual design.
def local_css():
    st.markdown('''
    <style>
        .stApp { background-color: #F0F2F6; }
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        h1, h2, h3 { font-weight: 600; color: #1E2B3B; }
        h1 { font-size: 2.5rem; }
        h2 { font-size: 2rem; border-bottom: 2px solid #E2E8F0; padding-bottom: 0.5rem; margin-top: 3rem; margin-bottom: 1.5rem; }
        h3 { font-size: 1.5rem; margin-top: 2rem; margin-bottom: 1rem; }
        .stMetric { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 0.5rem; padding: 1rem; }
        .persona-card { background-color: white; padding: 2rem; border-radius: 0.75rem; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1); text-align: center; height: 100%; }
        .persona-icon { font-size: 3rem; }
        .sidebar .sidebar-content { background-color: #FFFFFF; }
    </style>
    ''', unsafe_allow_html=True)

local_css()

# --- 5. SIDEBAR NAVIGATION ---
# The sidebar provides quick links to different sections of the page using HTML anchors.
with st.sidebar:
    st.title("Navigation")
    st.markdown("[Mission](#mission)")
    st.markdown("[Who Is This For?](#who-is-this-for)")
    st.markdown("[What is a Prediction Market?](#what-is-a-prediction-market)")
    st.markdown("[How It Works](#how-it-works-step-by-step)")
    st.markdown("[Example Transactions](#example-transactions)")
    st.markdown("[Interactive Tools](#interactive-tools)")
    st.markdown("[FAQ & Disclaimers](#faq-disclaimers)")
    st.markdown("---")
    st.info(f"© {SITE_CONFIG['current_year']} PredictionMart. All rights reserved.")


# --- 6. MAIN PAGE LAYOUT ---
# The main content of the app is rendered below, section by section. HTML anchors
# are created using st.markdown for the sidebar links to target.

# --- SECTION: Hero ---
st.markdown('<a name="mission"></a>', unsafe_allow_html=True)
st.title(f"{SITE_CONFIG['page_icon']} PredictionMart")
st.header(CONTENT['mission_header'])
st.subheader(CONTENT['mission_statement'])
st.markdown(textwrap.dedent(CONTENT['mission_subtext']))

# --- SECTION: Personas ---
st.markdown('<a name="who-is-this-for"></a>', unsafe_allow_html=True)
st.header(CONTENT['personas_header'])
cols = st.columns(len(CONTENT['personas']))
for i, persona in enumerate(CONTENT['personas']):
    with cols[i]:
        # Using a multi-line f-string for clean HTML structure.
        persona_html = f"""
        <div class="persona-card">
            <div class="persona-icon">{persona['icon']}</div>
            <h3>{persona['name']}</h3>
            <p>{persona['description']}</p>
        </div>
        """
        st.markdown(persona_html, unsafe_allow_html=True)

# --- SECTION: What is a Prediction Market? ---
st.markdown('<a name="what-is-a-prediction-market"></a>', unsafe_allow_html=True)
st.header(CONTENT['what_is_header'])
st.markdown(textwrap.dedent(CONTENT['what_is_explanation']))

# --- SECTION: How It Works ---
st.markdown('<a name="how-it-works-step-by-step"></a>', unsafe_allow_html=True)
st.header(CONTENT['how_it_works_header'])
for step in CONTENT['how_it_works_steps']:
    st.markdown(f"- {step}")

# --- SECTION: Example Transactions ---
st.markdown('<a name="example-transactions"></a>', unsafe_allow_html=True)
st.header(CONTENT['examples_header'])
for trade in CONTENT['example_trades']:
    with st.expander(trade['title'], expanded=True):
        st.markdown(f"**Scenario:** {trade['scenario']}")
        st.markdown("---")
        cols = st.columns(2)
        with cols[0]:
            st.markdown("**Calculation:**")
            # Building the markdown table string robustly.
            table_rows = ["| Metric | Value |", "|---|---|"]
            for key, value in trade['calculation'].items():
                table_rows.append(f"| {key} | {value} |")
            st.markdown("\n".join(table_rows))

        with cols[1]:
            st.markdown("**Outcome:**")
            st.info(trade['outcome'])

# --- SECTION: Interactive Widgets ---
st.markdown('<a name="interactive-tools"></a>', unsafe_allow_html=True)
st.header(CONTENT['widgets_header'])

# Widget 1: Payoff Calculator
st.subheader(CONTENT['calculator_subheader'])
st.markdown(CONTENT['calculator_intro'])

calc_cols = st.columns([1, 2])
with calc_cols[0]:
    st.markdown("#### Inputs")
    investment_amount = st.number_input("Your Investment Amount ($)", min_value=1.0, max_value=100000.0, value=100.0, step=50.0)
    share_price = st.slider("Share Price (Implied Probability)", min_value=0.01, max_value=0.99, value=0.40, step=0.01, format="$%.2f")
    fees_percent = st.slider("Platform Fees on Profit (%)", min_value=0.0, max_value=10.0, value=1.0, step=0.5)

with calc_cols[1]:
    st.markdown("#### Potential Outcome")
    results = calculate_payoff(share_price, investment_amount, fees_percent)
    if results:
        res_cols = st.columns(3)
        res_cols[0].metric(label="Shares Purchased", value=f"{results['shares_purchased']:.2f}")
        res_cols[0].metric(label="Loss if Wrong", value=format_currency(results['loss_if_wrong']))
        res_cols[1].metric(label="Max Payout (if 'Yes')", value=format_currency(results['max_payout']))
        res_cols[1].metric(label="Potential ROI", value=f"{results['roi_if_correct_percent']:.1f}%")
        res_cols[2].metric(label="Net Profit (after fees)", value=format_currency(results['net_profit_if_correct']))
        res_cols[2].metric(label="Breakeven Probability", value=f"{results['breakeven_prob_percent']:.1f}%")

with st.expander("Show ROI vs. Purchase Price Chart"):
    st.altair_chart(create_roi_chart(investment_amount, fees_percent), use_container_width=True)

# Widget 2: YouTube Embed
st.subheader(CONTENT['youtube_subheader'])
st.video(f"https://www.youtube.com/watch?v={SITE_CONFIG['youtube_video_id']}")

# --- SECTION: FAQ & Disclaimers ---
st.markdown('<a name="faq-disclaimers"></a>', unsafe_allow_html=True)
st.header(CONTENT['faq_header'])
for question, answer in CONTENT['faq_items'].items():
    with st.expander(question):
        st.write(answer)

# --- SECTION: Footer ---
st.markdown("---")
# Using a clear, multi-line f-string for the footer HTML.
footer_html = f"""
<div style="text-align: center; padding: 1rem;">
    <p>{CONTENT['footer_text']}</p>
    <p>
        <a href="mailto:{SITE_CONFIG['footer_email']}">Contact Us</a> |
        <a href="#" target="_blank">Twitter (X)</a> |
        <a href="#" target="_blank">LinkedIn</a>
    </p>
    <p>© {SITE_CONFIG['current_year']} PredictionMart. Built with ❤️ in Asia.</p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)

# --- END OF SCRIPT ---

