import streamlit as st
import pdf_utils
import fit_analyzer

def main():
    # 1. Configure the Streamlit page
    st.set_page_config(
        page_title="AI Fit Verdict",
        page_icon="📋",
        layout="centered"
    )

    # 2. Display Title and Subtitle
    st.title("AI Fit Verdict")
    st.markdown(
        "Compare a candidate's resume PDF with a Job Description (JD) to get an "
        "evidence-based fit verdict and key reasons using Groq AI."
    )

    # Collapsible 'How it Works' section
    with st.expander("ℹ️ How it Works", expanded=False):
        st.markdown(
            """
            1. **Upload Resume**: Upload the candidate's resume as a PDF file or click **Use Sample Resume**.
            2. **Paste Job Description**: Paste the target job requirements in the text area.
            3. **Extract Text**: The system extracts the raw text from the PDF using `pypdf`.
            4. **AI Analysis**: Groq's `llama-3.3-70b-versatile` model analyzes the candidate's skills, qualifications, and experience against the job requirements.
            5. **Structured Verdict**: The application displays a color-coded verdict (**Qualified**, **Almost There**, or **Not Yet**), exactly 3 key reasons, and lists of matched vs. missing capabilities.
            """
        )

    # 3. Input section: Resume PDF uploader and Job Description text area
    st.subheader("1. Upload Candidate Resume")
    col1, col2 = st.columns([3, 1])
    with col1:
        uploaded_file = st.file_uploader(
            "Upload Resume (PDF format only)", 
            type=["pdf"],
            label_visibility="collapsed",
            help="Upload the candidate's resume as a PDF file."
        )
    with col2:
        use_sample = st.button("Use Sample Resume", use_container_width=True)

    # Initialize session state for resume text and source tracking
    if "resume_text" not in st.session_state:
        st.session_state["resume_text"] = ""
        st.session_state["resume_source"] = ""

    # Check if a file is uploaded or sample is requested
    if uploaded_file:
        try:
            st.session_state["resume_text"] = pdf_utils.extract_text_from_pdf(uploaded_file)
            st.session_state["resume_source"] = uploaded_file.name
        except Exception as e:
            st.error(f"Error reading PDF file: {str(e)}")
            st.session_state["resume_text"] = ""
            st.session_state["resume_source"] = ""
    elif use_sample:
        import os
        sample_path = r"C:\Users\bhara\Desktop\Sravani_Resume.pdf"
        if os.path.exists(sample_path):
            try:
                with open(sample_path, "rb") as f:
                    st.session_state["resume_text"] = pdf_utils.extract_text_from_pdf(f)
                st.session_state["resume_source"] = "Sravani_Resume.pdf (Sample)"
            except Exception as e:
                st.error(f"Error reading sample PDF file: {str(e)}")
                st.session_state["resume_text"] = ""
                st.session_state["resume_source"] = ""
        else:
            st.error(f"Sample resume file not found at {sample_path}")
            st.session_state["resume_text"] = ""
            st.session_state["resume_source"] = ""
    elif not uploaded_file and st.session_state["resume_source"] not in ["", "Sravani_Resume.pdf (Sample)"]:
        # If the file uploader was cleared, reset the session state
        st.session_state["resume_text"] = ""
        st.session_state["resume_source"] = ""

    # Show a status message if resume is loaded
    if st.session_state["resume_text"]:
        st.success(f"📄 Loaded resume: **{st.session_state['resume_source']}**")

    st.subheader("2. Paste Job Description (JD)")
    job_description = st.text_area(
        "Job Description Requirements",
        height=250,
        placeholder="Paste the job description or skill requirements here..."
    )

    # 4. Action Button: Analyze Fit
    if st.button("Analyze Fit", type="primary"):
        # Validate inputs
        if not st.session_state["resume_text"]:
            st.error("Please upload a resume PDF file first or click 'Use Sample Resume'.")
            return

        if not job_description.strip():
            st.error("Please enter a job description.")
            return

        # 5. Analyze Fit using AI
        with st.spinner("Analyzing candidate fit with Groq API..."):
            try:
                result = fit_analyzer.analyze_fit(st.session_state["resume_text"], job_description)
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
                return

        # 7. Display Results Prominently
        st.divider()
        st.subheader("Analysis Results")
        
        verdict = result["verdict"]
        reasons = result["reasons"]

        # Color-coded display based on verdict
        if verdict == "Qualified":
            st.success(f"### Verdict: {verdict}")
        elif verdict == "Almost There":
            st.warning(f"### Verdict: {verdict}")
        else:
            st.error(f"### Verdict: {verdict}")

        st.markdown("#### Why?")
        for index, reason in enumerate(reasons, 1):
            st.write(f"**{index}.** {reason}")

        # Display Matched and Missing Capabilities
        matched_skills = result.get("matched_skills", [])
        missing_skills = result.get("missing_skills", [])

        st.divider()
        col_matched, col_missing = st.columns(2)
        
        with col_matched:
            st.markdown("#### ✅ Matched Capabilities")
            if matched_skills:
                for skill in matched_skills:
                    st.write(f"- {skill}")
            else:
                st.write("*No matches found.*")
                
        with col_missing:
            st.markdown("#### ❌ Gaps / Missing Capabilities")
            if missing_skills:
                for skill in missing_skills:
                    st.write(f"- {skill}")
            else:
                st.write("*No gaps identified.*")

   

if __name__ == "__main__":
    main()
