# 🚀 Generative AI ATS Resume Architect

## Overview
An automated, AI-powered web application designed to help job seekers bypass Applicant Tracking Systems (ATS). This tool dynamically restructures and optimizes existing resumes to perfectly align with target Job Descriptions.

**[Try the Live App Here]** *(Insert your Streamlit URL here)*

## How It Works
1. **Parses:** Extracts raw text from unstructured PDF resumes using `PyPDF2`.
2. **Optimizes:** Utilizes the Gemini 1.5 Flash LLM to rewrite bullet points using the XYZ formula (Action + Context + Result).
3. **Enforces Schema:** Employs strict Prompt Engineering to force the LLM to output clean JSON data, preventing AI hallucinations.
4. **Renders:** Programmatically generates a brand new, ATS-compliant PDF document from scratch using `FPDF`.

## Tech Stack
* **Language:** Python
* **Frontend/Hosting:** Streamlit
* **AI/LLM:** Google Generative AI (Gemini 1.5 Flash API)
* **Document Processing:** PyPDF2, FPDF
