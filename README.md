# 🧠 Resume Improver – AI-Powered Resume Enhancer

Resume Improver is a Python-based tool that analyzes your resume against a given job description (JD), detects matched and missing keywords, categorizes them, and generates a polished PDF report with smart improvement suggestions.

> 🎯 Ideal for students, developers, and job seekers looking to improve their resume for ATS systems or match real-world job listings.

---

## 🚀 Features

- 📊 Resume–JD keyword match score
- ✅ Highlights matched and ❌ missing keywords
- 🔥 Flags high-priority JD terms based on frequency
- 🧠 Categorizes missing terms: skills, concepts, roles
- ✍️ Suggests AI-generated resume lines to improve impact
- 📄 Exports all findings into a clean, one-page PDF report

---

🚀 [Try Resume Improver Live on Streamlit](https://resumeimprover-ypeot5agzjyl68nudkmqkk.streamlit.app/)

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://resumeimprover-ypeot5agzjyl68nudkmqkk.streamlit.app/)

---

## ⚙️ How to Run

```bash
# Step 1: Clone the repo
git clone https://github.com/IsJn-227/resume_improver.git

# Step 2: Navigate into the project directory
cd resume_improver

# Step 3: Create a virtual environment (optional but recommended)
python -m venv .venv

# Step 4: Activate the virtual environment
.venv\Scripts\activate

# Step 5: Replace the sample files
# Overwrite:
#   - sample_job_description.txt with your own job description
#   - sample_resume.pdf with your own resume

# Step 6: Install dependencies and run the tool
pip install -r requirements.txt
python main.py

The resume_suggestions.pdf will be saved in the project folder.
