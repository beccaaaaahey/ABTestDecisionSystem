# ABTestDecisionSystem
An end-to-end AB testing pipeline integrating Python, statistical analysis, and LLM-powered business insights for product growth decisions

## Business Case
A subscription-based app is testing two paywall types:
- **Control**: Soft Paywall (allowing limited free content)
- **Treatment**: Hard Paywall (requires subscription immediately)

The goal is to examine the result of the Paywall implement and the trade-off between **Short -term" Revenue from the conversion increase** and **Long-term User Value decrease in retention**

 ## Tech Stack
- **Data Engineering**: SQL (CTEs, Window Functions)
- **Statistics**: Python, SciPy (T-Test, Chi-Square for SRM, Confidence Intervals)
- **Machine Learning**: PyTorch (Multilayer Perceptron for Churn Prediction)
- **Decision Automation**: Google Gemini API (LLM for Automated Executive Reporting)

## Project Architecture & Workflow
1. **`data_exteaction.sql`**: Simulates extraction from a data warehouse. Uses `ROW_NUMBER()` to handle event logs and calculate "Last Touchpoint" before churn.
2. **`generate_paywall_data.py`**: Generates a synthetic dataset of 5,000 users.
3. **`analyze_stats.py`**:
    - **SRM Check**: Chi-Square test to detect Sample Ratio Mismatch (ensuring 50/50 split integrity).
    - **Hypothesis Testing**: T-Tests for Conversion and Retention metrics.
    - **Interval Estimation**: Calculation of **Relative Lift** and **95% Confidence Intervals**.
4. **`analyze_ml.py` (PyTorch)**: A predictive model that identifies high-risk churners within the treatment group. It moves beyond aggregate averages to provide user-level risk scores.
5. **`ai_agent.py`**: An LLM-powered agent that synthesizes statistical results and ML insights into a professional Markdown business report.

## Key Insights & Methodology
- **Statistical Rigor**: Eliminated selection bias by verifying the **SRM p-value**, ensuring the experiment results are trustworthy.
- **Addressing Heterogeneous Treatment Effects (HTE)**: While aggregate data might show a lift in conversion, the PyTorch model reveals specific segments (e.g., long-term users) that are highly sensitive to the Hard Paywall.
- **Automated Decision Support**: Replaced manual data interpretation with an AI Agent that understands the "Meta culture" of prioritizing long-term user health over short-term gains.


