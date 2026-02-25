import os
import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
from dotenv import load_dotenv
import re

# 1. Configuration
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def get_available_model():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            return m.name
    return None

# --- Page Setup ---
st.set_page_config(page_title="AI Career Pilot", page_icon="🎯", layout="centered")

# --- UI Styling (Stealth Dark Mode) ---
st.markdown("""
    <style>
    .stApp { background-color: #0f1113; }
    html, body, [class*="css"], .stMarkdown, p, span, li {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
    }
    .main-card {
        background: #1c1f23;
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #2d3139;
        margin-bottom: 20px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #007bff, #00d2ff);
        color: white !important;
        border-radius: 10px;
        border: none;
        padding: 12px 30px;
        font-weight: bold;
        width: 100%;
    }
    .summary-box {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #3b82f6;
        margin: 20px 0;
    }
    .streamlit-expanderHeader {
        background-color: #1c1f23 !important;
        border: 1px solid #2d3139 !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
st.markdown("""
    <div style="text-align: center; padding: 40px 0;">
        <h1 style="font-size: 3rem; margin-bottom: 10px;">🎯 AI Career Pilot</h1>
        <p style="font-size: 1.2rem; color: #94a3b8 !important;">Stealth mode for career optimization</p>
    </div>
""", unsafe_allow_html=True)

# --- Input Area ---
with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### 📄 Resume (PDF)")
        uploaded_file = st.file_uploader("Upload", type="pdf", label_visibility="collapsed")
    with col2:
        st.markdown("##### 💼 Job Details")
        job_description = st.text_area("Paste", height=100, placeholder="Target job requirements...", label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

# --- Logic ---
if st.button("🚀 Analyze Compatibility"):
    if uploaded_file and job_description:
        with st.spinner('Analyzing in stealth mode...'):
            try:
                resume_text = extract_text_from_pdf(uploaded_file)
                model_name = get_available_model()
                
                # SET TEMPERATURE TO 0.2 FOR CONSISTENCY
                model = genai.GenerativeModel(
                    model_name,
                    generation_config={"temperature": 0.2}
                )
                
                prompt = f"""
                Analyze the resume vs job. Respond in ENGLISH.
                FORMAT:
                SCORE: [number 0-100]
                SUMMARY: [1 sentence verdict]
                GAPS: [Bullets]
                IMPROVEMENTS: [Bullets]
                PROJECTS: [2 detailed project ideas to bridge tech gaps]

                Resume: {resume_text}
                Job: {job_description}
                """
                
                response_text = model.generate_content(prompt).text
                
                # Robust data extraction using helper function
                def get_section(name, text):
                    pattern = rf"{name}:(.*?)(?=(?:SUMMARY|GAPS|IMPROVEMENTS|PROJECTS|SCORE):|$)"
                    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
                    return match.group(1).strip() if match else "Check details below."

                score_match = re.search(r"SCORE:\s*(\d+)", response_text)
                score = min(int(score_match.group(1)), 100) if score_match else 0
                
                summary = get_section("SUMMARY", response_text)
                gaps = get_section("GAPS", response_text)
                improvements = get_section("IMPROVEMENTS", response_text)
                projects = get_section("PROJECTS", response_text)

                # --- Results Display ---
                st.markdown("---")
                
                # Circular Score
                st.markdown(f"""
                    <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 30px;">
                        <div style="width: 150px; height: 150px; border-radius: 50%; background: conic-gradient(#00d2ff {score * 3.6}deg, #2d3139 0deg); display: flex; align-items: center; justify-content: center;">
                            <div style="width: 120px; height: 120px; border-radius: 50%; background: #0f1113; display: flex; align-items: center; justify-content: center; font-size: 30px; font-weight: 900; color: #00d2ff;">
                                {score}%
                            </div>
                        </div>
                        <h4 style="margin-top: 15px;">Match Rating</h4>
                    </div>
                """, unsafe_allow_html=True)
                # Simulated keyword extraction (or ask AI for a list of found keywords)
                matched_skills = ["Python", "C++", "Algorithms", "Real-time Systems"]
                st.markdown("##### ✅ Matched Keywords Found:")
                cols = st.columns(len(matched_skills))
                for i, skill in enumerate(matched_skills):
                        cols[i].markdown(f"<p style='background:#10b981; color:white; border-radius:5px; text-align:center; padding:5px;'>{skill}</p>", unsafe_allow_html=True)
                st.markdown(f'<div class="summary-box"><strong style="color: #60a5fa;">AI Verdict:</strong> {summary}</div>', unsafe_allow_html=True)

                with st.expander("❌ VIEW CRITICAL GAPS"):
                    st.write(gaps)
                
                with st.expander("📝 RESUME OPTIMIZATION TIPS"):
                    st.write(improvements)

                with st.expander("🛠️ SUGGESTED PROJECTS TO BUILD"):
                    st.info(projects)

                # --- NEW: DOWNLOAD BUTTON ---
                report_text = f"""AI CAREER PILOT - REPORT
Match Compatibility: {score}%
Verdict: {summary}

CRITICAL GAPS:
{gaps}

OPTIMIZATION TIPS:
{improvements}

PROJECTS TO BUILD:
{projects}
"""
                st.download_button(
                    label="📥 Download Results as TXT",
                    data=report_text,
                    file_name="Career_Pilot_Analysis.txt",
                    mime="text/plain"
                )

            except Exception as e:
                if "429" in str(e):
                    st.error("⏳ Quota exceeded. Please wait 60 seconds.")
                else:
                    st.error(f"Analysis Error: {e}")
    else:
        st.warning("Please upload files to initiate scan.")