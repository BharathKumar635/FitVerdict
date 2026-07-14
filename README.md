# AI-Powered Fit Verdict Application

An AI-powered web application that compares a candidate's resume with a Job Description (JD) and provides a clear suitability verdict along with exactly three concise supporting reasons.

The application uses the **Groq API** with the **`llama-3.3-70b-versatile`** model to analyze the candidate's resume against the job requirements. The model returns a structured JSON response containing one of three verdicts:

* **Qualified**
* **Almost There**
* **Not Yet**

The application is intentionally designed with a lightweight architecture using Python and Streamlit, keeping the code modular, understandable, and easy to maintain.

---

## Assignment Objective

The objective of this assignment is to build an application that compares a candidate's resume with a Job Description and provides:

1. A verdict:

   * **Qualified**
   * **Almost There**
   * **Not Yet**

2. Exactly three concise reasons supporting the verdict.

### Example

**Resume Skills**

```text
React
JavaScript
TypeScript
Redux
HTML
CSS
```

**Job Description Skills**

```text
React
TypeScript
Redux
AWS
Docker
```

**Expected Output**

```text
Verdict: Almost There

Reasons:
1. Strong experience in React, TypeScript, and Redux.
2. Good match for the required frontend technologies.
3. Missing experience with AWS and Docker.
```

---

## Features

* **Resume PDF Upload** — Accepts candidate resumes in PDF format.
* **PDF Text Extraction** — Uses `pypdf` to extract readable text from uploaded resumes.
* **AI-Powered Fit Analysis** — Uses the Groq API with a Llama model to compare the complete resume against the Job Description.
* **Structured JSON Output** — Requests and validates a predictable JSON response from the AI model.
* **Three-Level Verdict Classification** — Classifies candidates as Qualified, Almost There, or Not Yet.
* **Exactly Three Supporting Reasons** — Provides concise, evidence-based explanations for every verdict.
* **Interactive Streamlit Interface** — Provides resume upload, Job Description input, loading indicators, verdict display, and error feedback.
* **Secure API Key Management** — Stores the Groq API key in a local `.env` file instead of hardcoding it into the source code.
* **Input Validation** — Prevents analysis when the resume or Job Description is missing.
* **Error Handling** — Gracefully handles PDF extraction failures, invalid AI responses, and API errors.

---

## Tech Stack

| Component                 | Technology                |
| ------------------------- | ------------------------- |
| Programming Language      | Python 3.11+              |
| Web Interface             | Streamlit                 |
| AI Inference              | Groq API                  |
| AI Model                  | `llama-3.3-70b-versatile` |
| PDF Processing            | pypdf                     |
| Environment Configuration | python-dotenv             |
| Data Exchange Format      | JSON                      |

The application intentionally avoids unnecessary dependencies such as databases, vector stores, LangChain, or additional frontend frameworks because they are not required for the assignment requirements.

---

## Architecture

The application separates responsibilities across three main Python files:

```text
app.py
    │
    ├── Handles Streamlit UI
    ├── Accepts user input
    ├── Validates input
    └── Displays results
              │
              ▼
      pdf_utils.py
              │
              ├── Reads uploaded PDF
              └── Extracts plain text
              │
              ▼
      fit_analyzer.py
              │
              ├── Builds AI prompt
              ├── Calls Groq API
              ├── Receives JSON response
              ├── Parses JSON
              └── Validates verdict and reasons
```

This separation keeps the code modular and gives each file a single clear responsibility.

---

## Application Pipeline

```text
User uploads Resume PDF
        ↓
User pastes Job Description
        ↓
User clicks "Analyze Fit"
        ↓
Validate Resume and Job Description
        ↓
pypdf extracts plain text from Resume PDF
        ↓
Resume Text + Job Description
        ↓
Sent to Groq API
        ↓
Llama model evaluates candidate-job fit
        ↓
AI returns structured JSON
        ↓
{
    "verdict": "Almost There",
    "reasons": [
        "Reason 1",
        "Reason 2",
        "Reason 3"
    ]
}
        ↓
Python parses and validates JSON
        ↓
Streamlit displays:
    - Verdict
    - Exactly three supporting reasons
```

---

## Project Structure

```text
fit-verdict/
│
├── app.py
├── fit_analyzer.py
├── pdf_utils.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── README.md
```

### File Responsibilities

| File               | Responsibility                                                                                         |
| ------------------ | ------------------------------------------------------------------------------------------------------ |
| `app.py`           | Main Streamlit application, UI components, input validation, analysis coordination, and result display |
| `fit_analyzer.py`  | Groq API communication, prompt construction, JSON parsing, and AI response validation                  |
| `pdf_utils.py`     | Extracts plain text from uploaded PDF resumes                                                          |
| `requirements.txt` | Lists required Python packages                                                                         |
| `.env`             | Stores the actual local Groq API key and should never be committed                                     |
| `.env.example`     | Provides an environment variable template without exposing secrets                                     |
| `.gitignore`       | Prevents sensitive and unnecessary files from being committed                                          |
| `README.md`        | Project documentation and setup instructions                                                           |

---

## How the Application Works

### 1. Resume Upload

The user uploads a PDF resume using Streamlit's `st.file_uploader`:

```python
uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)
```

When a PDF is selected, Streamlit returns a file-like object containing the uploaded data.

---

### 2. PDF Text Extraction

The uploaded file is passed to the PDF extraction utility:

```python
resume_text = pdf_utils.extract_text_from_pdf(uploaded_file)
```

Inside [`pdf_utils.py`](pdf_utils.py), `pypdf.PdfReader` reads the PDF:

```python
reader = pypdf.PdfReader(pdf_file)
```

The application loops through all pages:

```python
for page in reader.pages:
    text = page.extract_text()

    if text:
        extracted_text.append(text)
```

Finally, the extracted page contents are combined into one string:

```python
return "\n".join(extracted_text)
```

---

### 3. Job Description Input

The user enters the Job Description using a Streamlit text area:

```python
job_description = st.text_area(
    "Job Description Requirements",
    height=250,
    placeholder="Paste the job description or skill requirements here..."
)
```

The complete JD is preserved so the AI can analyze:

* Required technical skills.
* Experience requirements.
* Education requirements.
* Certifications.
* Domain knowledge.
* Mandatory and preferred qualifications.

---

### 4. Input Validation

Before calling the AI API, the application validates both required inputs.

Resume validation:

```python
if not st.session_state["resume_text"]:
    st.error(
        "Please upload a resume PDF file first."
    )
    return
```

Job Description validation:

```python
if not job_description.strip():
    st.error("Please enter a job description.")
    return
```

This prevents unnecessary API calls when required information is missing.

---

### 5. AI Analysis

The extracted resume text and Job Description are passed to:

```python
result = fit_analyzer.analyze_fit(
    st.session_state["resume_text"],
    job_description
)
```

The `analyze_fit()` function in [`fit_analyzer.py`](fit_analyzer.py):

1. Retrieves the Groq API key.
2. Creates the Groq client.
3. Constructs the evaluation prompt.
4. Sends the resume and JD to the selected Llama model.
5. Receives the structured JSON response.
6. Parses the JSON into a Python dictionary.
7. Validates the verdict and supporting reasons.
8. Returns the validated result.

---

## AI Response Format

The model is instructed to return only structured JSON:

```json
{
  "verdict": "Almost There",
  "reasons": [
    "Strong experience in React, TypeScript, and Redux.",
    "Good alignment with the core frontend requirements.",
    "Missing experience with AWS and Docker."
  ]
}
```

The expected structure is:

```text
Dictionary
│
├── verdict → String
│
└── reasons → List containing exactly 3 strings
```

---

## JSON Parsing and Validation

The Groq API response initially arrives as text.

Python converts the JSON string into a dictionary using:

```python
result = json.loads(response_text)
```

For example:

```text
JSON String
    ↓
json.loads()
    ↓
Python Dictionary
```

The application then validates:

* The result is a Python dictionary.
* The `"verdict"` key exists.
* The `"reasons"` key exists.
* The verdict is one of the three permitted categories.
* The reasons value is a list.
* Exactly three reasons are returned.
* Every reason is a non-empty string.

The allowed verdicts are:

```python
allowed_verdicts = {
    "Qualified",
    "Almost There",
    "Not Yet"
}
```

An example validation check is:

```python
if verdict not in allowed_verdicts:
    raise ValueError(
        f"Invalid verdict returned by AI: {verdict}"
    )
```

This prevents unexpected AI output from reaching the user interface.

---

## Why JSON Is Used

JSON provides a structured and predictable data format that can easily be processed by Python.

Without JSON, the AI might return free-form text:

```text
I think this candidate is almost qualified because they know React,
TypeScript and Redux, but they don't have AWS or Docker experience.
```

This is difficult to process reliably.

With JSON:

```json
{
  "verdict": "Almost There",
  "reasons": [
    "Strong React, TypeScript, and Redux experience.",
    "Good alignment with frontend requirements.",
    "Missing AWS and Docker experience."
  ]
}
```

Python can directly access:

```python
verdict = result["verdict"]
reasons = result["reasons"]
```

---

## Local Setup Instructions

### Prerequisites

Ensure the following are installed:

* Python 3.11 or later.
* Git.
* A valid Groq API key.

---

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd fit-verdict
```

---

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

For Windows Command Prompt:

```cmd
venv\Scripts\activate
```

For macOS/Linux:

```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file in the project root.

You can copy the provided example file:

**Windows PowerShell:**

```powershell
Copy-Item .env.example .env
```

**Windows Command Prompt:**

```cmd
copy .env.example .env
```

**macOS/Linux:**

```bash
cp .env.example .env
```

Open `.env` and configure your Groq credentials:

```env
GROQ_API_KEY=your_actual_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
```

> Never commit the `.env` file or expose your actual API key in source code.

---

### 5. Run the Application

```bash
python -m streamlit run app.py
```

The application will typically be available at:

```text
http://localhost:8501
```

---

## Implementation Decisions

### Why Streamlit?

Streamlit was selected because the assignment requires a focused Python application that:

* Accepts a PDF resume.
* Accepts Job Description text.
* Calls an AI service.
* Displays a verdict and supporting reasons.

Using Streamlit keeps the implementation concise and allows the application to be built primarily in Python without requiring a separate frontend framework or API layer.

### Why Send the Complete Resume to the AI?

The complete resume provides contextual information beyond individual keywords, including:

* Work experience.
* Project experience.
* Education.
* Certifications.
* Duration of experience.
* How technologies were applied.

This allows the model to make a more context-aware comparison.

### Why Send the Complete Job Description?

The complete JD helps the AI distinguish between:

* Core requirements.
* Preferred qualifications.
* Experience expectations.
* Education requirements.
* Certifications.
* Domain-specific requirements.

Keyword matching alone may not capture these distinctions.

### Why Use `temperature=0`?

Fit evaluation is a classification task rather than a creative-writing task.

Using:

```python
temperature=0
```

reduces randomness and encourages more consistent responses for the same input.

It improves reproducibility, although it does not guarantee mathematically identical outputs on every API call.

### Why Require Exactly Three Reasons?

Exactly three reasons provide a consistent output format while keeping the result concise and understandable.

The reasons can summarize:

1. Strong qualifications or matched requirements.
2. Overall alignment with the role.
3. Important missing requirements or gaps.

The prompt does not need to force this exact strength/match/gap ordering in every case, but it requires three evidence-based reasons.

---

## Security Considerations

### API Key Protection

The Groq API key is stored in:

```text
.env
```

The application retrieves it using:

```python
api_key = os.getenv("GROQ_API_KEY")
```

The `.env` file is excluded from Git using `.gitignore`.

A safe `.gitignore` should contain:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

### No Hardcoded Credentials

The application does not hardcode API keys directly into Python source files.

This prevents credentials from being accidentally exposed through a public GitHub repository.

### Input Validation

The application checks that:

* A resume has been provided.
* A Job Description has been entered.
* The uploaded resume is a PDF through the Streamlit file uploader configuration.
* Extracted text is available before analysis.
* The AI response follows the expected structure.

---

## Assumptions

The application is based on the following assumptions:

* The uploaded resume is a PDF containing machine-readable text.
* The Job Description contains sufficient information for meaningful comparison.
* The Groq API is available and accessible using the configured API key.
* The configured AI model is available to the associated Groq account.
* The AI should evaluate only information explicitly available in the resume and JD.
* The application is intended as a candidate-fit analysis aid rather than an autonomous hiring decision system.

---

## Trade-Offs

### Streamlit Instead of a Separate Frontend and Backend

The application uses Streamlit rather than Django, React, or a separate REST API.

**Advantages:**

* Smaller codebase.
* Faster development.
* Python-focused implementation.
* Easy local setup.
* Easy to explain.

**Trade-off:**

Streamlit provides less architectural separation and frontend customization than a traditional frontend-backend application.

---

### Direct LLM Evaluation Instead of Deterministic Scoring

The AI directly evaluates the candidate's overall fit rather than using a fixed numerical scoring formula.

**Advantages:**

* Can consider contextual experience.
* Can distinguish between core and optional requirements.
* Can evaluate education, experience, certifications, and technologies together.

**Trade-off:**

AI classifications may occasionally vary or interpret ambiguous requirements differently.

---

### Full Resume and JD Processing

The complete extracted resume and Job Description are sent to the AI model.

**Advantages:**

* Preserves context.
* Supports nuanced evaluation.
* Avoids losing relevant experience through premature filtering.

**Trade-off:**

Longer inputs consume more tokens and may increase API usage.

---

### pypdf Instead of OCR

The application uses `pypdf` for text extraction.

**Advantages:**

* Lightweight.
* Easy to use.
* Suitable for standard text-based resumes.

**Trade-off:**

Scanned or image-only resumes cannot be processed without an OCR solution.

---

## Limitations

* Scanned or image-only PDFs are not supported.
* AI output may vary slightly for ambiguous resumes or job descriptions.
* The application depends on internet connectivity and Groq API availability.
* The model can only evaluate information contained in the provided text.
* PDF layouts with unusual formatting may affect text extraction quality.
* The application should not be used as the sole basis for a hiring decision.

---

## Responsible AI Considerations

The application is designed as a decision-support tool, not an autonomous hiring system.

The AI is instructed to evaluate professional qualifications such as:

* Technical skills.
* Relevant experience.
* Education.
* Certifications.
* Job-specific requirements.

The evaluation should not rely on protected or irrelevant personal characteristics.

Final hiring decisions should always involve human review and broader evaluation beyond automated resume analysis.

---

## Future Improvements

Potential future enhancements include:

* OCR support for scanned resumes.
* Downloadable analysis reports.
* Resume and analysis history.
* User authentication.
* Batch resume processing.
* Automated test coverage.
* More detailed structured output showing matched and missing requirements.
* Model fallback handling for API availability issues.
* Production deployment with managed secret configuration.

---

## Author

**Bharath Kumar Reddy**

---

## License

This project was developed as part of a technical assessment.
