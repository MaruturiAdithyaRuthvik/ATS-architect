import streamlit as st
import google.generativeai as genai
import PyPDF2
from fpdf import FPDF
import json

# --- 1. API SETUP ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- 2. THE PDF TEMPLATE DESIGN ---
class ResumePDF(FPDF):
    def add_section(self, title, body):
        # Section Header
        self.set_font("Arial", "B", 12)
        self.set_text_color(0, 51, 102) # Dark Blue
        self.cell(0, 8, title, ln=True)
        self.set_text_color(0, 0, 0) # Black
        
        # Section Content
        self.set_font("Arial", "", 11)
        # multi_cell automatically wraps text so it never overlaps!
        self.multi_cell(0, 6, txt=body.encode('latin-1', 'ignore').decode('latin-1'))
        self.ln(4)

# --- ADD THIS HELPER FUNCTION ---
def safe_string(value):
    """Flattens AI lists or dictionaries into clean text for the PDF."""
    if isinstance(value, list):
        # Join lists with a new line
        return "\n".join(str(v) for v in value)
    elif isinstance(value, dict):
        # Join dictionaries with a pipe separator
        return " | ".join(str(v) for k, v in value.items())
    elif value is None:
        return ""
    return str(value)

# --- UPDATE YOUR PDF GENERATOR ---
def generate_clean_pdf(json_data):
    pdf = ResumePDF()
    pdf.add_page()
    
    # Header: Name and Contact
    pdf.set_font("Arial", "B", 16)
    name = safe_string(json_data.get("Name", "Applicant Name"))
    pdf.cell(0, 10, name, ln=True, align="C")
    
    pdf.set_font("Arial", "", 10)
    contact = safe_string(json_data.get("ContactInfo", ""))
    pdf.cell(0, 6, contact, ln=True, align="C")
    pdf.ln(5)
    
    # Body Sections using the safe_string cleaner
    pdf.add_section("PROFESSIONAL SUMMARY", safe_string(json_data.get("Summary", "")))
    pdf.add_section("TECHNICAL SKILLS", safe_string(json_data.get("Skills", "")))
    pdf.add_section("PROFESSIONAL EXPERIENCE", safe_string(json_data.get("Experience", "")))
    pdf.add_section("PROJECTS", safe_string(json_data.get("Projects", "")))
    pdf.add_section("EDUCATION", safe_string(json_data.get("Education", "")))
    
    output_filename = "Flawless_ATS_Resume.pdf"
    pdf.output(output_filename)
    return output_filename

# --- 3. THE AI JSON ENGINE ---
def optimize_resume_to_json(old_text, jd):
    model = genai.GenerativeModel(
        'gemini-2.5-flash',
        generation_config={"response_mime_type": "application/json"}
    )
    
    # Notice the new "CRITICAL DATA RULE" section in the prompt
    prompt = f"""
    You are an ATS Resume Expert. Rewrite the provided RESUME to match the JOB DESCRIPTION.
    Output the result STRICTLY as a JSON object with these exact keys:
    "Name", "ContactInfo", "Summary", "Skills", "Experience", "Projects", "Education".
    
    CRITICAL DATA RULE: 
    The value for EVERY key must be a SINGLE FORMATTED STRING. 
    DO NOT output arrays `[]` or nested dictionaries `{{}}`. 
    For sections with multiple items (like Experience or Projects), combine them into one long string using newline characters (`\\n`) for line breaks.
    
    Example format for Experience:
    "Web Development Intern | Emterra Software | Mar 2024 - Nov 2024\\n- Handled customer inquiries...\\n- Resolved database issues..."
    
    JOB DESCRIPTION: {jd}
    ORIGINAL RESUME: {old_text}
    """
    
    response = model.generate_content(prompt)
    return json.loads(response.text)

# --- 4. STREAMLIT UI ---
st.title("✨ Flawless ATS Resume Architect")
st.write("Converts your old PDF into a structurally perfect, ATS-optimized template.")

jd = st.text_area("Paste Target Job Description:")
uploaded_file = st.file_uploader("Upload Original Resume (PDF)", type="pdf")

if st.button("Generate Flawless Resume"):
    if uploaded_file and jd:
        with st.spinner("Extracting, Analyzing, and Rendering..."):
            # Step A: Read Old Text
            reader = PyPDF2.PdfReader(uploaded_file)
            old_text = "".join([page.extract_text() for page in reader.pages])
            
            # Step B: Get JSON from AI
            ai_json_data = optimize_resume_to_json(old_text, jd)
            
            # Step C: Render New PDF
            final_pdf_path = generate_clean_pdf(ai_json_data)
            
            st.success("Resume built successfully with perfect formatting!")
            
            with open(final_pdf_path, "rb") as f:
                st.download_button("📥 Download Perfect Resume", f, "Optimized_Resume.pdf")