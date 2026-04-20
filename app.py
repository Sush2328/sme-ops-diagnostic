import streamlit as st
import anthropic
import json

st.set_page_config(page_title="SME Fintech Ops Diagnostic", layout="wide", page_icon="🔍")

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500&family=Instrument+Serif:ital@0;1&display=swap');
  html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
  .hero { background: #0e0e0d; padding: 48px 40px; border-radius: 4px; margin-bottom: 32px; }
  .hero h1 { font-family: 'Instrument Serif', serif; font-size: 2.2rem; color: #f7f4ee; letter-spacing: -1px; margin-bottom: 8px; }
  .hero p { color: rgba(247,244,238,0.55); font-size: 15px; font-weight: 300; }
  .result-card { background: #f7f4ee; border-left: 3px solid #c13b20; padding: 24px; border-radius: 0 4px 4px 0; margin: 12px 0; }
  .section-label { font-size: 11px; font-weight: 500; letter-spacing: 0.14em; text-transform: uppercase; color: #7a7a76; margin-bottom: 8px; }
  .tag { display: inline-block; background: #f5ebe7; color: #c13b20; font-size: 11px; font-weight: 500; padding: 4px 10px; border-radius: 100px; margin: 3px; border: 1px solid rgba(193,59,32,0.15); }
  div[data-testid="stSelectbox"] label { font-weight: 500; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>SME Fintech Ops Diagnostic</h1>
  <p>Tell me about your company. I will tell you what is likely broken and what to fix first.</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    company_type = st.selectbox("Company type", [
        "SME neobank (business accounts, cards, payments)",
        "Payments platform (payment processing, gateway)",
        "Lending platform (SME loans, BNPL, credit)",
        "Spend management (expense cards, reimbursements)",
        "Multi-product fintech (banking + payments + lending)"
    ])

    markets = st.multiselect("Markets", [
        "Singapore", "Indonesia", "Malaysia", "Philippines",
        "Thailand", "Vietnam", "India", "UAE", "Global"
    ], default=["Singapore"])

with col2:
    stage = st.selectbox("Company stage", [
        "Early (Series A, under 50 people)",
        "Growth (Series B/C, 50 to 200 people)",
        "Scale (Series D+, 200+ people)",
        "Enterprise / Public"
    ])

    team_size = st.selectbox("Ops team size", [
        "Just getting started (1 to 5 people)",
        "Small but growing (5 to 20 people)",
        "Established team (20 to 50 people)",
        "Large ops function (50+ people)"
    ])

context = st.text_area(
    "Optional: anything specific you want diagnosed",
    placeholder="e.g. We are seeing high churn in month 2. Our payment failure rate has been rising. Our ops team is overwhelmed with manual KYC reviews...",
    height=80
)

focus = st.selectbox("Diagnostic focus", [
    "Full ops health check",
    "Payment operations and reliability",
    "Onboarding and KYC workflows",
    "Customer support and escalation",
    "Reconciliation and finance ops",
    "Compliance and audit readiness"
])

if st.button("Run Diagnostic", type="primary"):
    with st.spinner("Analysing your ops setup..."):

        prompt = f"""You are a senior ops and product consultant who has worked with 50+ fintech companies at various stages. You specialise in identifying operational failure points before they become crises.

Company profile:
- Type: {company_type}
- Markets: {', '.join(markets) if markets else 'Not specified'}
- Stage: {stage}
- Ops team: {team_size}
- Focus area: {focus}
{f'- Additional context: {context}' if context else ''}

Provide a sharp, specific operational diagnostic. Structure it exactly as follows:

## Ops Health Assessment

**Overall ops maturity:** [score out of 10 with one sentence rationale]

## Top 3 Operational Failure Points

For each failure point:
**[Name of failure point]**
- What is likely happening right now (be specific, not generic)
- The real cost of this (time, revenue, customer trust)
- Severity: [Critical / High / Medium]

## What Your Ops Team Is Probably Doing Manually Right Now

List 4 to 5 specific manual workflows that almost certainly exist at this company type and stage. Be concrete. Name the actual task, not a category.

## The 3 Systems That Should Exist But Probably Don't

For each:
- System name
- What it does in one sentence
- Why it matters at this stage specifically

## Recommended First 30 Days

Three specific, sequenced actions. Not generic advice. Tell them exactly what to build or fix first and why.

## One Thing Most Companies At This Stage Get Wrong

One sharp, opinionated insight that shows deep pattern recognition.

Be direct, specific, and opinionated. Write like someone who has seen this exact company before and knows where the bodies are buried. No filler."""

        try:
            client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
            message = client.messages.create(
                model="claude-opus-4-5",
                max_tokens=1800,
                messages=[{"role": "user", "content": prompt}]
            )
            result = message.content[0].text

            st.markdown("---")
            st.markdown(f"""
            <div style='background:#f7f4ee; border-radius:4px; padding:32px; border-left:3px solid #c13b20; font-family: DM Sans, sans-serif; line-height:1.8; white-space:pre-wrap;'>
            {result}
            </div>
            """, unsafe_allow_html=True)

            st.download_button(
                label="Download Diagnostic Report",
                data=result,
                file_name="ops_diagnostic.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Error: {e}")

st.divider()
st.markdown("""
<div style='text-align:center; padding:20px 0;'>
  <p style='font-size:13px; color:#7a7a76;'>Built by <strong>Bhavani Susmitha</strong> · IIM Ahmedabad · Ex-Revolut · <a href="https://www.linkedin.com/in/bhavanisusmitha" target="_blank" style="color:#c13b20;">LinkedIn</a></p>
  <p style='font-size:12px; color:#9a9a96; margin-top:4px;'>I built this because it is the first thing I would run on any fintech ops team I join.</p>
</div>
""", unsafe_allow_html=True)