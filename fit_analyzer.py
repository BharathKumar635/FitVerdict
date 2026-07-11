import os
import json
from dotenv import load_dotenv
from groq import Groq

def analyze_fit(resume_text, job_description):
    """
    Analyzes the fit between a candidate's resume and a job description.
    
    Args:
        resume_text (str): The plain text extracted from the candidate's resume PDF.
        job_description (str): The job description text.
        
    Returns:
        dict: A dictionary containing:
            - "verdict": One of "Qualified", "Almost There", "Not Yet"
            - "reasons": A list of exactly 3 concise supporting reasons
            
    Raises:
        ValueError: If API key is missing, API call fails, JSON parsing fails, or validation fails.
    """
    # 1. Load the Groq API key from the environment
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    
    # 2. Validate that the key exists
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set. Please add it to your environment or .env file.")
        
    # 3. Create the Groq client
    client = Groq(api_key=api_key)
    
    # 4. Construct a clear prompt
    prompt = f"""You are an AI recruitment assistant.

Compare the candidate's resume against the provided job description.

Your task is to choose exactly one verdict:
1. Qualified
2. Almost There
3. Not Yet

Classification criteria:

QUALIFIED:
The candidate strongly satisfies most core and mandatory job requirements and does not have major critical gaps.

ALMOST THERE:
The candidate satisfies several important requirements but has meaningful gaps in some required skills, experience, qualifications, or technologies.

NOT YET:
The candidate lacks several core or critical requirements necessary for the role.

Provide exactly three concise reasons supporting your verdict.

Rules:
- Base the analysis only on information explicitly present in the resume and job description.
- Never invent candidate skills, experience, certifications, education, or qualifications.
- Never assume that the candidate possesses a skill that is not explicitly supported by the resume.
- Consider mandatory requirements more heavily than preferred or optional requirements.
- Consider relevant years of experience when explicitly stated.
- Consider education and certifications only when relevant to the job description.
- Be fair and evidence-based.
- Keep every reason concise and specific.
- Mention strengths and gaps where appropriate.
- Extract and list all skills and capabilities present in both the candidate resume and the job description under "matched_skills". Do not leave out any matching skills.
- Extract and list all skills, technologies, and qualifications required/mentioned in the job description that are NOT present in the candidate resume under "missing_skills". Do not leave out any missing skills.
- Return exactly one valid verdict.
- Return exactly three reasons.
- Return ONLY valid JSON.
- Do not include markdown.
- Do not include additional explanations outside the JSON.

Required JSON format:
{{
    "verdict": "Almost There",
    "reasons": [
        "First concise reason.",
        "Second concise reason.",
        "Third concise reason."
    ],
    "matched_skills": [
        "React",
        "Node.js",
        "REST APIs"
    ],
    "missing_skills": [
        "TailwindCSS",
        "TypeScript",
        "Docker"
    ]
}}

CANDIDATE RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}"""

    # 5. Send the resume text and JD to the model
    # Use llama-3.3-70b-versatile and response_format to ensure JSON is returned
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            response_format={"type": "json_object"}
        )
    except Exception as e:
        raise ValueError(f"Failed to communicate with Groq API: {str(e)}") from e
        
    # 6. Receive the AI response
    response_text = completion.choices[0].message.content
    if not response_text:
        raise ValueError("Received empty response from the AI model.")
        
    # 7. Clean markdown code fences if the model returns them
    cleaned_text = response_text.strip()
    if cleaned_text.startswith("```json"):
        cleaned_text = cleaned_text[7:]
    elif cleaned_text.startswith("```"):
        cleaned_text = cleaned_text[3:]
    if cleaned_text.endswith("```"):
        cleaned_text = cleaned_text[:-3]
    cleaned_text = cleaned_text.strip()
    
    # 8. Parse the response safely using Python's built-in json module
    try:
        result = json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"AI response is not valid JSON. Response text: {response_text}") from e
        
    # 9-10. Validate the verdict and that exactly three reasons are returned
    if not isinstance(result, dict):
        raise ValueError("AI response must be a JSON object.")
        
    allowed_verdicts = ["Qualified", "Almost There", "Not Yet"]
    
    if "verdict" not in result:
        raise ValueError("Missing 'verdict' field in the AI response.")
        
    # Standardise case to match allowed verdicts in case of minor casing issues
    verdict = result["verdict"].strip()
    # Find matching case-insensitive verdict in allowed_verdicts
    matched_verdict = None
    for av in allowed_verdicts:
        if av.lower() == verdict.lower():
            matched_verdict = av
            break
            
    if not matched_verdict:
        raise ValueError(f"Invalid verdict '{verdict}' returned. Must be one of: {', '.join(allowed_verdicts)}.")
    
    result["verdict"] = matched_verdict
    
    if "reasons" not in result:
        raise ValueError("Missing 'reasons' field in the AI response.")
        
    reasons = result["reasons"]
    if not isinstance(reasons, list):
        raise ValueError("'reasons' field must be a list of strings.")
        
    if len(reasons) != 3:
        raise ValueError(f"AI response must contain exactly three reasons. Found {len(reasons)}.")
        
    for idx, reason in enumerate(reasons):
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError(f"Reason #{idx + 1} must be a non-empty string.")
            
    # Validate matched_skills
    if "matched_skills" not in result:
        raise ValueError("Missing 'matched_skills' field in the AI response.")
    if not isinstance(result["matched_skills"], list):
        raise ValueError("'matched_skills' field must be a list of strings.")
    for idx, skill in enumerate(result["matched_skills"]):
        if not isinstance(skill, str) or not skill.strip():
            raise ValueError(f"Matched skill at index {idx} must be a non-empty string.")
            
    # Validate missing_skills
    if "missing_skills" not in result:
        raise ValueError("Missing 'missing_skills' field in the AI response.")
    if not isinstance(result["missing_skills"], list):
        raise ValueError("'missing_skills' field must be a list of strings.")
    for idx, skill in enumerate(result["missing_skills"]):
        if not isinstance(skill, str) or not skill.strip():
            raise ValueError(f"Missing skill at index {idx} must be a non-empty string.")
            
    return result
