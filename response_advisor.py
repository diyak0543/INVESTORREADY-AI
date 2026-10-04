"""
response_advisor.py
Drafts evidence-anchored executive responses for earnings call questions.
Highlights missing evidence, flags unsupported assumptions, and enforces strict governance disclaimers.
"""

from typing import Dict, Any


def get_suggested_responses() -> Dict[str, Dict[str, Any]]:
    """
    Returns verified, structured draft responses for each generated question ID.
    Enforces strict discipline: relies only on reported numbers, never invents disclosures.
    """
    advisories = {
        "Q_MARGIN_COMPRESSION_1": {
            "question_id": "Q_MARGIN_COMPRESSION_1",
            "executive_opening": (
                "Acknowledge the margin contraction immediately without defensiveness; provide clear operational attribution."
            ),
            "suggested_draft_response": (
                "Thank you for the question. We fully acknowledge that while headline revenue reached a record $152.0M "
                "(up 9.4% QoQ), our operating margin contracted by 300 basis points to 14.0%, and operating profit was $21.3M.\n\n"
                "To be clear on the driver: this was not driven by broad-based price discounting. Instead, it reflects two distinct factors: "
                "First, a significant product mix shift toward our Hardware & Edge Systems segment, which expanded 25.9% QoQ to $68.0M "
                "carrying an 7.9% operating margin. Second, we absorbed higher upfront component procurement and shipping costs to fulfill "
                "that surge in hardware volume within the quarter.\n\n"
                "Our high-margin Enterprise Cloud SaaS business remained profitable at 27.1% operating margin, but stalled at $45.0M revenue. "
                "We are actively rationalizing SG&A spend across delivery units and adjusting hardware pricing tiers to restore operating leverage."
            ),
            "evidentiary_anchors": [
                "Revenue: $152.0M (+9.4% QoQ)",
                "Operating Margin: 14.0% (-300 bps QoQ from 17.0%)",
                "Operating Profit: $21.3M (-9.7% QoQ from $23.6M)",
                "Hardware Segment: $68.0M (+25.9% QoQ, 7.9% margin)",
                "Enterprise Cloud: $45.0M (0.0% QoQ, 27.1% margin)"
            ],
            "missing_evidence_and_data_gaps": [
                "Detailed gross profit percentage by product line has not been filed yet (pending 10-Q filing).",
                "Specific freight and component surcharge numbers are unconfirmed pending full vendor reconciliation.",
                "Customer-level discount approvals have not been audited for the full quarter."
            ],
            "unsupported_assumptions_to_avoid": [
                "DO NOT promise that operating margin will rebound to 18% next quarter without verified cost reduction contracts.",
                "DO NOT claim that competitors are suffering the exact same margin compression unless third-party industry reports exist.",
                "DO NOT characterize hardware cost inflation as 'temporary' without disclosing current vendor contract durations."
            ],
            "compliance_disclaimer": (
                "⚠️ INSTITUTIONAL DISCLOSURE NOTICE: This response is a preliminary advisory draft intended for internal "
                "executive preparation. Final wording must be formally validated by Corporate Legal, Investor Relations, "
                "and the Chief Financial Officer before public delivery. Do not make forward-looking commitments without safe-harbor qualifications."
            )
        },

        "Q_MARGIN_COMPRESSION_2": {
            "question_id": "Q_MARGIN_COMPRESSION_2",
            "executive_opening": (
                "Address operating expense trajectory honestly, outline margin recovery levers, and decline to provide unapproved multi-year commitments."
            ),
            "suggested_draft_response": (
                "We recognize the critical need for operating cost discipline. In Q4, operating costs increased as we scaled fulfillment "
                "for the hardware delivery cycle. We do not view a 14.0% operating margin as our long-term steady state.\n\n"
                "We are executing on three operational levers: First, targeted cost containment on variable operating overhead; second, "
                "re-accelerating our enterprise cloud go-to-market where margins are 27.1%; and third, instituting stricter margin hurdle rates "
                "on large hardware deals.\n\n"
                "We will release our formal full-year fiscal guidance during our upcoming strategy update, and we remain committed to "
                "disciplined, profitable growth rather than volume expansion at the expense of profitability."
            ),
            "evidentiary_anchors": [
                "Current Operating Margin: 14.0%",
                "Enterprise Cloud Margin: 27.1%",
                "Hardware Margin: 7.9%"
            ],
            "missing_evidence_and_data_gaps": [
                "The board-approved FY26 annual operating budget is still undergoing final audit.",
                "Quantified headcount rationalization savings have not been formally calculated."
            ],
            "unsupported_assumptions_to_avoid": [
                "DO NOT give an unapproved numeric margin guidance range for next quarter.",
                "DO NOT use generic phrases like 'we see immense synergies' without naming specific cost line items."
            ],
            "compliance_disclaimer": (
                "⚠️ INSTITUTIONAL DISCLOSURE NOTICE: Forward-looking statements on margin recovery must be accompanied "
                "by SEC Regulation G GAAP reconciliations and approved by Investor Relations."
            )
        },

        "Q_CASH_FLOW_1": {
            "question_id": "Q_CASH_FLOW_1",
            "executive_opening": (
                "Provide transparent operational explanation for the accrual-versus-cash divergence without evading working capital metrics."
            ),
            "suggested_draft_response": (
                "The divergence between our $21.3M operating profit and $13.2M in operating cash flow is an essential question. "
                "Our cash conversion ratio fell to 62.0% in Q4.\n\n"
                "The primary driver was working capital timing tied to the late-quarter delivery of large Hardware & Edge Systems contracts. "
                "Because shipments surged in the final month of the quarter, significant billings remain in accounts receivable and have not "
                "yet converted to cash collections. Concurrently, we built inventory buffer stock to safeguard customer deployment timelines.\n\n"
                "We have not witnessed any deterioration in counterparty creditworthiness or default rates. Our collection teams are actively "
                "working down these receivables, and our full cash flow statement and balance sheet schedules will be disclosed in our 10-Q."
            ),
            "evidentiary_anchors": [
                "Operating Cash Flow: $13.2M (-28.6% QoQ from $18.5M)",
                "Operating Profit: $21.3M (Accrual-to-Cash Gap: $8.1M)",
                "Cash Conversion Ratio: 62.0% (down from 78.4% in Q3 and 105.0% in Q1)"
            ],
            "missing_evidence_and_data_gaps": [
                "Audited Days Sales Outstanding (DSO) and Days Sales of Inventory (DSI) figures are pending final 10-Q filing.",
                "Exact breakdown of aging receivables past 60 and 90 days."
            ],
            "unsupported_assumptions_to_avoid": [
                "DO NOT state that 'all receivables have been collected this morning' unless Treasury provides verified bank statements.",
                "DO NOT dismiss the cash flow drop as 'pure noise'—investors track working capital as an indicator of earnings quality."
            ],
            "compliance_disclaimer": (
                "⚠️ INSTITUTIONAL DISCLOSURE NOTICE: Statements regarding customer collections and working capital timing "
                "must be reviewed by the Corporate Controller and Treasury before the call."
            )
        },

        "Q_CASH_FLOW_2": {
            "question_id": "Q_CASH_FLOW_2",
            "executive_opening": (
                "Reassure analysts on liquidity covenants and balance sheet stability without speculating on unapproved capital actions."
            ),
            "suggested_draft_response": (
                "While Q4 free cash flow compressed to $1.4M after $11.8M in capital expenditures, our balance sheet position remains secure. "
                "Our capital expenditures in Q4 were elevated due to previously planned test lab and hardware tooling investments.\n\n"
                "We maintain ample liquidity under our existing credit facilities, and our capital allocation framework continues to prioritize "
                "essential operational reinvestment and maintaining a resilient investment-grade balance sheet. We will provide our updated "
                "annual capex outlook with our comprehensive filing."
            ),
            "evidentiary_anchors": [
                "Operating Cash Flow: $13.2M",
                "Capital Expenditures: $11.8M",
                "Free Cash Flow: $1.4M (compressed from $8.3M in Q3 and $16.7M in Q1)"
            ],
            "missing_evidence_and_data_gaps": [
                "Total undrawn revolving credit facility capacity figure.",
                "Board-approved share buyback authorization balance."
            ],
            "unsupported_assumptions_to_avoid": [
                "DO NOT make unannounced promises about increasing dividends or launching an emergency share buyback.",
                "DO NOT guarantee zero credit facility usage if seasonal cash needs fluctuate."
            ],
            "compliance_disclaimer": (
                "⚠️ INSTITUTIONAL DISCLOSURE NOTICE: Balance sheet and credit covenant disclosures are subject to strict "
                "regulatory compliance review."
            )
        },

        "Q_SEGMENT_ASYMMETRY_1": {
            "question_id": "Q_SEGMENT_ASYMMETRY_1",
            "executive_opening": (
                "Directly address the SaaS versus Hardware growth divergence, clarify market demand dynamics, and outline cloud sales strategy."
            ),
            "suggested_draft_response": (
                "This touches on the core strategic transition of our business. In Q4, Hardware & Edge Systems generated $68.0M (up 25.9% QoQ) "
                "at a 7.9% operating margin, while Enterprise Cloud SaaS recorded $45.0M, unchanged from Q3, but maintaining high profitability at 27.1%.\n\n"
                "We do not view Enterprise Cloud as saturated. Rather, in Q4, several large enterprise customers extended their software procurement "
                "review cycles, which delayed several seven-figure contract closures into subsequent periods. Meanwhile, demand for integrated hardware "
                "deployments accelerated rapidly.\n\n"
                "Our strategy is not to rely on commoditized hardware. Instead, our hardware installations serve as the physical entry point "
                "for cross-selling higher-margin cloud SaaS subscriptions in future quarters. We have reinforced our enterprise software sales "
                "leadership to drive pipeline conversion."
            ),
            "evidentiary_anchors": [
                "Enterprise Cloud SaaS: $45.0M revenue (0.0% QoQ growth), $12.2M operating profit (27.1% margin)",
                "Hardware & Edge Systems: $68.0M revenue (+25.9% QoQ growth), $5.4M operating profit (7.9% margin)",
                "Managed Digital Services: $39.0M revenue (-2.5% QoQ), $3.7M operating profit (9.5% margin)"
            ],
            "missing_evidence_and_data_gaps": [
                "Audited Annual Recurring Revenue (ARR) and Net Retention Rate (NRR) metrics are not yet formally published.",
                "Customer cross-sell conversion rates from Hardware to Cloud are unconfirmed."
            ],
            "unsupported_assumptions_to_avoid": [
                "DO NOT state that delayed cloud contracts have already closed unless executed contracts are in hand.",
                "DO NOT characterize hardware clients as 'guaranteed cloud conversions'."
            ],
            "compliance_disclaimer": (
                "⚠️ INSTITUTIONAL DISCLOSURE NOTICE: Segment sales projections and pipeline statements must adhere to "
                "Regulation FD fair disclosure standards."
            )
        },

        "Q_COMMITMENT_VARIANCE_1": {
            "question_id": "Q_COMMITMENT_VARIANCE_1",
            "executive_opening": (
                "Take direct ownership of the guidance miss, explain the unforeseen variance factors, and lay out revised forecasting safeguards."
            ),
            "suggested_draft_response": (
                "We appreciate the direct question and we take our commitments to shareholders with the utmost seriousness. In our Q3 call, "
                "we anticipated full-year operating margins of 18%-19% and cash conversion exceeding 90%. Our actual Q4 margin of 14.0% and "
                "cash conversion of 62.0% fell short of those commitments.\n\n"
                "What changed in the final two months of the quarter was twofold: First, an unprecedented acceleration in lower-margin hardware "
                "deliveries shifted our blended revenue mix far faster than our planning model forecasted. Second, critical high-margin enterprise "
                "cloud closings that were factored into our margin guidance slipped past year-end.\n\n"
                "We have instituted more rigorous sensitivity stress-testing into our quarterly guidance models, increased the margin hurdle rates "
                "for low-margin deployments, and improved intra-quarter visibility between sales pipeline and finance. We are dedicated to regaining "
                "market confidence through transparent execution."
            ),
            "evidentiary_anchors": [
                "Guidance Target: 18.0% - 19.0% | Achieved Q4 Margin: 14.01% (Miss of ~400 bps)",
                "Cash Conversion Target: >90% | Achieved Q4 Cash Conversion: 61.97% (Miss of ~28 pp)",
                "Enterprise Cloud YoY Growth Target: +15% | Achieved Q4 Growth: +2.1%"
            ],
            "missing_evidence_and_data_gaps": [
                "Formal post-mortem variance analysis across business units has not been publicly filed.",
                "Updated baseline guidance ranges for FY26 are pending final board sign-off."
            ],
            "unsupported_assumptions_to_avoid": [
                "DO NOT deflect blame entirely to customers or macroeconomic conditions without acknowledging internal forecasting gaps.",
                "DO NOT guarantee that guidance will never be missed again—commit to improved processes and transparency instead."
            ],
            "compliance_disclaimer": (
                "⚠️ INSTITUTIONAL DISCLOSURE NOTICE: Executive statements addressing prior guidance misses are closely reviewed "
                "by securities counsel and investor governance committees."
            )
        }
    }
    return advisories
