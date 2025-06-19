from resume_parser import extract_text_from_pdf, split_into_sections
from jd_matcher import match_keywords, get_missing_keywords, categorize_keywords, get_high_priority_keywords, suggest_keyword_locations
from pdf_writer import write_suggestions_to_pdf
from keyword_extractor import extract_keywords_with_keybert  # Import keyBERT-based extractor
from spacy_filter import filter_keywords  # Import spaCy-based POS filter
from line_generator import generate_resume_line

if __name__ == "__main__":
    resume_path = "sample_resume.pdf"  # Place your resume file here
    jd_path = "sample_job_description.txt"

    # Resume parsing
    resume_text = extract_text_from_pdf(resume_path)
    sections = split_into_sections(resume_text)

    # Load job description
    with open(jd_path, "r", encoding="utf-8") as f:
        jd_text = f.read()

    # 🔍 Extract top keywords from JD using KeyBERT
    bert_keywords = extract_keywords_with_keybert(jd_text, top_n=30)
    print("\n🧠 KeyBERT Extracted Keywords:", bert_keywords)

    # 🧠 Apply spaCy POS filtering to remove unhelpful keywords
    filtered_keywords = filter_keywords(bert_keywords)
    print("\n✅ Filtered Keywords (NOUN/PROPN only):", filtered_keywords)

    # Replace full JD with only extracted and filtered keywords for smarter matching
    jd_keywords_text = " ".join(filtered_keywords)

    # Match keywords
    matched, total, keywords = match_keywords(resume_text, jd_keywords_text)
    match_percent = round((matched / total) * 100, 2)

    print(f"\n📊 Resume-JD Match: {match_percent}%")
    print(f"✅ Matched keywords ({len(keywords)}): {keywords}")
    
    missing = get_missing_keywords(resume_text, jd_keywords_text)
    print(f"\n❌ Missing keywords ({len(missing)}): {missing}")

    # 🔥 High priority keywords
    high_priority, normal_keywords = get_high_priority_keywords(jd_keywords_text, missing)

    # 📌 Suggest where to add
    locations = suggest_keyword_locations(missing, sections)

    # ✍️ Generate resume lines (with section)
    print("\n✍️ Suggested Resume Line Improvements:")
    suggested_lines = []
    for word, _ in high_priority:
        line = generate_resume_line(word)
        section = locations.get(word, "General")
        print(f" - {line}  [{section}]")
        suggested_lines.append((word, line, section))

    # 🧠 Categorize missing
    categorized = categorize_keywords(missing)

    # 📝 Write all results to PDF
    write_suggestions_to_pdf(
    categorized_keywords=categorized,
    high_priority=high_priority,
    locations=locations,
    suggested_lines=suggested_lines,
    match_percent=match_percent,
    matched_keywords=keywords,
    missing_keywords=missing
    )

    print("\n📄 Suggestions saved to resume_suggestions.pdf")
