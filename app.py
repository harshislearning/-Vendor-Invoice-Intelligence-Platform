import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from inference.predict_freight import predict_freight_cost
from inference.predict_invoice_flag import predict_invoice_flag

# -------------------------------------------------------
# Palette (dark surface)
# -------------------------------------------------------
PAGE_BG = "#0d0d0d"
CARD_BG = "#1a1a19"
BORDER = "rgba(255,255,255,0.10)"
TEXT_PRIMARY = "#ffffff"
TEXT_SECONDARY = "#c3c2b7"
TEXT_MUTED = "#898781"
GRIDLINE = "#2c2c2a"
ACCENT = "#3987e5"
GOOD = "#0ca30c"
WARNING = "#fab219"
CRITICAL = "#d03b3b"

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------
st.set_page_config(
    page_title="Vendor Invoice Intelligence Portal",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------------
# Global styling
# -------------------------------------------------------
st.markdown(f"""
<style>
    .stApp {{
        background-color: {PAGE_BG};
    }}

    #MainMenu, footer, header {{ visibility: hidden; }}

    .block-container {{
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }}

    /* Hero header */
    .hero {{
        background: linear-gradient(135deg, rgba(57,135,229,0.16) 0%, rgba(26,26,25,0.4) 100%);
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 2rem 2.25rem;
        margin-bottom: 1.75rem;
    }}
    .hero h1 {{
        font-size: 1.9rem;
        font-weight: 700;
        color: {TEXT_PRIMARY};
        margin: 0 0 0.35rem 0;
    }}
    .hero p {{
        color: {TEXT_SECONDARY};
        font-size: 1rem;
        margin: 0;
    }}
    .hero-tags {{
        margin-top: 1rem;
        display: flex;
        gap: 0.6rem;
        flex-wrap: wrap;
    }}
    .hero-tag {{
        background: rgba(255,255,255,0.06);
        border: 1px solid {BORDER};
        color: {TEXT_SECONDARY};
        border-radius: 999px;
        padding: 0.3rem 0.8rem;
        font-size: 0.82rem;
    }}

    /* Card container (targets st.container(key="card-...")) */
    div[class*="st-key-card-"] {{
        background-color: {CARD_BG};
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 1.6rem 1.75rem;
        margin-bottom: 1.25rem;
    }}
    .card-subtext {{
        color: {TEXT_SECONDARY};
        font-size: 0.92rem;
        margin-bottom: 1.1rem;
    }}

    /* Section label */
    .section-eyebrow {{
        color: {ACCENT};
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: {CARD_BG};
        border-right: 1px solid {BORDER};
    }}
    .sidebar-brand {{
        display: flex;
        align-items: center;
        gap: 0.6rem;
        padding: 0.25rem 0 1rem 0;
        border-bottom: 1px solid {BORDER};
        margin-bottom: 1.2rem;
    }}
    .sidebar-brand-title {{
        font-weight: 700;
        color: {TEXT_PRIMARY};
        font-size: 1.05rem;
        line-height: 1.15;
    }}
    .sidebar-brand-sub {{
        color: {TEXT_MUTED};
        font-size: 0.75rem;
    }}
    .impact-row {{
        display: flex;
        align-items: flex-start;
        gap: 0.6rem;
        padding: 0.55rem 0;
        border-bottom: 1px solid {BORDER};
    }}
    .impact-row:last-child {{ border-bottom: none; }}
    .impact-label {{
        color: {TEXT_PRIMARY};
        font-size: 0.85rem;
        font-weight: 600;
    }}
    .impact-desc {{
        color: {TEXT_MUTED};
        font-size: 0.78rem;
    }}

    /* Result badges */
    .badge {{
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.55rem 1rem;
        border-radius: 10px;
        font-weight: 700;
        font-size: 0.95rem;
    }}
    .badge-good {{
        background: rgba(12,163,12,0.15);
        color: #3fd43f;
        border: 1px solid rgba(12,163,12,0.35);
    }}
    .badge-critical {{
        background: rgba(208,59,59,0.15);
        color: #ef7373;
        border: 1px solid rgba(208,59,59,0.35);
    }}

    /* Buttons */
    .stButton > button, .stFormSubmitButton > button {{
        background-color: {ACCENT};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.55rem 1.4rem;
        font-weight: 600;
        transition: opacity 0.15s ease;
    }}
    .stButton > button:hover, .stFormSubmitButton > button:hover {{
        opacity: 0.88;
        color: white;
    }}

    hr {{ border-color: {BORDER}; }}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# Header
# -------------------------------------------------------
st.markdown("""
<div class="hero">
    <h1>📦 Vendor Invoice Intelligence Portal</h1>
    <p>AI-driven freight cost forecasting and invoice risk detection for procurement &amp; finance operations.</p>
    <div class="hero-tags">
        <span class="hero-tag">🚚 Freight Forecasting</span>
        <span class="hero-tag">🧾 Invoice Risk Scoring</span>
        <span class="hero-tag">⚙️ ML-Powered</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div style="font-size: 1.8rem;">📊</div>
        <div>
            <div class="sidebar-brand-title">Prediction Console</div>
            <div class="sidebar-brand-sub">Select an analytics module</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    selected_model = st.radio(
        "Prediction Module",
        ["Freight Cost Prediction", "Invoice Manual Approval Flag"],
        label_visibility="collapsed",
    )

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-eyebrow'>Business Impact</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="impact-row">
        <div>📉</div>
        <div>
            <div class="impact-label">Sharper Cost Forecasting</div>
            <div class="impact-desc">Anticipate freight spend before invoices land</div>
        </div>
    </div>
    <div class="impact-row">
        <div>🧾</div>
        <div>
            <div class="impact-label">Fewer Missed Anomalies</div>
            <div class="impact-desc">Automatically surface high-risk invoices</div>
        </div>
    </div>
    <div class="impact-row">
        <div>⚙️</div>
        <div>
            <div class="impact-label">Faster Finance Ops</div>
            <div class="impact-desc">Less manual review, more auto-approvals</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------
# Shared: dark plotly layout
# -------------------------------------------------------
def _dark_layout(fig, height=260):
    fig.update_layout(
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font={"color": TEXT_SECONDARY, "family": "system-ui, -apple-system, 'Segoe UI', sans-serif"},
        margin={"l": 20, "r": 20, "t": 40, "b": 20},
        height=height,
    )
    return fig

# -------------------------------------------------------
# Freight Cost Prediction
# -------------------------------------------------------
if selected_model == "Freight Cost Prediction":
    with st.container(key="card-freight-form"):
        st.markdown("<div class='section-eyebrow'>Module 01</div>", unsafe_allow_html=True)
        st.markdown("### 🚚 Freight Cost Prediction")
        st.markdown(
            "<div class='card-subtext'>Estimate freight cost for a vendor invoice from its "
            "dollar value to support budgeting, forecasting, and vendor negotiations.</div>",
            unsafe_allow_html=True,
        )

        with st.form("freight_form"):
            dollars = st.number_input("💰 Invoice Dollars", min_value=1.0, value=18500.0, step=100.0)
            submit_freight = st.form_submit_button("🔮 Predict Freight Cost")

    if submit_freight:
        prediction = predict_freight_cost({"Dollars": [dollars]})["Predicted_Freight"]
        predicted_freight = float(prediction[0])
        pct_of_dollars = (predicted_freight / dollars) * 100 if dollars else 0

        with st.container(key="card-freight-result"):
            st.markdown("#### Prediction Result")

            col1, col2 = st.columns([1, 1.4])
            with col1:
                st.metric("📊 Estimated Freight Cost", f"${predicted_freight:,.2f}")
                st.metric("📐 Freight as % of Invoice", f"{pct_of_dollars:.2f}%")

            with col2:
                fig = go.Figure(go.Bar(
                    x=["Invoice Dollars", "Predicted Freight"],
                    y=[dollars, predicted_freight],
                    marker_color=[ACCENT, "#eb6834"],
                    text=[f"${dollars:,.0f}", f"${predicted_freight:,.0f}"],
                    textposition="outside",
                    width=0.5,
                ))
                fig.update_yaxes(gridcolor=GRIDLINE, zeroline=False)
                fig.update_xaxes(gridcolor=GRIDLINE)
                fig.update_layout(title="Invoice Value vs. Predicted Freight")
                st.plotly_chart(_dark_layout(fig), use_container_width=True, config={"displayModeBar": False})

# -------------------------------------------------------
# Invoice Flag Prediction
# -------------------------------------------------------
else:
    with st.container(key="card-flag-form"):
        st.markdown("<div class='section-eyebrow'>Module 02</div>", unsafe_allow_html=True)
        st.markdown("### 🚨 Invoice Manual Approval Prediction")
        st.markdown(
            "<div class='card-subtext'>Score whether a vendor invoice should be flagged for "
            "manual approval based on abnormal cost, freight, or delivery patterns.</div>",
            unsafe_allow_html=True,
        )

        with st.form("invoice_flag_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                invoice_quantity = st.number_input("Invoice Quantity", min_value=1, value=50)
                freight = st.number_input("Freight Cost", min_value=0.0, value=1.73)
            with col2:
                invoice_dollars = st.number_input("Invoice Dollars", min_value=1.0, value=352.95)
                total_item_quantity = st.number_input("Total Item Quantity", min_value=1, value=162)
            with col3:
                total_item_dollars = st.number_input("Total Item Dollars", min_value=1.0, value=2476.0)

            submit_flag = st.form_submit_button("🧠 Evaluate Invoice Risk")

    if submit_flag:
        input_data = {
            "invoice_quantity": [invoice_quantity],
            "invoice_dollars": [invoice_dollars],
            "Freight": [freight],
            "total_item_quantity": [total_item_quantity],
            "total_item_dollars": [total_item_dollars],
        }
        result = predict_invoice_flag(input_data)
        is_flagged = bool(result["Predicted_Flag"][0])
        risk_pct = float(result["Risk_Probability"][0]) * 100

        with st.container(key="card-flag-result"):
            st.markdown("#### Risk Assessment")

            col1, col2 = st.columns([1, 1.4])
            with col1:
                if is_flagged:
                    st.markdown(
                        '<span class="badge badge-critical">🚨 MANUAL APPROVAL REQUIRED</span>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        '<span class="badge badge-good">✅ SAFE FOR AUTO-APPROVAL</span>',
                        unsafe_allow_html=True,
                    )
                st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
                st.metric("Risk Probability", f"{risk_pct:.1f}%")

            with col2:
                gauge_color = GOOD if risk_pct < 40 else (WARNING if risk_pct < 70 else CRITICAL)
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=risk_pct,
                    number={"suffix": "%", "font": {"color": TEXT_PRIMARY}},
                    gauge={
                        "axis": {"range": [0, 100], "tickcolor": TEXT_MUTED},
                        "bar": {"color": gauge_color},
                        "bgcolor": CARD_BG,
                        "borderwidth": 1,
                        "bordercolor": GRIDLINE,
                        "steps": [
                            {"range": [0, 40], "color": "rgba(12,163,12,0.15)"},
                            {"range": [40, 70], "color": "rgba(250,178,25,0.15)"},
                            {"range": [70, 100], "color": "rgba(208,59,59,0.15)"},
                        ],
                    },
                ))
                st.plotly_chart(_dark_layout(fig, height=240), use_container_width=True, config={"displayModeBar": False})
