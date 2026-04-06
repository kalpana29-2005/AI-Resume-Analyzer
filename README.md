AI Powered Resume Analyzer with ATS Scoring and Role Matching

Overview
This project is a web application that analyzes resumes and provides ATS based scoring, role matching, and improvement suggestions. It helps students and job seekers understand how well their resume performs and how to improve it for specific job roles.

Features
ATS Score Analysis
Evaluates resumes based on key sections like skills, projects, experience, and education

Score Breakdown
Provides a visual understanding of resume strengths and weaknesses using charts

Resume Review
Gives feedback on missing sections, short content, and overall quality

Role Based Matching
Supports roles such as Embedded Engineer, RTL Design Engineer, Software Engineer, and AI Engineer
Calculates match percentage and highlights missing skills

Career Insights
Suggests companies, salary ranges, and relevant projects for each role

PDF Report Generation
Creates a downloadable report containing scores, feedback, suggestions, and charts

HR Tips
Provides best practices like using bullet points, keeping resume concise, and adding achievements

Tech Stack
Python
Streamlit
PyPDF2
Matplotlib
ReportLab

Project Structure
AI Resume Analyzer
app.py main application file
requirements.txt dependencies
README.md documentation
gitignore ignored files
assets optional folder for sample files

How to Run Locally

Step 1 Clone the repository
git clone https://github.com/kalpana29_2005/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer

Step 2 Install dependencies
pip install -r requirements.txt

Step 3 Run the application
streamlit run app.py
