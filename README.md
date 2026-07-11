# AI-Powered Fit Verdict Application

An application that compares a candidate's resume (uploaded as a PDF) with a Job Description (JD) using Groq API and the `llama-3.3-70b-versatile` model. It provides a classification verdict along with exactly three concise supporting reasons.

---

## Assignment Objective

The objective is to build a simple, clean, and interview-explainable pipeline that helps assess candidate fit for a role based on objective evidence from their resume and a given job description, without over-engineering or introducing unnecessary dependencies (e.g., classes, databases, vector stores, frameworks like LangChain, etc.).

---

## Features

- **PDF Text Extraction**: Uses `pypdf` to extract raw text content from uploaded resume PDFs.
- **AI-Powered Evaluation**: Sends resume text and Job Description directly to the Groq API utilizing Llama 3.3.
- **Structured JSON Responses**: Requests a specific JSON format from the model and parses/validates it in Python.
- **Prominent Verdict Classification**: Classifies candidates as either **Qualified**, **Almost There**, or **Not Yet**.
- **Evidence-Based Explanations**: Returns exactly three concise supporting reasons outlining strengths and missing qualifications.
- **Streamlit Interface**: Clean, interactive UI with spinner indicators, color-coded alerts for verdicts, and explicit error feedback.
- **Security First**: Uses `dotenv` to load API keys securely without hardcoding them in the source code.

---

## Tech Stack

- **Python**: Core programming language.
- **Streamlit**: Web interface framework.
- **Groq API** (`llama-3.3-70b-versatile` model): AI inference provider.
- **pypdf**: PDF parsing.
- **python-dotenv**: Environment variable management.

---

## Application Pipeline

```
User uploads Resume PDF
        ↓
User pastes Job Description
        ↓
User clicks "Analyze Fit"
        ↓
pypdf extracts plain text from Resume PDF
        ↓
Resume Text + Job Description
        ↓
Sent to Groq API
        ↓
Llama model analyzes candidate-job fit
        ↓
AI returns structured JSON:
{
    "verdict": "Almost There",
    "reasons": [
        "Reason 1",
        "Reason 2",
        "Reason 3"
    ]
}
        ↓
Python validates and parses JSON
        ↓
Streamlit displays:
- Verdict (Color-coded)
- Exactly 3 supporting reasons
```

---

## Project Structure

```text
fit-verdict/
│
├── app.py              # Main Streamlit application and layout configuration
├── fit_analyzer.py     # Groq API connection, prompting, JSON cleaning/validation
├── pdf_utils.py        # Plain-text extraction from PDFs using pypdf
├── requirements.txt    # Python dependencies list
├── .env.example        # Reference environment file for setup
├── .gitignore          # File rules to ignore local secrets and environments
└── README.md           # Instructions, explanations, and interview Q&A
```

---

## Installation & Setup

Follow these steps to run the application on your local machine:

### 1. Clone or Copy the Project
Ensure all files (`app.py`, `fit_analyzer.py`, `pdf_utils.py`, `requirements.txt`, etc.) are placed in the same directory.

### 2. Set Up a Virtual Environment (Optional but Recommended)
Open a terminal in the project directory and run:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (macOS/Linux)
source venv/bin/activate
```

### 3. Install Dependencies
Install all required libraries using pip:

```bash
pip install -r requirements.txt
```

### 4. Configure Your Groq API Key
1. Create a file named `.env` in the root of the project.
2. Copy the contents of `.env.example` into `.env`.
3. Add your actual Groq API key:
   ```text
   GROQ_API_KEY=gsk_your_actual_api_key_here
   ```

*(Note: The `.gitignore` file contains rules to prevent `.env` from being checked into Git control, maintaining security.)*

### 5. Run the Application
Start the Streamlit development server:

```bash
python -m streamlit run app.py
```

Streamlit will open the application in your default web browser automatically (typically at `http://localhost:8501`).

---

## How the Application Works

1. **Text Extraction**: The app accepts a PDF file upload. Using `pypdf.PdfReader`, the app iterates through all pages of the file, extracts the text using `extract_text()`, and compiles them into a single string.
2. **Groq Inference**: The extracted text along with the pasted job description is inserted into a prompt that commands the `llama-3.3-70b-versatile` model to act as a recruiter. The model is forced to reply with a valid JSON format and a temperature of `0` to keep classifications consistent.
3. **Structured Validation**: The application receives the JSON, cleans off any Markdown formatting blocks (e.g. ` ```json ` fences), and converts it into a Python dictionary. It runs validation checks to ensure the verdict is correct and exactly three reasons exist before displaying the outcome to the user.

---

## Verdict Categories

- 🟢 **Qualified**: The candidate strongly satisfies most core and mandatory job requirements and does not have major critical gaps.
- 🟡 **Almost There**: The candidate satisfies several important requirements but has meaningful gaps in some required skills, experience, qualifications, or technologies.
- 🔴 **Not Yet**: The candidate lacks several core or critical requirements necessary for the role.

---

## Interview Questions & Answers

These answers correspond directly to the logic written in this codebase:

### 1. Why was Streamlit chosen?
Streamlit was chosen because it allows python developers to create clean, responsive, and interactive user interfaces with minimal code. It eliminates the need for frontend code (HTML/CSS/JS) or backend routing, making the code simple, beginner-friendly, and easy to explain.

### 2. How does the user upload a resume?
The user uploads a resume using Streamlit's `st.file_uploader` component in [app.py](file:///c:/Users/bhara/Desktop/FitVerdict/app.py). We configure it to only accept `.pdf` files. It returns a file-like buffer object containing the PDF data when a file is selected.

### 3. How is PDF text extracted using pypdf?
In [pdf_utils.py](file:///c:/Users/bhara/Desktop/FitVerdict/pdf_utils.py), we initialize `pypdf.PdfReader(pdf_file)`. We loop through `reader.pages`, call `.extract_text()` on each page, ignore any empty pages (`None`), combine the text fragments, and return a clean, whitespace-trimmed string.

### 4. Why is the full resume text sent to the AI?
The full text is sent to ensure that the AI has access to all context (experience timeline, certification descriptions, educational details) rather than just a sparse list of keywords. Since `llama-3.3-70b-versatile` has a large context window, it can easily handle full-length resumes directly.

### 5. Why is the full job description sent to the AI?
The AI needs the entire job description to understand not just tech keywords, but also seniority requirements, mandatory vs. optional qualifications, domain expertise, and expectations, allowing it to perform a nuanced, context-aware analysis.

### 6. What is Groq API?
Groq is an AI inference cloud platform optimized for speed using custom hardware (LPU - Language Processing Unit). It enables LLMs like Llama 3.3 to run at extremely high tokens-per-second rates, ensuring near-instantaneous analysis inside the application.

### 7. Why is `llama-3.3-70b-versatile` used?
It is a state-of-the-art 70-billion-parameter open model that is highly capable of complex reasoning, classification, and strict JSON format compliance, while remaining cost-effective and fast to run via Groq.

### 8. What prompt is sent to the AI?
The prompt (constructed in [fit_analyzer.py](file:///c:/Users/bhara/Desktop/FitVerdict/fit_analyzer.py)) acts as a recruiter persona. It defines the classification criteria for the three verdicts, provides rules (e.g., base logic only on provided text, do not invent candidate capabilities), outlines the expected JSON output format, and supplies the candidate's resume and job description.

### 9. How does the model decide between Qualified, Almost There, and Not Yet?
The model decides by matching the candidate's qualifications against the JD criteria:
- **Qualified** if core requirements are met with no critical gaps.
- **Almost There** if several key requirements are met but meaningful gaps remain.
- **Not Yet** if several critical/core requirements are missing.

### 10. Why is JSON used for the AI response?
JSON is used because it provides a structured, predictable format that computers can parse easily. This bridges the gap between natural language generated by the AI and structured logic needed by Python to display fields neatly in the UI.

### 11. How is JSON converted into a Python dictionary?
In [fit_analyzer.py](file:///c:/Users/bhara/Desktop/FitVerdict/fit_analyzer.py), we use Python's built-in `json.loads()` function. It parses the sanitized JSON string and converts it into a native Python dictionary.

### 12. How does the application validate the AI output?
The application checks that the output is a dictionary, contains key fields (`verdict` and `reasons`), verifies the verdict is exactly one of the allowed options ("Qualified", "Almost There", "Not Yet"), and ensures `reasons` is a list containing exactly 3 non-empty strings.

### 13. Why must exactly three reasons be returned?
Exactly three reasons are requested to force the AI to summarize the comparison into high-level, digestible talking points (strengths, neutral matches, gaps), keeping the interface clean and uniform.

### 14. How is the API key kept secure?
The API key is saved in a local `.env` file and loaded into the environment using `python-dotenv`. It is referenced in code via `os.getenv("GROQ_API_KEY")`. The `.env` file is excluded from Git using `.gitignore` to prevent leaks.

### 15. What happens if the AI returns invalid JSON?
If `json.loads` fails or output validation fails, a `ValueError` is raised in [fit_analyzer.py](file:///c:/Users/bhara/Desktop/FitVerdict/fit_analyzer.py). The main function in [app.py](file:///c:/Users/bhara/Desktop/FitVerdict/app.py) catches the error and displays a user-friendly error box with `st.error()` without crashing the program.

### 16. What are the limitations of AI-generated recruitment decisions?
- **Text-Only Bias**: The AI only knows what is written; it cannot evaluate soft skills, interview performance, or portfolio quality.
- **Formatting Sensitive**: Differences in resume layouts might lead to text extraction errors.
- **Lack of Real-world Reasoning**: AI acts on textual heuristics and might misinterpret specialized domain experience not explicitly detailed in the JD.

---

## Responsible AI & Limitations

- **Objective Evaluation**: The AI is instructed to focus exclusively on professional skills, years of experience, relevant certifications, and education, ignoring personal or protected demographic characteristics.
- **Human-in-the-Loop**: This tool is an informational aid. Final hiring decisions should always involve human review.
