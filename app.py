import streamlit as st
import PyPDF2
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import tempfile
import os

st.set_page_config(page_title="AI-Powered Resume Analyzer with ATS Scoring & Role Matching", layout="wide")

# ---------- USER NAME ----------
st.title("AI-Powered Resume Analyzer with ATS Scoring & Role Matching")

name = st.text_input("👤 Enter Your Name")

# ---------- ROLES ----------
roles_data = {
    "Embedded Engineer": {
        "skills": ["c", "microcontroller", "rtos", "uart", "spi", "i2c"],
        "companies": ["Intel", "Texas Instruments", "Qualcomm", "Bosch", "NXP"],
        "projects": ["UART in VHDL", "IoT Smart System"],
        "salary": "6-20 LPA"
    },
    "RTL Design Engineer": {
        "skills": ["verilog", "rtl", "timing", "synthesis"],
        "companies": ["Intel", "AMD", "NVIDIA", "Broadcom"],
        "projects": ["ALU Design", "FIFO Design"],
        "salary": "8-25 LPA"
    },
    "Software Engineer": {
        "skills": ["python", "java", "c++", "dsa"],
        "companies": ["Google", "Amazon", "Microsoft"],
        "projects": ["Chat App", "Code Platform"],
        "salary": "5-30 LPA"
    },
    "AI Engineer": {
        "skills": ["python", "ml", "dl", "nlp"],
        "companies": ["OpenAI", "Google", "NVIDIA"],
        "projects": ["Face Recognition", "Chatbot"],
        "salary": "8-35 LPA"
    }
}

# ---------- EXTRACT TEXT ----------
def extract_text(file):
    pdf = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

# ---------- ATS ----------
def ats_score(text):
    score = 0
    if "experience" in text: score += 20
    if "projects" in text: score += 20
    if "skills" in text: score += 20
    if "education" in text: score += 20
    if len(text) > 800: score += 20
    return score

# ---------- BREAKDOWN ----------
def breakdown(text):
    return {
        "Skills": 25 if "skills" in text else 10,
        "Projects": 25 if "project" in text else 10,
        "Experience": 25 if "experience" in text else 10,
        "Education": 25 if "education" in text else 10,
    }

# ---------- ROLE MATCH ----------
def role_match(text, role):
    data = roles_data[role]
    skills = data["skills"]

    matched = [s for s in skills if s in text]
    percent = int((len(matched) / len(skills)) * 100)

    missing = [s for s in skills if s not in text]

    suggestions = []
    if missing:
        suggestions.append("Missing skills: " + ", ".join(missing))

    suggestions += [
        "Add strong projects",
        "Add GitHub links",
        "Use measurable impact"
    ]

    return percent, missing, suggestions

# ---------- RESUME REVIEW ----------
def review_resume(text):
    if len(text) < 500:
        return "Your resume is too short. Add more content like projects and experience."
    elif "project" not in text:
        return "Projects section missing. Add strong technical projects."
    elif "experience" not in text:
        return "No experience mentioned. Add internships or practical exposure."
    else:
        return "Good resume! Improve by adding metrics and strong action words."

# ---------- HR TIPS ----------
hr_tips = [
    "Keep resume 1 page",
    "Use bullet points",
    "Avoid paragraphs",
    "Add achievements",
    "Clean formatting"
]

# ---------- PDF ----------
def generate_pdf(name, ats, role, match, suggestions, review, scores):
    path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
    doc = SimpleDocTemplate(path)
    styles = getSampleStyleSheet()

    content = []

    # Title
    content.append(Paragraph("Ultimate Resume Report", styles["Title"]))
    content.append(Spacer(1, 10))

    # Name
    content.append(Paragraph(f"Name: {name}", styles["Normal"]))
    content.append(Spacer(1, 10))

    # Scores
    content.append(Paragraph(f"ATS Score: {ats}", styles["Normal"]))
    content.append(Paragraph(f"Role Match: {match}%", styles["Normal"]))
    content.append(Spacer(1, 10))

    # Review
    content.append(Paragraph("Resume Review:", styles["Heading2"]))
    content.append(Paragraph(review, styles["Normal"]))
    content.append(Spacer(1, 10))

    # Suggestions
    content.append(Paragraph("Improvements:", styles["Heading2"]))
    for s in suggestions:
        content.append(Paragraph("- " + s, styles["Normal"]))
    content.append(Spacer(1, 10))

    # HR Tips
    content.append(Paragraph("HR Tips:", styles["Heading2"]))
    for tip in hr_tips:
        content.append(Paragraph("- " + tip, styles["Normal"]))
    content.append(Spacer(1, 10))

    # ---------- PIE CHART IMAGE ----------
    chart_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name

    plt.figure()
    plt.pie(scores.values(), labels=scores.keys(), autopct='%1.1f%%')
    plt.savefig(chart_path)
    plt.close()

    content.append(Paragraph("Score Breakdown:", styles["Heading2"]))
    content.append(Image(chart_path, width=300, height=300))

    doc.build(content)

    return path

# ---------- UI ----------
file = st.file_uploader("📄 Upload Resume", type=["pdf"])

if file and name:
    text = extract_text(file)

    if text.strip() == "":
        st.error("Cannot read PDF")
    else:
        # ATS
        st.header("📊 ATS Score")
        ats = ats_score(text)
        st.progress(ats)

        # Breakdown
        st.header("📊 Score Breakdown")
        scores = breakdown(text)

        fig, ax = plt.subplots()
        ax.pie(scores.values(), labels=scores.keys(), autopct='%1.1f%%')
        st.pyplot(fig)

        # Review
        st.header("🧠 Resume Review")
        review = review_resume(text)
        st.info(review)

        # Role
        st.header("🎯 Role Selection")
        role = st.selectbox("Select Role", list(roles_data.keys()))

        match, missing, suggestions = role_match(text, role)
        data = roles_data[role]

        st.subheader("📈 Role Match")
        st.progress(match)

        st.subheader("🏢 Companies")
        st.write(", ".join(data["companies"]))

        st.subheader("💰 Salary Range")
        st.success(data["salary"])

        st.subheader("💡 Projects")
        for p in data["projects"]:
            st.write("- " + p)

        st.subheader("📉 Improvements")
        for s in suggestions:
            st.write("- " + s)

        # HR Tips
        st.header("🧑‍💼 HR Tips")
        for tip in hr_tips:
            st.write("- " + tip)

        # PDF
        pdf = generate_pdf(name, ats, role, match, suggestions, review, scores)
        with open(pdf, "rb") as f:
            st.download_button("📥 Download Full Report", f, "Resume_Report.pdf")

elif file and not name:
    st.warning("⚠️ Please enter your name first")
