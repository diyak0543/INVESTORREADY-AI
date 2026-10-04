"""
risk_radar.py
Rule-based Investor Risk Radar for detecting earnings call vulnerabilities.
"""

from typing import Dict, List, Any
import pandas as pd


def analyze_financial_risks(
    df_fin: pd.DataFrame,
    df_seg: pd.DataFrame = None,
    df_com: pd.DataFrame = None
) -> Dict[str, Any]:
    """
    Executes rule-based risk detection algorithms across headline financials,
    segment performance, and management guidance commitments.
    """
    risks: List[Dict[str, Any]] = []

    if len(df_fin) < 2:
        return {
            "risk_score": 0,
            "risk_level": "Insufficient Data",
            "risks": [],
            "summary": "At least two quarters of financial data are required to evaluate risks."
        }

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
    margin_diff_pp = margin_latest - margin_prev
    margin_diff_bps = margin_diff_pp * 100

    ocf_prev = float(prev_row["Operating_Cash_Flow"])
    ocf_latest = float(latest_row["Operating_Cash_Flow"])
    ocf_qoq = ((ocf_latest - ocf_prev) / ocf_prev) * 100 if ocf_prev != 0 else 0

    conv_prev = float(prev_row["Cash_Conversion_Pct"])
    conv_latest = float(latest_row["Cash_Conversion_Pct"])
    conv_diff_pp = conv_latest - conv_prev

    # --- RULE 1: Margin Compression with Top-Line Growth ---
    if rev_qoq > 0 and (op_qoq < 0 or margin_diff_pp < -0.2):
        risks.append({
            "id": "RISK_MARGIN_COMPRESSION",
            "title": "Margin Compression Amid Revenue Growth ('Top-Line Mirage')",
            "severity": "CRITICAL",
            "category": "Profitability & Margin Quality",
            "icon": "🔻",
            "summary": f"Revenue expanded +{rev_qoq:.1f}%, but Operating Profit fell {op_qoq:.1f}%, contracting operating margin by {abs(margin_diff_bps):.0f} bps.",
            "why_flagged": (
                "When revenue grows while operating margins drop significantly, institutional investors interpret "
                "this as an indicator of eroding pricing power, product discounting to inflate volume, or severe "
                "operational cost inflation outstripping revenue."
            ),
            "evidence": {
                "Latest Revenue": f"${rev_latest:,.1f}M (+{rev_qoq:+.1f}% QoQ from ${rev_prev:,.1f}M)",
                "Latest Operating Profit": f"${op_latest:,.1f}M ({op_qoq:+.1f}% QoQ from ${op_prev:,.1f}M)",
                "Operating Margin Change": f"{margin_latest:.2f}% (down {abs(margin_diff_pp):.2f} percentage points / {abs(margin_diff_bps):.0f} bps from {margin_prev:.2f}%)",
                "Implied Operating Cost Growth": f"+{(((rev_latest - op_latest) - (rev_prev - op_prev)) / (rev_prev - op_prev) * 100):+.1f}% QoQ",
            },
            "weight": 35
        })

    # --- RULE 2: Weakening Operating Cash Flow & Quality of Earnings ---
    if ocf_qoq < 0 or conv_latest < 75:
        severity = "CRITICAL" if ocf_qoq < -15 or conv_latest < 65 else "HIGH"
        risks.append({
            "id": "RISK_CASH_FLOW_DECOUPLING",
            "title": "Operating Cash Flow Decoupling & Working Capital Stress",
            "severity": severity,
            "category": "Cash Flow & Earnings Quality",
            "icon": "💸",
            "summary": f"Operating Cash Flow dropped {ocf_qoq:.1f}% QoQ to ${ocf_latest:,.1f}M; cash conversion fell to {conv_latest:.1f}%.",
            "why_flagged": (
                "A sharp decline in operating cash flow while accounting revenue is rising suggests that earnings "
                "are not being converted into cash. Analysts suspect uncollected receivables (extended credit terms) "
                "or inventory buildup from unsold goods."
            ),
            "evidence": {
                "Operating Cash Flow": f"${ocf_latest:,.1f}M ({ocf_qoq:+.1f}% QoQ from ${ocf_prev:,.1f}M)",
                "Cash Conversion Ratio": f"{conv_latest:.1f}% of Operating Profit (down {abs(conv_diff_pp):.1f} pp from {conv_prev:.1f}%)",
                "Cash vs Accrual Divergence": f"Operating Profit was ${op_latest:,.1f}M, but actual Cash generated was only ${ocf_latest:,.1f}M (${op_latest - ocf_latest:,.1f}M gap)",
            },
            "weight": 30
        })

    # --- RULE 3: Uneven Business Segment Growth & Unfavorable Mix ---
    if df_seg is not None and not df_seg.empty and "Segment" in df_seg.columns:
        seg_quarters = df_seg["Quarter"].unique()
        if len(seg_quarters) >= 2:
            q_prev_name = seg_quarters[-2]
            q_lat_name = seg_quarters[-1]
            seg_p = df_seg[df_seg["Quarter"] == q_prev_name].set_index("Segment")
            seg_l = df_seg[df_seg["Quarter"] == q_lat_name].set_index("Segment")

            growth_rates = {}
            for s in seg_l.index:
                if s in seg_p.index and seg_p.loc[s, "Revenue"] > 0:
                    r_growth = ((seg_l.loc[s, "Revenue"] - seg_p.loc[s, "Revenue"]) / seg_p.loc[s, "Revenue"]) * 100
                    margin_lat = seg_l.loc[s, "Operating_Margin_Pct"]
                    growth_rates[s] = {"growth": r_growth, "margin": margin_lat, "rev": seg_l.loc[s, "Revenue"]}

            if growth_rates:
                max_grower = max(growth_rates.items(), key=lambda x: x[1]["growth"])
                min_grower = min(growth_rates.items(), key=lambda x: x[1]["growth"])

                spread = max_grower[1]["growth"] - min_grower[1]["growth"]
                if spread >= 15.0 or (min_grower[1]["margin"] > max_grower[1]["margin"] and max_grower[1]["growth"] > min_grower[1]["growth"]):
                    risks.append({
                        "id": "RISK_SEGMENT_ASYMMETRY",
                        "title": "Segment Performance Asymmetry & Mix Dilution",
                        "severity": "HIGH",
                        "category": "Segment Operations & Portfolio Mix",
                        "icon": "⚖️",
                        "summary": f"Fastest growing segment '{max_grower[0]}' (+{max_grower[1]['growth']:.1f}%) has lower margins than lagging segment '{min_grower[0]}' ({min_grower[1]['growth']:+.1f}%).",
                        "why_flagged": (
                            "Company growth is disproportionately reliant on lower-margin or commodity offerings, "
                            "while higher-margin flagship/SaaS segments have stalled. This negative mix shift pulls "
                            "down company-wide profitability regardless of top-line volume."
                        ),
                        "evidence": {
                            f"Fastest Grower ({max_grower[0]})": f"+{max_grower[1]['growth']:.1f}% QoQ growth | Operating Margin: {max_grower[1]['margin']:.1f}%",
                            f"Lagging Segment ({min_grower[0]})": f"{min_grower[1]['growth']:+.1f}% QoQ growth | Operating Margin: {min_grower[1]['margin']:.1f}%",
                            "Growth Dispersion Spread": f"{spread:.1f} percentage point divergence between business units",
                        },
                        "weight": 20
                    })

    # --- RULE 4: Variance vs Previous Management Commitments ---
    if df_com is not None and not df_com.empty:
        missed_commitments = []
        for _, row in df_com.iterrows():
            metric = str(row.get("Metric", ""))
            comm = str(row.get("Management_Guidance_Commitment", ""))
            status = str(row.get("Status", ""))
            if "miss" in status.lower() or "stall" in status.lower():
                missed_commitments.append({
                    "metric": metric,
                    "commitment": comm,
                    "target": row.get("Target_Value", ""),
                    "actual": row.get("Actual_Achieved", ""),
                    "unit": row.get("Unit", ""),
                    "status": status,
                    "context": row.get("Context", "")
                })

        if missed_commitments:
            evidence_dict = {}
            for item in missed_commitments:
                evidence_dict[item["metric"]] = (
                    f"Target: {item['target']}{item['unit']} | Actual: {item['actual']}{item['unit']} ({item['status']})"
                )

            risks.append({
                "id": "RISK_COMMITMENT_VARIANCE",
                "title": "Broken Guidance & Management Commitment Deficit",
                "severity": "HIGH",
                "category": "Guidance & Executive Credibility",
                "icon": "⚠️",
                "summary": f"{len(missed_commitments)} previous public commitments were missed, notably Operating Margin and Cash Conversion targets.",
                "why_flagged": (
                    "When public guidance given in prior quarters is missed without early pre-announcement, sell-side "
                    "analysts will challenge executive visibility into internal operations and future pipeline predictability."
                ),
                "evidence": evidence_dict,
                "weight": 20
            })

    # Calculate aggregate risk score (capped at 100)
    total_score = sum(r["weight"] for r in risks)
    total_score = min(total_score, 100)

    if total_score >= 75:
        risk_level = "CRITICAL (Severe Analyst Scrutiny)"
        badge_color = "#EF4444"
    elif total_score >= 50:
        risk_level = "HIGH (Elevated Earnings Call Pressure)"
        badge_color = "#F59E0B"
    elif total_score >= 25:
        risk_level = "MODERATE (Specific Vulnerabilities)"
        badge_color = "#3B82F6"
    else:
        risk_level = "LOW (Stable Performance)"
        badge_color = "#10B981"

    return {
        "risk_score": total_score,
        "risk_level": risk_level,
        "badge_color": badge_color,
        "risks": risks,
        "summary": f"Detected {len(risks)} distinct risk factors requiring preemptive defense preparation."
    }
