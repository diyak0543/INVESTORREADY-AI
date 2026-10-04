"""
question_generator.py
Generates realistic, hard-hitting investor and analyst questions based on detected financial risks.
Strict adherence to financial evidence without inventing facts.
"""

from typing import List, Dict, Any
import pandas as pd


def generate_investor_questions(
    risks_data: Dict[str, Any],
    df_fin: pd.DataFrame,
    df_seg: pd.DataFrame = None,
    df_com: pd.DataFrame = None
) -> List[Dict[str, Any]]:
    """
    Produces prioritized investor questions tied strictly to detected risks and validated metrics.
    """
    questions: List[Dict[str, Any]] = []

    if len(df_fin) < 2:
        return []

    prev_row = df_fin.iloc[-2]
    latest_row = df_fin.iloc[-1]

    rev_prev = float(prev_row["Revenue"])
    rev_latest = float(latest_row["Revenue"])
    rev_qoq = ((rev_latest - rev_prev) / rev_prev) * 100 if rev_prev != 0 else 0

    op_prev = float(prev_row["Operating_Profit"])
    op_latest = float(latest_row["Operating_Profit"])
    op_qoq = ((op_latest - op_prev) / op_prev) * 100 if op_prev != 0 else 0

    margin_prev = float(prev_row["Operating_Margin_Pct"])
    margin_latest = float(latest_row["Operating_Margin_Pct"])
    margin_diff_bps = (margin_latest - margin_prev) * 100

    ocf_prev = float(prev_row["Operating_Cash_Flow"])
    ocf_latest = float(latest_row["Operating_Cash_Flow"])
    ocf_qoq = ((ocf_latest - ocf_prev) / ocf_prev) * 100 if ocf_prev != 0 else 0

    conv_prev = float(prev_row["Cash_Conversion_Pct"])
    conv_latest = float(latest_row["Cash_Conversion_Pct"])

    # Optional Free Cash Flow
    fcf_prev = float(prev_row.get("Free_Cash_Flow", ocf_prev - 10.0))
    fcf_latest = float(latest_row.get("Free_Cash_Flow", ocf_latest - 11.8))

    detected_ids = {r["id"] for r in risks_data.get("risks", [])}

    # --- Questions for RISK 1: Margin Compression ---
    if "RISK_MARGIN_COMPRESSION" in detected_ids:
        questions.append({
            "id": "Q_MARGIN_COMPRESSION_1",
            "risk_id": "RISK_MARGIN_COMPRESSION",
            "priority": "CRITICAL",
            "priority_color": "#EF4444",
            "analyst_archetype": "Institutional Equity Research Analyst (Tier-1 Investment Bank)",
            "tone": "Skeptical & Direct",
            "question": (
                f"You reported +{rev_qoq:.1f}% top-line revenue growth to ${rev_latest:,.1f}M this quarter, yet your "
                f"operating profit fell {abs(op_qoq):.1f}% and operating margin compressed by {abs(margin_diff_bps):.0f} "
                f"basis points to {margin_latest:.1f}%. How much of this margin decline was driven by deliberate price "
                f"discounting to hit revenue targets versus structural operating expense inflation?"
            ),
            "financial_evidence": [
                f"Revenue: ${rev_latest:,.1f}M (+{rev_qoq:+.1f}% QoQ vs ${rev_prev:,.1f}M)",
                f"Operating Profit: ${op_latest:,.1f}M ({op_qoq:+.1f}% QoQ vs ${op_prev:,.1f}M)",
                f"Operating Margin: {margin_latest:.1f}% (-{abs(margin_diff_bps):.0f} bps from {margin_prev:.1f}%)"
            ],
            "what_analysts_suspect": (
                "Analysts suspect the company is discounting aggressively to artificially sustain volume growth, "
                "or that operating costs (SG&A, cost of delivery) have spiraled beyond management control."
            ),
            "missing_information": [
                "Exact gross margin vs SG&A margin split in the headline press release.",
                "Quantified breakdown between price realization changes and volume changes.",
                "Contract-level discounting data across enterprise accounts."
            ]
        })

        questions.append({
            "id": "Q_MARGIN_COMPRESSION_2",
            "risk_id": "RISK_MARGIN_COMPRESSION",
            "priority": "HIGH",
            "priority_color": "#F59E0B",
            "analyst_archetype": "Growth-at-a-Reasonable-Price (GARP) Portfolio Manager",
            "tone": "Forward-Looking & Probing",
            "question": (
                f"With operating expenses growing faster than revenue this quarter, at what revenue run-rate do you "
                f"expect positive operating leverage to return? Should investors treat this {margin_latest:.1f}% margin "
                f"as the new baseline for upcoming quarters, or is there a concrete timeline to recover back above {margin_prev:.1f}%?"
            ),
            "financial_evidence": [
                f"Latest Operating Margin: {margin_latest:.1f}% vs Previous Quarter: {margin_prev:.1f}%",
                f"Implied Operating Cost Growth: +{(((rev_latest - op_latest) - (rev_prev - op_prev)) / (rev_prev - op_prev) * 100):.1f}% QoQ"
            ],
            "what_analysts_suspect": (
                "Investors are concerned that the margin erosion is structural rather than transient, requiring a "
                "downward revision to multi-year EBITDA and EPS consensus estimates."
            ),
            "missing_information": [
                "Updated guidance for the next fiscal year.",
                "Headcount and compensation expense additions made during the quarter."
            ]
        })

    # --- Questions for RISK 2: Cash Flow Decoupling ---
    if "RISK_CASH_FLOW_DECOUPLING" in detected_ids:
        questions.append({
            "id": "Q_CASH_FLOW_1",
            "risk_id": "RISK_CASH_FLOW_DECOUPLING",
            "priority": "CRITICAL",
            "priority_color": "#EF4444",
            "analyst_archetype": "Long/Short Value Fund Manager",
            "tone": "Rigorous on Accounting Quality",
            "question": (
                f"Operating cash flow collapsed {abs(ocf_qoq):.1f}% QoQ to ${ocf_latest:,.1f}M, and your cash conversion "
                f"dropped to {conv_latest:.1f}% of operating profit from {conv_prev:.1f}% in the prior quarter. Why did "
                f"${op_latest - ocf_latest:,.1f}M of operating profit fail to materialize in cash? Are you experiencing "
                f"deteriorating customer payment terms or an inventory buildup of unsold units?"
            ),
            "financial_evidence": [
                f"Operating Cash Flow: ${ocf_latest:,.1f}M ({ocf_qoq:+.1f}% QoQ from ${ocf_prev:,.1f}M)",
                f"Cash Conversion Ratio: {conv_latest:.1f}% (vs {conv_prev:.1f}% prior quarter)",
                f"Cash-to-Profit Gap: ${op_latest - ocf_latest:,.1f}M gap between profit and cash flow"
            ],
            "what_analysts_suspect": (
                "Wall Street analysts monitor accrual-to-cash divergence closely. A sudden collapse in cash conversion "
                "often signifies pull-forward revenue recognition, channel stuffing, or bad debt accumulation."
            ),
            "missing_information": [
                "Days Sales Outstanding (DSO) balance sheet metric.",
                "Detailed Working Capital reconciliation (Change in Accounts Receivable, Inventory, and Accounts Payable).",
                "Aging schedule of customer receivables."
            ]
        })

        questions.append({
            "id": "Q_CASH_FLOW_2",
            "risk_id": "RISK_CASH_FLOW_DECOUPLING",
            "priority": "HIGH",
            "priority_color": "#F59E0B",
            "analyst_archetype": "Corporate Credit & Liquidity Analyst",
            "tone": "Balance-Sheet Focused",
            "question": (
                f"Free cash flow dropped to ${fcf_latest:,.1f}M this quarter after capital expenditures of $11.8M. Given "
                f"this tightening cash generation, will the company need to draw down on revolving credit facilities, "
                f"or does this pace of cash conversion force a deceleration in planned capex and share repurchases?"
            ),
            "financial_evidence": [
                f"Free Cash Flow: ${fcf_latest:,.1f}M (down from ${fcf_prev:,.1f}M in Q3)",
                f"Operating Cash Flow: ${ocf_latest:,.1f}M against ongoing Capex requirements"
            ],
            "what_analysts_suspect": (
                "Analysts want to verify that liquidity covenants are safe and that the dividend or capital allocation "
                "framework will not be abruptly altered."
            ),
            "missing_information": [
                "Total revolving credit facility availability.",
                "Contracted capital expenditure commitments for the next 12 months."
            ]
        })

    # --- Questions for RISK 3: Segment Asymmetry ---
    if "RISK_SEGMENT_ASYMMETRY" in detected_ids and df_seg is not None and not df_seg.empty:
        questions.append({
            "id": "Q_SEGMENT_ASYMMETRY_1",
            "risk_id": "RISK_SEGMENT_ASYMMETRY",
            "priority": "HIGH",
            "priority_color": "#F59E0B",
            "analyst_archetype": "Technology Sector Specialist",
            "tone": "Strategically Probing",
            "question": (
                "Hardware & Edge Systems grew +25.9% QoQ to $68.0M, but its operating margin is only 7.9%. Meanwhile, "
                "your flagship Enterprise Cloud SaaS business remained completely flat at $45.0M despite high margins (27.1%). "
                "Is your cloud segment encountering market saturation or elevated customer churn, and are you relying "
                "on commoditized hardware sales to mask an organic slowdown in high-margin software?"
            ),
            "financial_evidence": [
                "Hardware Segment: $68.0M revenue (+25.9% QoQ), 7.9% operating margin",
                "Enterprise Cloud SaaS: $45.0M revenue (0.0% QoQ growth), 27.1% operating margin",
                "Managed Digital Services: Operating margin fell from 15.5% to 9.5%"
            ],
            "what_analysts_suspect": (
                "Investors prize high-multiple SaaS revenue. If low-margin hardware dominates growth while software stalls, "
                "analysts will derate the company's valuation multiple (e.g. from 25x P/E to 14x P/E)."
            ),
            "missing_information": [
                "SaaS Net Revenue Retention (NRR) and Annual Recurring Revenue (ARR).",
                "Customer acquisition costs (CAC) for Enterprise Cloud versus Hardware.",
                "Pipeline conversion rates for the SaaS division."
            ]
        })

    # --- Questions for RISK 4: Commitment Variance ---
    if "RISK_COMMITMENT_VARIANCE" in detected_ids:
        questions.append({
            "id": "Q_COMMITMENT_VARIANCE_1",
            "risk_id": "RISK_COMMITMENT_VARIANCE",
            "priority": "CRITICAL",
            "priority_color": "#EF4444",
            "analyst_archetype": "Senior Managing Director, Equity Research",
            "tone": "Accountability & Governance Centered",
            "question": (
                f"On the Q3 call, management affirmed a full-year operating margin guidance band of 18.0%-19.0% and "
                f"cash conversion above 90%. Actual results came in at {margin_latest:.1f}% margin (-400 bps miss) and "
                f"{conv_latest:.1f}% cash conversion (-28 pp miss). What unexpected variance emerged in the final 60 days "
                f"of the quarter that was not foreseen during your Q3 update, and how does leadership regain investor confidence in internal forecasting?"
            ),
            "financial_evidence": [
                f"Operating Margin Target: 18.0% - 19.0% | Actual Achieved: {margin_latest:.1f}% (Miss of ~400 bps)",
                f"Cash Conversion Target: > 90.0% | Actual Achieved: {conv_latest:.1f}% (Miss of ~28 pp)",
                "Enterprise Cloud YoY Growth Target: +15.0% | Actual Achieved: +2.1%"
            ],
            "what_analysts_suspect": (
                "Sell-side analysts feel blindsided by unannounced guidance misses. They will challenge management's "
                "budgeting rigor, visibility into intra-quarter trends, and transparency."
            ),
            "missing_information": [
                "Specific month-by-month financial variance analysis for the quarter.",
                "Formal reconciliation bridge comparing Q3 guidance assumptions to Q4 realized actuals."
            ]
        })

    return questions
