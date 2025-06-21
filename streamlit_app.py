import streamlit as st
from resume_parser import extract_text_from_pdf
from jd_matcher import (
    match_keywords,
    get_missing_keywords,
    categorize_keywords,
    get_high_priority_keywords,
    suggest_keyword_locations,
)
from pdf_writer import write_suggestions_to_pdf

# Import extra tools for filtering
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from fuzzywuzzy import fuzz
import re
import nltk

nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)

# Setup NLP tools
stop_words = set(stopwords.words("english"))
custom_stopwords = {
    "experience", "responsible", "proficient", "strong", "skills", "knowledge",
    "working", "ability", "role", "team", "individual", "good", "capable", "interested",
    "clear", "building", "basic", "bonus", "collaborative", "communication", "background",
    "application", "apps", "clean", "code", "write", "understand", "maintain", "solution",
    "develop", "handle", "design", "create", "require", "ensure", "support"
}
stop_words.update(custom_stopwords)

lemmatizer = WordNetLemmatizer()


# 🧠 Clean + lemmatize a word
def clean_word(word):
    word = re.sub(r"[^\w\s]", "", word.lower())
    return lemmatizer.lemmatize(word)


# 💥 Fuzzy & smart keyword filter
def is_valid_keyword(word, jd_text, threshold=85):
    word = clean_word(word)
    if len(word) <= 2 or word in stop_words:
        return False
    score = fuzz.partial_ratio(word, jd_text.lower())
    return score >= threshold


# ----------------- Streamlit App -----------------

st.set_page_config(page_title="Resume Improver", layout="centered")
st.title("📄 Resume Improver")
st.markdown("Upload your resume and paste a job description to receive keyword analysis and suggestions.")

resume_file = st.file_uploader("📎 Upload your resume (PDF)", type=["pdf"])
jd_text = st.text_area("📝 Paste the Job Description below", height=250)

if st.button("🔍 Analyze Resume"):
    if resume_file and jd_text:
        resume_text = extract_text_from_pdf(resume_file)

        # Core NLP comparisons
        matched, total, matched_keywords = match_keywords(resume_text, jd_text)
        match_percent = round((matched / total) * 100, 2) if total else 0
        missing_keywords = get_missing_keywords(resume_text, jd_text)
        categorized = categorize_keywords(missing_keywords)
        high_priority, _ = get_high_priority_keywords(jd_text, missing_keywords)

        # Dummy mapping (simulate sections)
        resume_sections = {"Projects": resume_text, "Skills": resume_text}
        suggestions = suggest_keyword_locations(missing_keywords, resume_sections)

        # ✅ Display Results
        st.success(f"✅ Resume–JD Match Score: **{match_percent}%**")

        if matched_keywords:
            st.markdown("### ✅ Matched Keywords")
            st.markdown(", ".join(sorted(matched_keywords)))

        if missing_keywords:
            st.markdown("### ❌ Missing Keywords")
            st.markdown(", ".join(sorted(missing_keywords)))

        if high_priority:
            st.markdown("### 🔥 High-Priority JD Keywords")
            for word, count in high_priority:
                st.markdown(f"- **{word}** (mentioned {count} times)")

        if categorized:
            st.markdown("### 🧠 Categorized Missing Keywords")
            for category, words in categorized.items():
                valid = [w for w in words if is_valid_keyword(w, jd_text)]
                if valid:
                    st.markdown(f"**{category.capitalize()}:** {', '.join(valid)}")

        st.markdown("### 📌 Suggested Resume Sections")
        count = 0
        for word, section in suggestions.items():
            if is_valid_keyword(word, jd_text):
                st.markdown(f"- '{word}' → *{section}*")
                count += 1

        if count == 0:
            st.info("No strong keyword suggestions found based on filtering.")

        # Generate filtered PDF report
        filtered_missing = [w for w in missing_keywords if is_valid_keyword(w, jd_text)]
        filtered_categorized = categorize_keywords(filtered_missing)
        filtered_high_priority, _ = get_high_priority_keywords(jd_text, filtered_missing)
        filtered_suggestions = {
            k: v for k, v in suggestions.items() if is_valid_keyword(k, jd_text)
        }

        write_suggestions_to_pdf(
            categorized_keywords=filtered_categorized,
            high_priority=filtered_high_priority,
            locations=filtered_suggestions,
            suggested_lines=[],  # Optional
            match_percent=match_percent,
            matched_keywords=matched_keywords,
            missing_keywords=filtered_missing,
            output_path="resume_suggestions.pdf"
        )

        with open("resume_suggestions.pdf", "rb") as f:
            st.download_button("📥 Download Suggestions PDF", f, file_name="resume_suggestions.pdf")

    else:
        st.warning("⚠️ Please upload a resume and provide a job description.")
