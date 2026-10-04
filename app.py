"""
app.py
InvestorReady AI — Earnings Call Preparation Simulator
A beginner-friendly, institutional-grade financial analytics and executive preparation platform.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any

# Internal modules
import financial_engine
import risk_radar
import question_generator
import response_advisor
import mock_call_simulator

# Page configuration
st.set_page_config(
    page_title="InvestorReady AI | Earnings Call Simulator",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Institutional & Beginner-Friendly CSS
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background-color: #0b1120;
        color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Global Card */
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px 22px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        margin-bottom: 12px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .metric-title {
        font-size: 0.88rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94a3b8;
    }
    
    .metric-value {
        font-size: 2.0rem;
        font-weight: 800;
        color: #ffffff;
        margin: 6px 0;
    }
    
    .metric-delta-pos {
        color: #10b981;
        font-size: 0.92rem;
        font-weight: 700;
    }
    
    .metric-delta-neg {
        color: #ef4444;
        font-size: 0.92rem;
        font-weight: 700;
    }
    
    .simple-explainer {
        background-color: rgba(59, 130, 246, 0.12);
        border-left: 3px solid #3b82f6;
        padding: 8px 12px;
        border-radius: 0 6px 6px 0;
        font-size: 0.82rem;
        color: #93c5fd;
        margin-top: 10px;
        line-height: 1.4;
    }
    
    /* Header container */
    .header-banner {
        background: linear-gradient(90deg, #0f172a 0%, #1e3a8a 100%);
        border-bottom: 2px solid #3b82f6;
        padding: 24px 30px;
        border-radius: 12px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4);
    }
    
    .header-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.02em;
        margin-bottom: 4px;
    }
    
    .header-subtitle {
        color: #93c5fd;
        font-size: 1.05rem;
        font-weight: 400;
    }
    
    /* How it works card */
    .how-it-works-box {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #3b82f6;
        border-radius: 10px;
        padding: 16px 22px;
        margin-bottom: 22px;
    }
    
    /* Badges */
    .badge-critical {
        background-color: rgba(239, 68, 68, 0.25);
        color: #ef4444;
        border: 1px solid #ef4444;
        padding: 5px 12px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.8rem;
        text-transform: uppercase;
        display: inline-block;
    }
    
    .badge-high {
        background-color: rgba(245, 158, 11, 0.25);
        color: #f59e0b;
        border: 1px solid #f59e0b;
        padding: 5px 12px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.8rem;
        text-transform: uppercase;
        display: inline-block;
    }
    
    .callout-box {
        background-color: #1e293b;
        border-left: 4px solid #3b82f6;
        padding: 16px 20px;
        border-radius: 0 8px 8px 0;
        margin: 14px 0;
    }
</style>
""", unsafe_allow_html=True)


# Initialize Session State
if "data_source" not in st.session_state:
    st.session_state.data_source = "synthetic"

if "financial_data" not in st.session_state:
    st.session_state.financial_data = financial_engine.get_default_financial_data()
    st.session_state.segment_data = financial_engine.get_default_segment_data()
    st.session_state.commitments_data = financial_engine.get_default_commitments_data()
    st.session_state.company_name = "Apex Global Technologies Inc. (NYSE: APEX)"
    st.session_state.period_name = "Q4 FY25"

if "selected_question_id" not in st.session_state:
    st.session_state.selected_question_id = "Q_MARGIN_COMPRESSION_1"

nav_options = [
    "📊 Financial Dashboard",
    "📁 Excel Upload & Data",
    "🎯 Investor Risk Radar",
    "❓ Investor Question Generator",
    "💡 Suggested Responses",
    "🎙️ Mock Earnings Call Simulator",
]

if "nav_selection" not in st.session_state or st.session_state.nav_selection not in nav_options:
    st.session_state.nav_selection = "📊 Financial Dashboard"

if "simple_mode" not in st.session_state:
    st.session_state.simple_mode = True


# Navigation Callback Functions (executed before widgets are instantiated)
def set_page(page_name: str):
    st.session_state.nav_selection = page_name

def go_to_practice(qid: str):
    st.session_state.selected_question_id = qid
    st.session_state.nav_selection = "🎙️ Mock Earnings Call Simulator"

def apply_uploaded_data(dfs: Dict[str, pd.DataFrame], filename: str):
    st.session_state.financial_data = dfs["Financial_Results"]
    st.session_state.segment_data = dfs.get("Segment_Data", pd.DataFrame())
    st.session_state.commitments_data = dfs.get("Management_Commitments", pd.DataFrame())
    st.session_state.data_source = "uploaded"
    st.session_state.company_name = f"Uploaded File: {filename}"
    st.session_state.period_name = str(dfs["Financial_Results"].iloc[-1]["Quarter"])
    st.session_state.nav_selection = "📊 Financial Dashboard"


# Sidebar
with st.sidebar:
    st.markdown("### 🏛️ **InvestorReady AI**")
    st.caption("Earnings Call Preparation Simulator")
    st.divider()

    st.markdown("#### 🧭 Choose Section")
    nav_selection = st.radio(
        "Navigation",
        nav_options,
        key="nav_selection"
    )

    st.divider()
    st.session_state.simple_mode = st.toggle("💡 Plain-English Helper Mode", value=True, help="Shows simple translations for financial terms")

    st.divider()
    st.markdown("#### 🏢 Active Company Profile")
    st.markdown(f"**Company:** `{st.session_state.company_name}`")
    st.markdown(f"**Period:** `{st.session_state.period_name}`")
    st.markdown(f"**Data Status:** `{'Default Demo Data' if st.session_state.data_source == 'synthetic' else 'Custom Uploaded Excel'}`")

    # Sample download button
    sample_bytes = financial_engine.create_sample_excel_workbook()
    st.download_button(
        label="📥 Download Sample Excel Template",
        data=sample_bytes,
        file_name="sample_investor_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
        help="Download the complete synthetic 3-sheet Excel workbook."
    )

    if st.button("🔄 Reset to Original Demo Data", use_container_width=True):
        st.session_state.financial_data = financial_engine.get_default_financial_data()
        st.session_state.segment_data = financial_engine.get_default_segment_data()
        st.session_state.commitments_data = financial_engine.get_default_commitments_data()
        st.session_state.data_source = "synthetic"
        st.session_state.company_name = "Apex Global Technologies Inc. (NYSE: APEX)"
        st.session_state.period_name = "Q4 FY25"
        st.rerun()

    st.caption("100% Rule-Based. No Paid AI API Required.")


# Run core financial calculations
df_fin = st.session_state.financial_data
df_seg = st.session_state.segment_data
df_com = st.session_state.commitments_data

qoq = financial_engine.compute_qoq_metrics(df_fin)
risks_result = risk_radar.analyze_financial_risks(df_fin, df_seg, df_com)
questions = question_generator.generate_investor_questions(risks_result, df_fin, df_seg, df_com)
advisories = response_advisor.get_suggested_responses()


# Header Banner
st.markdown(f"""
<div class="header-banner">
    <div>
        <div class="header-title">InvestorReady AI</div>
        <div class="header-subtitle">Executive Earnings Call Simulator & Risk Radar | <strong>{st.session_state.company_name}</strong></div>
    </div>
    <div style="text-align: right;">
        <span class="badge-critical" style="font-size: 0.9rem;">⚠️ {risks_result['risk_level'].split()[0]} VULNERABILITY</span>
        <div style="font-size: 0.88rem; color: #cbd5e1; margin-top: 4px;">Wall Street Scrutiny Score: <strong>{risks_result['risk_score']}/100</strong></div>
    </div>
</div>
""", unsafe_allow_html=True)


# Quick 3-Step Walkthrough Banner (visible in Plain-English Mode)
if st.session_state.simple_mode:
    st.markdown("#### 💡 How InvestorReady AI Works in 3 Simple Steps:")
    s_col1, s_col2, s_col3 = st.columns(3)

    with s_col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border: 1px solid #3b82f6; border-radius: 10px; padding: 16px 18px; height: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                <span style="background:#3b82f6; color:#ffffff; font-weight:800; font-size:0.78rem; padding:3px 8px; border-radius:12px;">STEP 1</span>
                <span style="font-weight:700; color:#ffffff; font-size:0.95rem;">Spot the Trap 📊</span>
            </div>
            <p style="color:#cbd5e1; font-size:0.86rem; line-height:1.45; margin:0;">
                Headline sales grew <strong>+9.4%</strong>, but real profit dropped <strong>-9.7%</strong> and actual bank cash plunged <strong>-28.6%</strong>.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with s_col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border: 1px solid #f59e0b; border-radius: 10px; padding: 16px 18px; height: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                <span style="background:#f59e0b; color:#0f172a; font-weight:800; font-size:0.78rem; padding:3px 8px; border-radius:12px;">STEP 2</span>
                <span style="font-weight:700; color:#ffffff; font-size:0.95rem;">Find the Risks 🎯</span>
            </div>
            <p style="color:#cbd5e1; font-size:0.86rem; line-height:1.45; margin:0;">
                The <strong>Risk Radar</strong> automatically detects why: cheap hardware diluted profit, receivables are unpaid, and public guidance was missed.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with s_col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border: 1px solid #10b981; border-radius: 10px; padding: 16px 18px; height: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                <span style="background:#10b981; color:#0f172a; font-weight:800; font-size:0.78rem; padding:3px 8px; border-radius:12px;">STEP 3</span>
                <span style="font-weight:700; color:#ffffff; font-size:0.95rem;">Rehearse with AI 🎙️</span>
            </div>
            <p style="color:#cbd5e1; font-size:0.86rem; line-height:1.45; margin:0;">
                Anticipate tough Wall Street questions, test your answers in the <strong>Mock Simulator</strong>, and get an objective 0–100 score in 1 second.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 1. FINANCIAL DASHBOARD
# ==========================================
if nav_selection == "📊 Financial Dashboard":
    st.subheader(f"📊 Financial Dashboard: {qoq.get('prev_quarter', 'Q3')} vs {qoq.get('latest_quarter', 'Q4')}")
    st.markdown("Here are the company's headline numbers comparing the latest quarter with the prior quarter.")

    # 4 Main KPI Cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        rev_val = qoq.get("rev_latest", 0)
        rev_qoq = qoq.get("rev_qoq_pct", 0)
        explainer = "Sales grew from $139M to $152M (+9.4%). On the surface, the company looks healthy." if st.session_state.simple_mode else ""
        st.markdown(f"""
        <div class="metric-card">
            <div>
                <div class="metric-title">1. Total Revenue (Sales)</div>
                <div class="metric-value">${rev_val:,.1f}M</div>
                <div class="{'metric-delta-pos' if rev_qoq >= 0 else 'metric-delta-neg'}">
                    {'▲' if rev_qoq >= 0 else '▼'} {rev_qoq:+.1f}% vs last quarter
                </div>
            </div>
            {f'<div class="simple-explainer">💡 <strong>In Plain English:</strong> {explainer}</div>' if explainer else ''}
        </div>
        """, unsafe_allow_html=True)

    with col2:
        op_val = qoq.get("op_latest", 0)
        op_qoq = qoq.get("op_qoq_pct", 0)
        explainer = "Profit dropped from $23.6M to $21.3M (-9.7%) because costs grew faster than sales!" if st.session_state.simple_mode else ""
        st.markdown(f"""
        <div class="metric-card">
            <div>
                <div class="metric-title">2. Operating Profit (EBIT)</div>
                <div class="metric-value">${op_val:,.1f}M</div>
                <div class="{'metric-delta-pos' if op_qoq >= 0 else 'metric-delta-neg'}">
                    {'▲' if op_qoq >= 0 else '▼'} {op_qoq:+.1f}% vs last quarter
                </div>
            </div>
            {f'<div class="simple-explainer" style="border-left-color:#ef4444; color:#fca5a5;">💡 <strong>In Plain English:</strong> {explainer}</div>' if explainer else ''}
        </div>
        """, unsafe_allow_html=True)

    with col3:
        margin_val = qoq.get("margin_latest", 0)
        margin_bps = qoq.get("margin_diff_bps", 0)
        explainer = "Out of every $100 sold, the company kept only $14.01 in profit, down from $17.00." if st.session_state.simple_mode else ""
        st.markdown(f"""
        <div class="metric-card">
            <div>
                <div class="metric-title">3. Profit Margin %</div>
                <div class="metric-value">{margin_val:.1f}%</div>
                <div class="metric-delta-neg">
                    ▼ {abs(margin_bps):.0f} bps drop (from {qoq.get('margin_prev', 0):.1f}%)
                </div>
            </div>
            {f'<div class="simple-explainer" style="border-left-color:#ef4444; color:#fca5a5;">💡 <strong>In Plain English:</strong> {explainer}</div>' if explainer else ''}
        </div>
        """, unsafe_allow_html=True)

    with col4:
        ocf_val = qoq.get("ocf_latest", 0)
        ocf_qoq = qoq.get("ocf_qoq_pct", 0)
        conv_val = qoq.get("conv_latest", 0)
        explainer = "Real cash received fell to $13.2M. There is an $8.1M gap stuck in unpaid customer bills!" if st.session_state.simple_mode else ""
        st.markdown(f"""
        <div class="metric-card">
            <div>
                <div class="metric-title">4. Real Cash Flow (OCF)</div>
                <div class="metric-value">${ocf_val:,.1f}M</div>
                <div class="metric-delta-neg">
                    ▼ {abs(ocf_qoq):.1f}% drop (Cash Conv: {conv_val:.0f}%)
                </div>
            </div>
            {f'<div class="simple-explainer" style="border-left-color:#f59e0b; color:#fde68a;">💡 <strong>In Plain English:</strong> {explainer}</div>' if explainer else ''}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts Row 1
    ch_col1, ch_col2 = st.columns(2)

    with ch_col1:
        st.markdown("##### 📈 Chart 1: The Divergence (Sales Going Up, Profits Going Down)")
        if st.session_state.simple_mode:
            st.caption("Notice how the blue bars (Revenue) keep climbing, while green bars (Profit) started declining in Q4.")
        fig_rev_op = go.Figure()
        fig_rev_op.add_trace(go.Bar(
            x=df_fin["Quarter"],
            y=df_fin["Revenue"],
            name="Revenue (Total Sales) $M",
            marker_color="#3b82f6"
        ))
        fig_rev_op.add_trace(go.Bar(
            x=df_fin["Quarter"],
            y=df_fin["Operating_Profit"],
            name="Operating Profit $M",
            marker_color="#10b981"
        ))
        fig_rev_op.update_layout(
            barmode="group",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15,23,42,0.6)",
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_rev_op, use_container_width=True)

    with ch_col2:
        st.markdown("##### 📉 Chart 2: Profit Margin Fall vs. The 18% Promise")
        if st.session_state.simple_mode:
            st.caption("Management promised an 18% margin (dashed orange line), but actual margin collapsed to 14% (red line).")
        fig_margin = go.Figure()
        fig_margin.add_trace(go.Scatter(
            x=df_fin["Quarter"],
            y=df_fin["Operating_Margin_Pct"],
            mode="lines+markers+text",
            text=[f"{v:.1f}%" for v in df_fin["Operating_Margin_Pct"]],
            textposition="top center",
            name="Actual Margin (%)",
            line=dict(color="#ef4444", width=3),
            marker=dict(size=8)
        ))
        fig_margin.add_hline(
            y=18.0,
            line_dash="dash",
            line_color="#f59e0b",
            annotation_text="Management Promise (18.0%)",
            annotation_position="bottom right"
        )
        fig_margin.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15,23,42,0.6)",
            yaxis=dict(range=[10, 24], title="Margin %"),
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_margin, use_container_width=True)

    # Next step button
    st.divider()
    c_btn1, c_btn2 = st.columns([3, 1])
    with c_btn1:
        st.markdown("👉 **Ready to see what risks investors will attack based on these charts?**")
    with c_btn2:
        st.button("See Risk Radar 🎯", type="primary", use_container_width=True, on_click=set_page, args=("🎯 Investor Risk Radar",))


# ==========================================
# 2. EXCEL UPLOAD & DATA EXPLORER
# ==========================================
elif nav_selection == "📁 Excel Upload & Data":
    st.subheader("📁 Upload Your Own Excel File or View Demo Data")
    st.markdown("You can upload any company's quarterly results Excel workbook, or use our built-in sample file.")

    upload_col1, upload_col2 = st.columns([3, 2])

    with upload_col1:
        uploaded_file = st.file_uploader(
            "Select an Excel file (.xlsx or .xls)",
            type=["xlsx", "xls"],
            help="Must contain a sheet named 'Financial_Results' with columns: Quarter, Revenue, Operating_Profit, Operating_Cash_Flow"
        )

        if uploaded_file is not None:
            is_valid, dataframes, msg = financial_engine.parse_and_validate_excel(uploaded_file)
            if is_valid:
                st.success(f"✅ {msg}")
                st.button("Apply Uploaded Data to App", type="primary", on_click=apply_uploaded_data, args=(dataframes, uploaded_file.name))
            else:
                st.error(f"❌ Could not load file: {msg}")

    with upload_col2:
        st.markdown("""
        <div class="callout-box">
            <h5 style="color:#60a5fa; margin-top:0;">💡 How the Excel File is Structured</h5>
            <p style="font-size:0.85rem; color:#cbd5e1; margin-bottom:6px;">Your Excel file needs 4 simple columns:</p>
            <ul style="font-size:0.85rem; color:#94a3b8; padding-left:18px;">
                <li><code>Quarter</code> (e.g. Q1, Q2, Q3, Q4)</li>
                <li><code>Revenue</code> (Total sales in millions)</li>
                <li><code>Operating_Profit</code> (Earnings before interest/tax)</li>
                <li><code>Operating_Cash_Flow</code> (Real cash collected)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.download_button(
            label="📥 Download Sample Excel File to Inspect",
            data=sample_bytes,
            file_name="sample_investor_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    st.divider()
    st.markdown("#### 🔍 Active Data Preview")
    tab1, tab2, tab3 = st.tabs(["Headline Financials", "Segment Breakdown", "Management Promises & Targets"])

    with tab1:
        st.dataframe(st.session_state.financial_data, use_container_width=True)
    with tab2:
        st.dataframe(st.session_state.segment_data, use_container_width=True)
    with tab3:
        st.dataframe(st.session_state.commitments_data, use_container_width=True)


# ==========================================
# 3. INVESTOR RISK RADAR
# ==========================================
elif nav_selection == "🎯 Investor Risk Radar":
    st.subheader("🎯 Investor Risk Radar: The 4 Red Flags Detected")
    st.markdown("Our rule-based engine detected 4 key financial traps that will make analysts grill leadership on the call.")

    # 4 Simple Explanatory Cards
    for idx, r in enumerate(risks_result["risks"], 1):
        badge_class = "badge-critical" if r["severity"] == "CRITICAL" else "badge-high"
        
        # Simple plain-English header
        plain_title = ""
        if "MARGIN" in r["id"]:
            plain_title = "Trap 1: The 'Margin Squeeze' — Selling More, Keeping Less"
        elif "CASH" in r["id"]:
            plain_title = "Trap 2: The 'Cash Gap' — Profit on Paper, But Empty Bank Accounts"
        elif "SEGMENT" in r["id"]:
            plain_title = "Trap 3: The 'Cheap Product Trap' — Low-Profit Hardware Booming, Software Stalled"
        elif "COMMITMENT" in r["id"]:
            plain_title = "Trap 4: The 'Broken Promise' — Missed Public Margin & Cash Targets"

        with st.expander(f"{r['icon']} {plain_title} [{r['severity']}]", expanded=True):
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                <span class="{badge_class}">{r['severity']} PRIORITY</span>
                <span style="font-size:0.85rem; color:#94a3b8;">Technical Name: <strong>{r['title']}</strong></span>
            </div>
            <div style="font-size:1.05rem; font-weight:700; color:#ffffff; margin-bottom:6px;">{r['summary']}</div>
            <div style="background:#0f172a; border-left:4px solid #3b82f6; padding:10px 14px; border-radius:0 6px 6px 0; margin-bottom:12px; font-size:0.9rem; color:#93c5fd;">
                💡 <strong>Why Investors Care:</strong> {r['why_flagged']}
            </div>
            """, unsafe_allow_html=True)

            st.markdown("**📊 Exact Figures Supporting This Flag:**")
            ev_cols = st.columns(len(r["evidence"]))
            for c, (k, v) in zip(ev_cols, r["evidence"].items()):
                c.markdown(f"""
                <div style="background:#1e293b; padding:10px 14px; border-radius:6px; border:1px solid #334155;">
                    <div style="font-size:0.75rem; color:#94a3b8; font-weight:600;">{k}</div>
                    <div style="font-size:0.95rem; font-weight:700; color:#ffffff; margin-top:2px;">{v}</div>
                </div>
                """, unsafe_allow_html=True)

    st.divider()
    c_btn1, c_btn2 = st.columns([3, 1])
    with c_btn1:
        st.markdown("👉 **See the exact questions Wall Street analysts will ask based on these 4 traps:**")
    with c_btn2:
        st.button("Generate Questions ❓", type="primary", use_container_width=True, on_click=set_page, args=("❓ Investor Question Generator",))


# ==========================================
# 4. INVESTOR QUESTION GENERATOR
# ==========================================
elif nav_selection == "❓ Investor Question Generator":
    st.subheader("❓ Wall Street Analyst Questions Generated for You")
    st.markdown("Here are the real, hard-hitting questions Wall Street analysts will ask based on the detected risks.")

    for q in questions:
        badge_class = "badge-critical" if q["priority"] == "CRITICAL" else "badge-high"
        with st.container():
            st.markdown(f"""
            <div style="background:#1e293b; border:1px solid #334155; border-radius:10px; padding:20px; margin-bottom:18px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <span class="{badge_class}">{q['priority']} QUESTION</span>
                    <span style="font-size:0.85rem; color:#93c5fd;">Asked by: <strong>{q['analyst_archetype']}</strong></span>
                </div>
                <div style="font-size:1.15rem; font-weight:700; color:#ffffff; line-height:1.45; margin-bottom:14px;">
                    "{q['question']}"
                </div>
                <div style="background:#0f172a; border-radius:6px; padding:12px 16px; margin-bottom:12px;">
                    <div style="font-size:0.8rem; font-weight:700; color:#f59e0b; text-transform:uppercase;">🕵️ What the Analyst is Suspecting:</div>
                    <div style="font-size:0.9rem; color:#cbd5e1; margin-top:2px;">{q['what_analysts_suspect']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_ev, col_mis, col_act = st.columns([3, 3, 2])
            with col_ev:
                st.markdown("**Evidence Cited in Question:**")
                for ev in q["financial_evidence"]:
                    st.markdown(f"- `{ev}`")
            with col_mis:
                st.markdown("**Missing Info They Will Demand:**")
                for mis in q["missing_information"]:
                    st.markdown(f"- {mis}")
            with col_act:
                st.button(f"🎙️ Practice This Question", key=f"btn_practice_{q['id']}", use_container_width=True, on_click=go_to_practice, args=(q['id'],))


# ==========================================
# 5. SUGGESTED RESPONSES & EVIDENCE BRIDGE
# ==========================================
elif nav_selection == "💡 Suggested Responses":
    st.subheader("💡 Expert Draft Responses & Rules to Follow")
    st.markdown("Here is how a seasoned CFO would answer these tough questions, and what mistakes to avoid.")

    q_options = {q["id"]: f"[{q['priority']}] {q['question'][:90]}..." for q in questions}

    selected_q_id = st.selectbox(
        "Select an Analyst Question to View the Recommended Answer:",
        options=list(q_options.keys()),
        format_func=lambda x: q_options[x]
    )

    adv = advisories.get(selected_q_id)
    target_q = next((q for q in questions if q["id"] == selected_q_id), None)

    if adv and target_q:
        st.markdown(f"""
        <div class="callout-box" style="border-left-color: #3b82f6;">
            <div style="font-size:0.8rem; font-weight:700; color:#60a5fa; text-transform:uppercase;">Question:</div>
            <div style="font-size:1.05rem; font-weight:600; color:#ffffff; margin-top:4px;">"{target_q['question']}"</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 🎙️ Recommended Executive Answer:")
        st.markdown(f"""
        <div style="background:#0f172a; border:1px solid #1e3a8a; border-radius:8px; padding:22px; font-size:0.98rem; line-height:1.6; color:#f8fafc; white-space:pre-wrap;">
{adv['suggested_draft_response']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        r_col1, r_col2 = st.columns(2)

        with r_col1:
            st.markdown("##### ✅ Numbers You Can Safely Cite")
            for ea in adv["evidentiary_anchors"]:
                st.markdown(f"- `{ea}`")

            st.markdown("##### 🚫 Mistakes to Strictly Avoid")
            for ua in adv["unsupported_assumptions_to_avoid"]:
                st.markdown(f"- ⚠️ <span style='color:#f87171;'>{ua}</span>", unsafe_allow_html=True)

        with r_col2:
            st.markdown("##### 📌 Details Still Awaiting Confirmation")
            for dg in adv["missing_evidence_and_data_gaps"]:
                st.markdown(f"- {dg}")

            st.markdown(f"""
            <div style="background:rgba(239, 68, 68, 0.1); border:1px solid #ef4444; border-radius:8px; padding:12px; margin-top:14px;">
                <div style="font-size:0.75rem; font-weight:700; color:#ef4444; text-transform:uppercase;">Legal Notice:</div>
                <div style="font-size:0.82rem; color:#fca5a5;">{adv['compliance_disclaimer']}</div>
            </div>
            """, unsafe_allow_html=True)


# ==========================================
# 6. MOCK EARNINGS CALL SIMULATOR
# ==========================================
elif nav_selection == "🎙️ Mock Earnings Call Simulator":
    st.subheader("🎙️ Interactive Rehearsal Simulator: Practice Your Answer")
    st.markdown("Select a question, type your response (or test with our 1-click sample answers), and watch the AI score it!")

    # Question Selector
    q_map = {q["id"]: f"[{q['priority']}] {q['question'][:100]}..." for q in questions}
    default_index = 0
    if st.session_state.selected_question_id in q_map:
        default_index = list(q_map.keys()).index(st.session_state.selected_question_id)

    chosen_qid = st.selectbox(
        "Choose an Analyst Question to Rehearse:",
        options=list(q_map.keys()),
        index=default_index,
        format_func=lambda x: q_map[x]
    )

    current_q = next((q for q in questions if q["id"] == chosen_qid), None)

    if current_q:
        badge_class = "badge-critical" if current_q["priority"] == "CRITICAL" else "badge-high"
        st.markdown(f"""
        <div style="background:#1e293b; border-left:4px solid {'#ef4444' if current_q['priority'] == 'CRITICAL' else '#f59e0b'}; border-radius:0 8px 8px 0; padding:18px 22px; margin:16px 0;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="{badge_class}">{current_q['priority']} QUESTION</span>
                <span style="font-size:0.85rem; color:#93c5fd;">Analyst: <strong>{current_q['analyst_archetype']}</strong></span>
            </div>
            <div style="font-size:1.15rem; font-weight:700; color:#ffffff; margin-top:8px;">"{current_q['question']}"</div>
            <div style="margin-top:10px; font-size:0.85rem; color:#cbd5e1;">
                <strong>Figures in Question:</strong> {', '.join(current_q['financial_evidence'])}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 1-Click Demo Buttons for Instant Testing!
        st.markdown("##### ⚡ Quick Demonstration Buttons (Click to Test Without Typing):")
        d_col1, d_col2 = st.columns(2)

        good_text = (
            "Thank you. We acknowledge that our Q4 operating margin contracted by 300 basis points to 14.0% with operating profit "
            "at $21.3M, despite revenue growing 9.4% to $152.0M. The primary driver was a product mix shift: Hardware & Edge Systems "
            "grew 25.9% to $68.0M with a 7.9% margin, while Enterprise Cloud SaaS remained at $45.0M with a 27.1% margin. "
            "We are executing cost containment on delivery overhead and raising pricing hurdles to restore operating leverage."
        )

        bad_text = (
            "We remain cautiously optimistic about our long-term trajectory. There are always temporary headwinds and macro volatility, "
            "but we are laser focused on unlocking synergies across our divisions. Rest assured, we guarantee that margins will bounce "
            "back to unprecedented levels next quarter. We have zero risk of further slowdown."
        )

        with d_col1:
            if st.button("🟢 Load a Strong Answer (See High Score ~90/100)", use_container_width=True):
                st.session_state[f"input_{chosen_qid}"] = good_text
                st.rerun()

        with d_col2:
            if st.button("🔴 Load a Weak Fluffy Answer (See Jargon Penalties ~40/100)", use_container_width=True):
                st.session_state[f"input_{chosen_qid}"] = bad_text
                st.rerun()

        # Text input area
        user_answer = st.text_area(
            "Draft Your Answer Here:",
            height=160,
            placeholder="Type your response or click one of the buttons above to load an instant demonstration answer...",
            key=f"input_{chosen_qid}"
        )

        eval_btn = st.button("Evaluate My Answer 📊", type="primary", use_container_width=True)

        if eval_btn or user_answer:
            eval_result = mock_call_simulator.evaluate_mock_response(
                user_answer,
                current_q,
                qoq
            )

            st.markdown("---")
            st.markdown("### 🏆 Instant Evaluation Scorecard")

            score_col1, score_col2 = st.columns([2, 5])
            with score_col1:
                score = eval_result["score"]
                color = eval_result["rating_color"]
                st.markdown(f"""
                <div style="background:#0f172a; border:2px solid {color}; border-radius:12px; padding:24px; text-align:center;">
                    <div style="font-size:0.85rem; font-weight:700; color:#94a3b8; text-transform:uppercase;">Call Readiness Score</div>
                    <div style="font-size:3.5rem; font-weight:900; color:{color}; line-height:1.1;">{score}<span style="font-size:1.5rem;">/100</span></div>
                    <div style="font-size:1.0rem; font-weight:700; color:#ffffff; margin-top:8px;">{eval_result['rating']}</div>
                </div>
                """, unsafe_allow_html=True)

            with score_col2:
                st.markdown(f"**Diagnostic Summary:** {eval_result['summary']}")

                if eval_result["flagged_buzzwords"]:
                    st.markdown(f"🚨 **Flagged Empty Buzzwords:** {', '.join([f'`{b}`' for b in eval_result['flagged_buzzwords']])}")
                else:
                    st.markdown("✅ **Jargon Check:** Clean language. No empty corporate buzzwords detected.")

                if eval_result["metrics_detected"]:
                    st.markdown(f"📊 **Financial Numbers Detected:** {', '.join([f'`{m}`' for m in eval_result['metrics_detected'][:5]])}")

                st.markdown("**💡 How to Improve Your Score:**")
                for tip in eval_result["coaching_tips"]:
                    st.markdown(f"- {tip}")

            # Checklist breakdown
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("##### 📋 Transparent 5-Point Checklist Breakdown")
            for item in eval_result["checklist"]:
                with st.expander(f"{item['item']} — {item['status']} ({item['score']}/{item['max']} pts)", expanded=True):
                    st.write(item["feedback"])
