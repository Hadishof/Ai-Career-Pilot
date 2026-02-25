🎯 AI Career Pilot: Intelligent Resume-to-Job Matching
AI Career Pilot is a high-performance recruitment tool designed to provide candidates with a data-driven competitive edge.
By leveraging the Gemini 1.5 Pro Large Language Model (LLM),
the application performs deep semantic analysis between a user's resume and a specific job description to identify technical gaps and provide actionable project recommendations to improve employability.

🛠️ Technical Architecture & Implementation
This project adheres to modern Software Engineering principles, specifically focusing on data privacy, modularity, and secure credential management:

  -Frontend Interface: Developed with Streamlit, providing a responsive, "stealth-mode" dashboard for real-time career optimization. 
  
  -AI Engine: Integrates the Google Generative AI (Gemini API) for advanced natural language processing and compatibility scoring.
  
  -Data Ingestion: Implements PyPDF2 for robust parsing of binary PDF data into structured text strings for LLM consumption.
  
  -Security & Environment: Utilizes python-dotenv to manage sensitive API credentials via local environment variables, ensuring zero exposure of secrets in version control.
  
  -Logic & Extraction: Employs Regular Expressions (Regex) to parse unstructured AI responses into categorized, actionable UI components.



🧠 Core Functionalities

  -Automated Skill-Gap Analysis: Pinpoints specific technologies, frameworks, or experiences missing from the candidate's profile based on target job requirements.

  -Semantic Match Rating: Generates a dynamic 0–100% compatibility score using LLM-based evaluation logic.

  -Bespoke Project Generation: Suggests two detailed, hands-on project ideas specifically tailored to bridge the identified technical gaps.

  -Report Exporting: Enables users to download a full analysis summary as a .txt file for offline reference and career planning.



🚀 Local Deployment Guide

  1-Clone the Repository: git clone https://github.com/Hadishof/ai-career-pilot.git and navigate into the directory.

  2-Configure Environment: Create a .env file in the root directory and add GOOGLE_API_KEY=your_api_key_here.

  3-Initialize Virtual Environment: Run python -m venv venv and activate it using .\venv\Scripts\activate (Windows) or source venv/bin/activate (Mac/Linux).

  4-Install Dependencies: Execute pip install -r requirements.txt within the active virtual environment.

  5-Launch Application: Run streamlit run app.py to start the local development server.
