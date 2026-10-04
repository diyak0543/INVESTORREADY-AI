# 🏛️ InvestorReady AI — Earnings Call Preparation Simulator

An institutional-grade, rule-based financial analytics and executive preparation platform built with **Python**, **Streamlit**, and **Pandas**.

Designed specifically for executive leadership, CFOs, and business competition showcases to preemptively identify vulnerabilities, anticipate tough Wall Street analyst questioning, and rehearse defensible, evidence-grounded earnings call responses.

---

## 🚀 How to Run on Windows (Step-by-Step for Beginners)

As a beginner, running the application takes just two quick steps:

### Step 1: Open Terminal in the Project Folder
1. Press the `Windows Key`, type **PowerShell** or **Command Prompt**, and open it.
2. Navigate to your project folder by typing:
   ```powershell
   cd "C:\Users\Diya\OneDrive\Desktop\test"
   ```

### Step 2: Launch the Application
Run the following command:
```powershell
streamlit run app.py
```
> **What happens next?** Streamlit will automatically start the local web server and open the application in your default web browser at `http://localhost:8501`.

---

## 💼 The Core Business Problem

A listed enterprise (e.g. **Apex Global Technologies Inc.**) demonstrates growing headline revenue, but exhibits severe underlying operational vulnerabilities:
1. **Margin Compression**: Revenue increased +9.4% QoQ to $152.0M, but operating profit fell -9.7% to $21.3M, causing operating margins to compress from 17.0% down to 14.0% (-300 basis points).
2. **Weakening Cash Flow & Accrual Divergence**: Operating cash flow fell -28.6% QoQ to $13.2M, with cash conversion dropping to 62.0% (leaving an $8.1M gap between accounting profit and actual cash).
3. **Uneven Business Segment Growth (Mix Dilution)**: Low-margin Hardware (+25.9% QoQ, 7.9% margin) drove almost all volume growth, while high-margin Enterprise Cloud SaaS (27.1% margin) stagnated with 0.0% growth.
4. **Broken Commitments & Guidance Gaps**: Previous public guidance of 18.0%-19.0% operating margin and >90% cash conversion were both significantly missed.

---

## 🌟 Key Application Features

### 1. 📊 Financial Dashboard
* Real-time KPI metric cards displaying Revenue, Operating Profit (EBIT), Operating Margin (%), and Operating Cash Flow (OCF).
* Clear Quarter-on-Quarter (QoQ) comparative growth percentages with emerald green indicators for gains and crimson red indicators for negative changes.
* Interactive Plotly charts:
  * **Revenue vs. Operating Profit Divergence**: Visualizes the decoupling of top-line growth from bottom-line profit.
  * **Operating Margin Progression vs. Guidance**: Tracks margin trajectory across 4 quarters against the 18% benchmark.
  * **Cash Flow vs. Accrual Profit (Accrual Gap)**: Highlights cash conversion degradation.
  * **Business Segment Mix**: Compares revenue contribution against segment profitability.

### 2. 📁 Excel Upload & Data Management
* Upload any custom Excel file (`.xlsx` or `.xls`).
* Reads the mandatory `Financial_Results` sheet with robust column validation and numeric error checking.
* Supports multi-sheet workbooks with optional `Segment_Data` and `Management_Commitments` sheets.
* Includes pre-packaged, built-in fictional data for **Apex Global Technologies Inc.**.
* **Download Sample Template**: 1-click button to download `sample_investor_data.xlsx` directly from the UI to inspect or edit.

### 3. 🎯 Investor Risk Radar
* 100% transparent, deterministic rule-based algorithms for risk detection:
  * **Margin Compression**: Flags when revenue grows while margin contracts by >20 bps.
  * **Cash Flow Decoupling**: Flags when OCF contracts or cash conversion drops below 75%.
  * **Segment Mix Asymmetry**: Detects when low-margin segments dilute higher-margin flagship units.
  * **Broken Guidance**: Quantifies exact basis point and percentage misses against public management promises.
* Displays why each risk was flagged, risk severity, category, and exact supporting figures.
* Aggregated **Earnings Call Scrutiny Index (0-100)** predicting analyst stance.

### 4. ❓ Wall Street Investor Question Generator
* Generates prioritized questions tailored to the detected risks.
* Categorized by analyst archetype (e.g. *Morgan Stanley Sell-Side Equity Analyst*, *Long/Short Value Fund Manager*, *Credit & Liquidity Analyst*).
* Displays:
  * Question Priority (`CRITICAL`, `HIGH`).
  * What Analysts Are Suspecting (the underlying bear thesis).
  * Financial Evidence Cited in the question.
  * Critical Missing Information that analysts will probe in follow-ups.

### 5. 💡 Suggested Responses & Governance Bridge
* Executive draft responses linked strictly to reported facts.
* Distinguishes between:
  * **Validated Evidentiary Anchors**: Facts verified in reported quarterly results.
  * **Data Gaps & Pending Disclosures**: Operational details pending the formal 10-Q filing.
  * **Unsupported Assumptions to Strictly Avoid**: Unfounded forward-looking statements that must never be made.
* Prominent regulatory and compliance disclaimers (Regulation FD & Safe Harbor adherence).

### 6. 🎙️ Interactive Mock Earnings Call Simulator
* Select any generated analyst question to rehearse.
* Type your draft response in the interactive executive rehearsal area.
* "Load Reference Answer" button to observe how an institutional-grade answer scores.
* **Transparent 5-Point Evaluation Rubric (0-100 Points)**:
  1. **Factual Grounding & Metric Citation (25 pts)**: Citing concrete numbers and percentages.
  2. **Addressing Core Problem & Root Cause (20 pts)**: Naming mix shifts and operational drivers.
  3. **Consistency with Filings & Guidance (20 pts)**: Avoiding contradictions with historical disclosures.
  4. **Realistic Uncertainty & Executive Balance (15 pts)**: Avoiding dangerous forward-looking guarantees.
  5. **Freedom from Evasive Buzzwords (20 pts)**: Detects and flags empty corporate clichés (e.g. *"synergies"*, *"cautiously optimistic"*, *"headwinds"*).
* Actionable coaching recommendations with itemized pass/fail breakdown.

### 7. 📘 Playbook & Business Competition Notes
* Concise summary of the business problem, presentation structure, and why this prototype is suitable for a winning live business competition demonstration.

---

## 📂 Project Architecture

```
test/
├── app.py                      # Main Streamlit web application & UI
├── financial_engine.py         # Excel loading, data validation, metrics & sample generator
├── risk_radar.py               # Deterministic rule-based risk detection algorithms
├── question_generator.py       # Prioritized Wall Street analyst question engine
├── response_advisor.py         # Evidence-anchored response playbooks & governance rules
├── mock_call_simulator.py      # Interactive Q&A evaluator with 5-point rubric & buzzword detector
├── create_sample_excel.py      # Standalone generator for sample Excel file
├── sample_investor_data.xlsx   # Pre-generated 3-sheet Excel workbook (Ready to use)
├── requirements.txt            # Python dependencies (streamlit, pandas, openpyxl, plotly)
└── README.md                   # Complete beginner guide & documentation
```

---

## 🛡️ Key Technical Design Principles
* **No Paid API Needed**: The application operates completely locally and deterministically.
* **Zero Hallucination**: Financial figures are mathematically checked against uploaded sheets.
* **Executive Aesthetics**: Styled with institutional deep navy blue (`#0B1120`), slate grey, emerald green, and crimson red indicators.
