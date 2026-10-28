# Personal Time Management & Task Priority Advisor

AI-powered college mini project using **LangChain + LLM + Mamdani Fuzzy Logic + Streamlit**.

## Problem Statement

Students and professionals often have multiple tasks with different deadlines, importance, duration and difficulty. A simple deadline sort or weighted average does not represent the uncertainty involved in human prioritization. This project combines natural-language understanding with a genuine fuzzy inference system to recommend what to do next.

## Objectives

- Understand tasks written in natural language.
- Extract multiple tasks into validated structured data.
- Calculate continuous urgency and time pressure.
- Apply Mamdani fuzzy inference using overlapping membership functions.
- Evaluate 20+ fuzzy rules.
- Aggregate fuzzy outputs and use centroid defuzzification.
- Rank tasks using calculated fuzzy scores.
- Generate an evidence-based natural-language explanation.

## Features

- Natural-language multi-task extraction.
- Manual task entry for offline/demo use.
- Urgency, importance, time pressure and difficulty inputs.
- Genuine triangular/trapezoidal membership functions.
- 22 Mamdani rules.
- MIN fuzzy AND and MAX aggregation.
- Centroid defuzzification.
- Priority table and charts.
- Rule firing-strength inspection.
- LangChain-generated explanation.
- Simple priority-based time allocation.
- User-friendly error handling.

## System Architecture

```text
User
 ↓
Streamlit UI
 ↓
Natural Language Input
 ↓
LangChain + LLM
 ↓
Pydantic Structured Task Extraction
 ↓
Validation
 ↓
Derived Metrics
 ↓
Mamdani Fuzzy Inference System
 ↓
Fuzzification
 ↓
Rule Evaluation (MIN)
 ↓
Aggregation (MAX)
 ↓
Centroid Defuzzification
 ↓
Priority Score
 ↓
Task Ranking
 ↓
LangChain Explanation
 ↓
Streamlit Dashboard
```

## Fuzzy Inputs

All inputs use 0–100 scales.

- **Urgency:** Low / Medium / High
- **Importance:** Low / Medium / High
- **Time Pressure:** Low / Medium / High
- **Difficulty:** Easy / Moderate / Difficult

Output:

- Very Low
- Low
- Medium
- High
- Very High

### Urgency

Urgency is a continuous function of time remaining. Overdue/today tasks receive 100; future deadlines decay smoothly rather than being handled by only three if/else buckets. Tasks without a deadline receive a documented low default.

### Time Pressure

Time pressure is derived from estimated task hours versus available hours using a smooth saturation function. This prevents the project from reducing the variable to a simple binary condition.

## Fuzzy Inference

For each task:

1. Fuzzify each crisp input.
2. Evaluate every rule.
3. Use MIN for fuzzy AND.
4. Clip the consequent membership function.
5. Aggregate consequents using MAX.
6. Apply centroid defuzzification.

Centroid:

`Priority = Σ(x × μ(x)) / Σμ(x)`

## LangChain Component

The natural-language workflow uses:

- `ChatPromptTemplate`
- `ChatOpenAI`
- `with_structured_output(PydanticModel)`
- LangChain Runnable chains
- A separate explanation chain

The LLM does not calculate the final priority. The fuzzy engine does. The explanation chain receives the real calculated values and is instructed not to invent or recalculate them.

## Technology Stack

- Python
- Streamlit
- LangChain
- OpenAI-compatible LLM through `langchain-openai`
- Pydantic
- NumPy
- Pandas
- Plotly
- python-dotenv

## Project Structure

```text
personal-time-management-advisor/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
├── ai/
│   ├── __init__.py
│   ├── extractor.py
│   ├── explainer.py
│   ├── prompts.py
│   └── chains.py
├── fuzzy/
│   ├── __init__.py
│   ├── membership.py
│   ├── rules.py
│   ├── inference.py
│   └── defuzzification.py
├── models/
│   ├── __init__.py
│   └── task.py
├── utils/
│   ├── __init__.py
│   ├── time_utils.py
│   ├── validation.py
│   └── helpers.py
├── ui/
│   ├── __init__.py
│   ├── components.py
│   └── charts.py
├── assets/
└── docs/
```

## Installation

Python 3.10+ is recommended.

```bash
git clone <your-repository-url>
cd personal-time-management-advisor
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Copy `.env.example` to `.env`:

```text
OPENAI_API_KEY=your_api_key_here
```

Never commit a real key.

## Run Locally

```bash
streamlit run app.py
```

Manual mode can be demonstrated without an LLM API key.

## Example Natural-Language Input

> I have a DBMS assignment due tomorrow. It is very important and will take 3 hours. I also have a presentation next week that will take 2 hours.

Expected behavior:

1. LangChain extracts two tasks.
2. Each task receives derived urgency/time-pressure values.
3. The fuzzy engine evaluates the complete rule base.
4. Each task receives a crisp priority score.
5. Tasks are ranked after fuzzy inference.
6. LangChain generates an explanation using those actual results.

## Screenshots

Add screenshots from your running application to `assets/` before final submission.

## Streamlit Community Cloud Deployment

1. Push the repository to GitHub.
2. Open Streamlit Community Cloud.
3. Create a new app and select the repository.
4. Set the main file to `app.py`.
5. In the app's Secrets settings, add:

```toml
OPENAI_API_KEY = "your_real_key"
```

6. Deploy.

Do not put the key in GitHub.

## Limitations

- Natural-language extraction depends on the configured LLM.
- Deadline interpretation is represented as a date; exact time-of-day is not currently modeled.
- The scheduling module is intentionally simple and is separate from fuzzy priority inference.
- The project is a decision-support tool, not a guaranteed optimal scheduling algorithm.

## Future Enhancements

- Calendar integration.
- User profiles and historical workload learning.
- More granular deadline timestamps.
- Automatic break optimization.
- Persistent task database.
- Alternative local LLM support.
- Sensitivity analysis for fuzzy rules.

## Viva Questions

**Q1. Why fuzzy logic?**  
Because task priority is not naturally binary. A deadline can be somewhat urgent, importance can be partly high, and time pressure can overlap between linguistic categories.

**Q2. Why Mamdani inference?**  
It is interpretable and allows human-readable rules such as “IF urgency is high AND importance is high THEN priority is very high.”

**Q3. What is fuzzification?**  
Converting a crisp input into degrees of membership in linguistic fuzzy sets.

**Q4. What is rule firing strength?**  
For an AND rule using MIN, it is the minimum membership degree among its antecedents.

**Q5. What is aggregation?**  
Combining activated consequent fuzzy sets, here using the MAX operator.

**Q6. Why centroid defuzzification?**  
It converts the final fuzzy output into a single continuous priority score.

**Q7. What does LangChain do?**  
It orchestrates prompts, LLM calls and structured output for natural-language task extraction and explanation.

**Q8. Does the LLM calculate priority?**  
No. The LLM extracts/ explains. The Mamdani fuzzy system calculates the priority.

**Q9. Why use Pydantic?**  
To validate and structure the LLM output into predictable task objects.

**Q10. What happens without an API key?**  
Manual mode remains usable, allowing the fuzzy system to be demonstrated independently.

## Author

**Name:** Add your name here  
**College:** Add your college name  
**Course / Class:** Add your course  
**Academic Year:** Add the current academic year
