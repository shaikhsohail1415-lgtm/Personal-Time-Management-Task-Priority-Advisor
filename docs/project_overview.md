# Project Overview

Personal Time Management & Task Priority Advisor solves the practical problem of deciding what to work on first when several tasks compete for limited time.

The application separates natural-language understanding from decision making. LangChain/LLM extracts structured task information and generates explanations; a Mamdani Fuzzy Inference System calculates the priority score.

## Architecture

User → Streamlit → LangChain extraction → Pydantic tasks → derived metrics → Mamdani FIS → ranking → LangChain explanation → dashboard.
