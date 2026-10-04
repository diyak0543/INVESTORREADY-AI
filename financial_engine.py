"""
financial_engine.py
Core Financial Processing, Data Validation, and Metric Engine for InvestorReady AI.
"""

import io
from typing import Dict, Any, Tuple, Optional
import pandas as pd
import numpy as np


def get_default_financial_data() -> pd.DataFrame:
    """Returns the synthetic financial results for Apex Global Technologies Inc."""
    data = {
        "Quarter": ["Q1 FY25", "Q2 FY25", "Q3 FY25", "Q4 FY25"],
        "Revenue": [120.0, 128.5, 139.0, 152.0],
        "Operating_Profit": [24.0, 24.4, 23.6, 21.3],
        "Operating_Margin_Pct": [20.0, 18.99, 16.98, 14.01],
        "Operating_Cash_Flow": [25.2, 23.1, 18.5, 13.2],
        "Capital_Expenditures": [8.5, 9.0, 10.2, 11.8],
        "Free_Cash_Flow": [16.7, 14.1, 8.3, 1.4],
    }
    df = pd.DataFrame(data)
    # Ensure exact calculated margin
    df["Operating_Margin_Pct"] = (df["Operating_Profit"] / df["Revenue"]) * 100
    df["Cash_Conversion_Pct"] = (df["Operating_Cash_Flow"] / df["Operating_Profit"]) * 100
    return df


def get_default_segment_data() -> pd.DataFrame:
    """Returns synthetic segment breakdown for Apex Global Technologies Inc."""
    data = {
        "Segment": [
            "Enterprise Cloud SaaS",
            "Hardware & Edge Systems",
            "Managed Digital Services",
            "Enterprise Cloud SaaS",
            "Hardware & Edge Systems",
            "Managed Digital Services",
        ],
        "Quarter": [
            "Q3 FY25", "Q3 FY25", "Q3 FY25",
            "Q4 FY25", "Q4 FY25", "Q4 FY25",
        ],
        "Revenue": [45.0, 54.0, 40.0, 45.0, 68.0, 39.0],
        "Operating_Profit": [12.6, 4.8, 6.2, 12.2, 5.4, 3.7],
        "Operating_Margin_Pct": [28.0, 8.89, 15.5, 27.11, 7.94, 9.49],
    }
    df = pd.DataFrame(data)
    df["Operating_Margin_Pct"] = (df["Operating_Profit"] / df["Revenue"]) * 100
    return df


def get_default_commitments_data() -> pd.DataFrame:
    """Returns previous management commitments and guidance from Q3 earnings call."""
    data = {
        "Metric": [
            "Full-Year Operating Margin",
            "Operating Cash Conversion Ratio",
            "Enterprise Cloud Segment Growth",
            "Working Capital (DSO Days)",
        ],
        "Management_Guidance_Commitment": [
            "18.0% - 19.0% minimum operating margin",
            "> 90% conversion of Operating Profit into Cash",
            "+15% YoY expansion in high-margin Cloud",
            "Reduce DSO by 5 days (normalize receivables)",
        ],
        "Target_Value": [18.0, 90.0, 15.0, -5.0],
        "Actual_Achieved": [14.01, 61.97, 2.1, 8.0],
        "Unit": ["%", "%", "%", "days"],
        "Status": ["MISSED (-399 bps)", "MISSED (-28.0 pp)", "MISSED (-12.9 pp)", "MISSED (+13 days)"],
        "Context": [
            "Q3 Earnings Call: 'Confident in delivering 18%+ operating margin for FY25.'",
            "Q3 Earnings Call: 'Cash flow will rebound sharply in Q4 as working capital clears.'",
            "Investor Day: 'Enterprise Cloud remains our primary secular growth engine.'",
            "Q3 Call: 'Customer collections will normalize before year-end.'",
        ]
    }
    return pd.DataFrame(data)


def create_sample_excel_workbook() -> bytes:
    """Generates an in-memory sample Excel workbook with all 3 sheets."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_fin = get_default_financial_data()
        df_seg = get_default_segment_data()
        df_com = get_default_commitments_data()

        df_fin.to_excel(writer, sheet_name="Financial_Results", index=False)
        df_seg.to_excel(writer, sheet_name="Segment_Data", index=False)
        df_com.to_excel(writer, sheet_name="Management_Commitments", index=False)

    return output.getvalue()


def parse_and_validate_excel(file_content: Any) -> Tuple[bool, Dict[str, pd.DataFrame], str]:
    """
    Parses and validates an uploaded Excel file.
    Must contain 'Financial_Results' sheet with required columns.
    Returns: (is_valid, dict_of_dataframes, message)
    """
    try:
        excel_file = pd.ExcelFile(file_content, engine="openpyxl")
    except Exception as e:
        return False, {}, f"Unable to read file as an Excel workbook: {str(e)}"

    sheet_names = excel_file.sheet_names

    # Check for Financial_Results sheet (case insensitive)
    fin_sheet_match = None
    for s in sheet_names:
        if s.strip().lower() in ["financial_results", "financial results", "financials"]:
            fin_sheet_match = s
            break

    if not fin_sheet_match:
        return False, {}, (
            f"Missing required sheet 'Financial_Results'. Found sheets: {', '.join(sheet_names)}. "
            "Please ensure your workbook contains a sheet named 'Financial_Results'."
        )

    # Read Financial_Results
    try:
        df_fin = excel_file.parse(fin_sheet_match)
    except Exception as e:
        return False, {}, f"Failed to parse sheet '{fin_sheet_match}': {str(e)}"

    if df_fin.empty:
        return False, {}, "Sheet 'Financial_Results' is empty."

    # Standardize column names (strip whitespace, lowercase for matching)
    col_map = {}
    standard_columns = {
        "quarter": "Quarter",
        "revenue": "Revenue",
        "operating_profit": "Operating_Profit",
        "operating profit": "Operating_Profit",
        "operating_income": "Operating_Profit",
        "operating income": "Operating_Profit",
        "ebit": "Operating_Profit",
        "operating_cash_flow": "Operating_Cash_Flow",
        "operating cash flow": "Operating_Cash_Flow",
        "ocf": "Operating_Cash_Flow",
        "cash_flow_from_operations": "Operating_Cash_Flow",
        "cash flow from operations": "Operating_Cash_Flow",
        "operating_margin_pct": "Operating_Margin_Pct",
        "operating margin": "Operating_Margin_Pct",
        "operating margin %": "Operating_Margin_Pct",
        "operating_margin": "Operating_Margin_Pct",
    }

    for col in df_fin.columns:
        clean_col = str(col).strip().lower()
        if clean_col in standard_columns:
            col_map[col] = standard_columns[clean_col]

    df_fin = df_fin.rename(columns=col_map)

    # Required columns check
    required_cols = ["Quarter", "Revenue", "Operating_Profit", "Operating_Cash_Flow"]
    missing = [c for c in required_cols if c not in df_fin.columns]
    if missing:
        return False, {}, (
            f"Sheet 'Financial_Results' is missing mandatory columns: {', '.join(missing)}. "
            f"Detected columns: {', '.join(list(df_fin.columns))}."
        )

    # Validate numeric types and convert
    numeric_cols = ["Revenue", "Operating_Profit", "Operating_Cash_Flow"]
    for nc in numeric_cols:
        df_fin[nc] = pd.to_numeric(df_fin[nc], errors="coerce")
        if df_fin[nc].isnull().any():
            return False, {}, f"Column '{nc}' contains invalid non-numeric or blank values."

    # Calculate or recalculate Margin & Cash conversion
    df_fin["Operating_Margin_Pct"] = (df_fin["Operating_Profit"] / df_fin["Revenue"]) * 100
    df_fin["Cash_Conversion_Pct"] = (df_fin["Operating_Cash_Flow"] / df_fin["Operating_Profit"]) * 100

    # Ensure Quarter is string
    df_fin["Quarter"] = df_fin["Quarter"].astype(str)

    if len(df_fin) < 2:
        return False, {}, "Financial_Results must contain at least 2 quarters to enable quarter-on-quarter (QoQ) comparison."

    dataframes = {"Financial_Results": df_fin}

    # Optional: Segment_Data sheet
    seg_sheet_match = None
    for s in sheet_names:
        if s.strip().lower() in ["segment_data", "segment data", "segments"]:
            seg_sheet_match = s
            break

    if seg_sheet_match:
        try:
            df_seg = excel_file.parse(seg_sheet_match)
            # Normalize segment columns
            seg_col_map = {
                "segment": "Segment", "segment name": "Segment",
                "quarter": "Quarter", "period": "Quarter",
                "revenue": "Revenue", "operating_profit": "Operating_Profit",
                "operating profit": "Operating_Profit"
            }
            renamed = {}
            for c in df_seg.columns:
                if str(c).strip().lower() in seg_col_map:
                    renamed[c] = seg_col_map[str(c).strip().lower()]
            df_seg = df_seg.rename(columns=renamed)
            if "Revenue" in df_seg.columns and "Operating_Profit" in df_seg.columns:
                df_seg["Revenue"] = pd.to_numeric(df_seg["Revenue"], errors="coerce").fillna(0)
                df_seg["Operating_Profit"] = pd.to_numeric(df_seg["Operating_Profit"], errors="coerce").fillna(0)
                df_seg["Operating_Margin_Pct"] = np.where(
                    df_seg["Revenue"] > 0,
                    (df_seg["Operating_Profit"] / df_seg["Revenue"]) * 100,
                    0.0
                )
                dataframes["Segment_Data"] = df_seg
        except Exception:
            # Fallback to default segment data if parsing fails
            dataframes["Segment_Data"] = get_default_segment_data()
    else:
        # Fallback to default segment data
        dataframes["Segment_Data"] = get_default_segment_data()

    # Optional: Management_Commitments sheet
    com_sheet_match = None
    for s in sheet_names:
        if s.strip().lower() in ["management_commitments", "commitments", "guidance"]:
            com_sheet_match = s
            break

    if com_sheet_match:
        try:
            df_com = excel_file.parse(com_sheet_match)
            dataframes["Management_Commitments"] = df_com
        except Exception:
            dataframes["Management_Commitments"] = get_default_commitments_data()
    else:
        dataframes["Management_Commitments"] = get_default_commitments_data()

    return True, dataframes, f"Successfully uploaded and validated workbook with {len(df_fin)} quarters of financial results!"


def compute_qoq_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes latest quarter vs previous quarter comparisons and key growth figures.
    """
    if len(df) < 2:
        return {}

    # Sort if index or quarters are orderly
    prev_row = df.iloc[-2]
    latest_row = df.iloc[-1]

    rev_prev = float(prev_row["Revenue"])
    rev_latest = float(latest_row["Revenue"])
    rev_qoq_pct = ((rev_latest - rev_prev) / rev_prev) * 100 if rev_prev != 0 else 0.0

    op_prev = float(prev_row["Operating_Profit"])
    op_latest = float(latest_row["Operating_Profit"])
    op_qoq_pct = ((op_latest - op_prev) / op_prev) * 100 if op_prev != 0 else 0.0

    margin_prev = float(prev_row["Operating_Margin_Pct"])
    margin_latest = float(latest_row["Operating_Margin_Pct"])
    margin_diff_pp = margin_latest - margin_prev  # in percentage points
    margin_diff_bps = margin_diff_pp * 100  # in basis points

    ocf_prev = float(prev_row["Operating_Cash_Flow"])
    ocf_latest = float(latest_row["Operating_Cash_Flow"])
    ocf_qoq_pct = ((ocf_latest - ocf_prev) / ocf_prev) * 100 if ocf_prev != 0 else 0.0

    conv_prev = float(prev_row["Cash_Conversion_Pct"])
    conv_latest = float(latest_row["Cash_Conversion_Pct"])
    conv_diff_pp = conv_latest - conv_prev

    return {
        "prev_quarter": str(prev_row["Quarter"]),
        "latest_quarter": str(latest_row["Quarter"]),
        "rev_prev": rev_prev,
        "rev_latest": rev_latest,
        "rev_qoq_pct": rev_qoq_pct,
        "op_prev": op_prev,
        "op_latest": op_latest,
        "op_qoq_pct": op_qoq_pct,
        "margin_prev": margin_prev,
        "margin_latest": margin_latest,
        "margin_diff_pp": margin_diff_pp,
        "margin_diff_bps": margin_diff_bps,
        "ocf_prev": ocf_prev,
        "ocf_latest": ocf_latest,
        "ocf_qoq_pct": ocf_qoq_pct,
        "conv_prev": conv_prev,
        "conv_latest": conv_latest,
        "conv_diff_pp": conv_diff_pp,
    }
