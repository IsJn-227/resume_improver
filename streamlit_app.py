import streamlit as st
import re
from resume_parser import extract_text_from_pdf, split_into_sections
from jd_matcher import match_keywords, get_missing_keywords, categorize_keywords, get_high_priority_keywords, suggest_keyword_locations, custom_stopwords
from pdf_writer import write_suggestions_to_pdf
from keyword_extractor import extract_keywords_with_keybert
from spacy_filter import filter_keywords
from line_generator import generate_resume_line

st.set_page_config(page_title="📄 Resume Improver", layout="centered")
st.title("📄 Resume Improver")
st.markdown("Upload your resume and paste a job description to get smart keyword suggestions and improvement tips!")

resume_file = st.file_uploader("📎 Upload your resume (PDF)", type=["pdf"])
jd_text = st.text_area("📝 Paste the Job Description below", height=300)

if st.button("🔍 Analyze Resume"):
    if not resume_file or not jd_text.strip():
        st.warning("⚠️ Please upload a resume and paste a job description.")
        st.stop()

    resume_text = extract_text_from_pdf(resume_file)
    resume_sections = split_into_sections(resume_text)

    # Step 1: Extract JD keywords and clean them
    bert_keywords = extract_keywords_with_keybert(jd_text, top_n=30)
    filtered_keywords = filter_keywords(bert_keywords)
    jd_keywords_text = " ".join(filtered_keywords)

    # Step 2: Match keywords using cleaned JD keywords
    matched_count, total_keywords, matched_keywords = match_keywords(resume_text, jd_keywords_text)
    missing_keywords = get_missing_keywords(resume_text, jd_keywords_text)

    # Step 3: Define clean_display before using it
    def clean_display(words):
        return sorted([w for w in words if w.isalpha() and len(w) > 2 and w.lower() not in custom_stopwords])

    display_matched = clean_display(matched_keywords)
    display_missing = clean_display(missing_keywords)

    match_percent = round((len(display_matched) / (len(display_matched) + len(display_missing))) * 100, 2) if (display_matched or display_missing) else 0

    # Step 4: Prioritize, categorize, suggest locations
    high_priority, _ = get_high_priority_keywords(jd_text, display_missing)
    categorized = categorize_keywords(display_missing)
    locations = suggest_keyword_locations(display_missing, resume_sections)

    # Step 5: Generate smart lines
    suggested_lines = []
    for word, _ in high_priority:
        line = generate_resume_line(word)
        section = locations.get(word, "General / Customize per context")
        suggested_lines.append((word, line, section))

    # Step 6: Display results (with tighter spacing)
    st.subheader(f"📊 Resume–JD Match: {match_percent}%")
    st.markdown(f"✅ **Matched Keywords ({len(display_matched)}):** {display_matched}")
    st.markdown(f"❌ **Missing Keywords ({len(display_missing)}):** {display_missing}")

    if high_priority:
        st.markdown("🔥 **High-Priority Keywords (frequent in JD):**")
        st.markdown(
            "<br>".join(
                [f"<span style='line-height:1.2'>• <b>{word}</b> (mentioned {count} times)</span>"
                 for word, count in high_priority]
            ),
            unsafe_allow_html=True
        )

    if locations:
        st.markdown("📌 **Suggested Technical Skills And Where To Add:**")
        st.markdown(
            "<br>".join(
                [f"<span style='line-height:1.2'>• '{word}' → <i>{section}</i></span>"
                 for word, section in locations.items()]
            ),
            unsafe_allow_html=True
        )

    if suggested_lines:
        st.markdown("✍️ **AI-Generated Resume Lines:**")
        st.markdown(
            "<br>".join(
                [f"<span style='line-height:1.2'>• {line}  [{section}]</span>"
                 for _, line, section in suggested_lines]
            ),
            unsafe_allow_html=True
        )

    # Step 7: Save to PDF
    write_suggestions_to_pdf(
        categorized_keywords=categorized,
        high_priority=high_priority,
        locations=locations,
        suggested_lines=suggested_lines,
        match_percent=match_percent,
        matched_keywords=display_matched,
        missing_keywords=display_missing
    )

    with open("resume_suggestions.pdf", "rb") as f:
        st.download_button("📥 Download Suggestions PDF", f, file_name="resume_suggestions.pdf")
