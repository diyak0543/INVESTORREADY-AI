"""
mock_call_simulator.py
Rule-based evaluation engine for Mock Earnings Call Q&A simulation.
Transparent checklist checking factual grounding, consistency, uncertainty, and unsupported buzzwords.
"""

import re
from typing import Dict, Any, List


BUZZWORDS_EMPTY = [
    "cautiously optimistic",
    "laser focused",
    "unprecedented",
    "synergies",
    "game changer",
    "silver lining",
    "rest assured",
    "trust us",
    "don't worry",
    "headwinds",
    "tailwinds",
    "paradigm shift",
    "exponentially",
    "sky is the limit",
    "massive upside",
]

UNREALISTIC_PROMISES = [
    "we guarantee",
    "guaranteed",
    "100% certain",
    "promise that",
    "zero risk",
    "flawless",
    "impossible to fail",
    "will definitely double",
    "absolute certainty",
]


def evaluate_mock_response(
    user_answer: str,
    question_data: Dict[str, Any],
    df_fin_summary: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Evaluates an executive response using a transparent, multi-point rule-based rubric.
    """
    text = (user_answer or "").strip()
    text_lower = text.lower()
    word_count = len(text.split())

    checklist: List[Dict[str, Any]] = []
    total_score = 0

    if word_count < 15:
        return {
            "score": 10,
            "rating": "Insufficient Response",
            "rating_color": "#EF4444",
            "summary": "The response is too brief (less than 15 words). Institutional investors expect substantive, structured explanations.",
            "checklist": [
                {
                    "item": "Completeness & Substance",
                    "status": "FAILED ❌",
                    "score": 0,
                    "max": 100,
                    "feedback": "Please provide a comprehensive response addressing the analyst's question directly."
                }
            ],
            "coaching_tips": [
                "Acknowledge the core question directly in your opening sentence.",
                "Cite at least 2 specific financial metrics from the quarter.",
                "Explain the operational drivers (e.g. product mix shift, shipment timing)."
            ],
            "flagged_buzzwords": [],
            "metrics_detected": []
        }

    # 1. CHECKLIST ITEM 1: Factual Grounding & Numeric Rigor (25 pts)
    # Check for numbers, dollar signs, percentages, basis points
    numbers_found = re.findall(r"\b\d+(?:\.\d+)?%?|\$\d+(?:\.\d+)?[MBK]?", text)
    financial_keywords = ["revenue", "margin", "profit", "cash flow", "growth", "hardware", "cloud", "mix", "cost", "basis points", "bps"]
    kw_hits = [k for k in financial_keywords if k in text_lower]

    num_score = 0
    num_feedback = ""
    if len(numbers_found) >= 2 and len(kw_hits) >= 2:
        num_score = 25
        num_status = "PASSED ✅"
        num_feedback = f"Strong numeric grounding: Cited {len(numbers_found)} figures ({', '.join(numbers_found[:4])}) and financial terms."
    elif len(numbers_found) >= 1 or len(kw_hits) >= 2:
        num_score = 15
        num_status = "NEEDS ATTENTION ⚠️"
        num_feedback = f"Partially grounded. Cited {len(numbers_found)} number(s). Anchor your response with more specific figures (e.g., 14.0% margin, $152M revenue, $13.2M cash flow)."
    else:
        num_score = 5
        num_status = "FAILED ❌"
        num_feedback = "Lacks numeric evidence. Wall Street analysts will discount general qualitative statements without hard figures."

    checklist.append({
        "item": "1. Factual Grounding & Metric Citation",
        "status": num_status,
        "score": num_score,
        "max": 25,
        "feedback": num_feedback
    })
    total_score += num_score

    # 2. CHECKLIST ITEM 2: Addressing Core Risk & Root Cause (20 pts)
    risk_id = question_data.get("risk_id", "")
    addressed = False
    cause_terms = []

    if "MARGIN" in risk_id:
        cause_terms = ["mix", "hardware", "cost", "discount", "margin", "cloud", "pricing", "inflation", "procurement"]
    elif "CASH" in risk_id:
        cause_terms = ["working capital", "receivable", "inventory", "dso", "timing", "collection", "conversion", "capex"]
    elif "SEGMENT" in risk_id:
        cause_terms = ["cloud", "hardware", "saas", "software", "mix", "services", "enterprise", "procurement"]
    elif "COMMITMENT" in risk_id:
        cause_terms = ["guidance", "target", "commitment", "variance", "forecast", "planning", "unforeseen", "model"]
    else:
        cause_terms = ["growth", "margin", "cash", "performance"]

    matched_causes = [t for t in cause_terms if t in text_lower]
    if len(matched_causes) >= 2:
        cause_score = 20
        cause_status = "PASSED ✅"
        cause_feedback = f"Directly addressed core drivers: Mentioned key operational concepts ({', '.join(matched_causes[:3])})."
    elif len(matched_causes) == 1:
        cause_score = 12
        cause_status = "NEEDS ATTENTION ⚠️"
        cause_feedback = f"Touched on '{matched_causes[0]}', but could be more explicit about operational causality."
    else:
        cause_score = 4
        cause_status = "FAILED ❌"
        cause_feedback = "Did not directly address the underlying operational cause of the financial variance."

    checklist.append({
        "item": "2. Addressing Core Problem & Root Cause",
        "status": cause_status,
        "score": cause_score,
        "max": 20,
        "feedback": cause_feedback
    })
    total_score += cause_score

    # 3. CHECKLIST ITEM 3: Consistency with Commitments & Avoidance of Contradictions (20 pts)
    # Check if user claims untrue statements like "we exceeded our 18% margin" or denies the miss
    contradiction_flag = False
    if "margin" in text_lower and ("exceeded" in text_lower or "beat our guidance" in text_lower or "achieved 18%" in text_lower):
        contradiction_flag = True

    if not contradiction_flag:
        cons_score = 20
        cons_status = "PASSED ✅"
        cons_feedback = "Consistent with company filings: Honestly acknowledges the quarterly results without contradicting historical guidance."
    else:
        cons_score = 0
        cons_status = "FAILED ❌"
        cons_feedback = "Potential contradiction: Suggesting the company beat margin guidance when actual reported margin was 14.0%."

    checklist.append({
        "item": "3. Consistency with Filings & Guidance",
        "status": cons_status,
        "score": cons_score,
        "max": 20,
        "feedback": cons_feedback
    })
    total_score += cons_score

    # 4. CHECKLIST ITEM 4: Realistic Uncertainty & Balanced Executive Tone (15 pts)
    # Flag over-promising or unbacked guarantees
    guarantee_hits = [p for p in UNREALISTIC_PROMISES if p in text_lower]
    if not guarantee_hits:
        tone_score = 15
        tone_status = "PASSED ✅"
        tone_feedback = "Balanced, professional tone: Acknowledges reality without dangerous forward-looking guarantees."
    else:
        tone_score = 5
        tone_status = "FAILED ❌"
        tone_feedback = f"Over-promising detected ({', '.join(guarantee_hits)}). Never make unconditional guarantees on an earnings call; use safe-harbor qualified language."

    checklist.append({
        "item": "4. Realistic Uncertainty & Executive Balance",
        "status": tone_status,
        "score": tone_score,
        "max": 15,
        "feedback": tone_feedback
    })
    total_score += tone_score

    # 5. CHECKLIST ITEM 5: Avoidance of Evasive Fluff & Unsupported Buzzwords (20 pts)
    found_buzzwords = [b for b in BUZZWORDS_EMPTY if b in text_lower]
    if len(found_buzzwords) == 0:
        buzz_score = 20
        buzz_status = "PASSED ✅"
        buzz_feedback = "Clean language: Free of empty corporate jargon and evasive buzzwords."
    elif len(found_buzzwords) <= 2:
        buzz_score = 12
        buzz_status = "NEEDS ATTENTION ⚠️"
        buzz_feedback = f"Contains generic cliché(s): '{', '.join(found_buzzwords)}'. Replace with concrete facts or operational details."
    else:
        buzz_score = 4
        buzz_status = "FAILED ❌"
        buzz_feedback = f"Heavy reliance on evasive jargon: '{', '.join(found_buzzwords)}'. Analysts view this as an attempt to dodge the question."

    checklist.append({
        "item": "5. Freedom from Evasive Buzzwords & Fluff",
        "status": buzz_status,
        "score": buzz_score,
        "max": 20,
        "feedback": buzz_feedback
    })
    total_score += buzz_score

    # Overall Grading
    if total_score >= 85:
        rating = "Institutional Grade (Executive Ready)"
        rating_color = "#10B981"
        overall_summary = "Outstanding response! Grounded in verified facts, transparent on operational drivers, and free of evasive fluff."
    elif total_score >= 70:
        rating = "Adequate (Defensible, Needs Sharpening)"
        rating_color = "#3B82F6"
        overall_summary = "Good foundation, but can be strengthened by adding more concrete metrics and pruning clichés."
    elif total_score >= 50:
        rating = "Vulnerable (Risk of Analyst Pushback)"
        rating_color = "#F59E0B"
        overall_summary = "The response lacks sufficient hard data and may sound defensive or evasive to experienced investors."
    else:
        rating = "Critical Risk (Loss of Credibility)"
        rating_color = "#EF4444"
        overall_summary = "High risk of damaging management credibility. Missing data, evasive phrasing, or over-promising."

    # Actionable Coaching Tips
    coaching_tips = []
    if num_score < 25:
        coaching_tips.append("Cite at least 2 hard metrics (e.g. '$152M revenue (+9.4%)', '14.0% operating margin', '$13.2M cash flow').")
    if cause_score < 20:
        coaching_tips.append("Explicitly state the operational bridge: distinguish mix shift (Hardware vs Cloud) from cost inflation.")
    if found_buzzwords:
        coaching_tips.append(f"Remove generic buzzwords like '{found_buzzwords[0]}' and replace with verified operational steps.")
    if guarantee_hits:
        coaching_tips.append("Eliminate forward guarantees ('we guarantee'). Replace with 'We are implementing strict cost hurdle rates.'")
    if not coaching_tips:
        coaching_tips.append("Excellent execution. Consider linking the response to the upcoming 10-Q filing for final reconciliation details.")

    return {
        "score": total_score,
        "rating": rating,
        "rating_color": rating_color,
        "summary": overall_summary,
        "checklist": checklist,
        "coaching_tips": coaching_tips,
        "flagged_buzzwords": found_buzzwords,
        "metrics_detected": numbers_found
    }
