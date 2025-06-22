from resume_parser import extract_text_from_pdf, split_into_sections
from jd_matcher import (
    match_keywords,
    get_missing_keywords,
    categorize_keywords,
    get_high_priority_keywords,
    suggest_keyword_locations,
)
from pdf_writer import write_suggestions_to_pdf
from keyword_extractor import extract_keywords_with_keybert
from spacy_filter import filter_keywords
from line_generator import generate_resume_line

if __name__ == "__main__":
    resume_path = "sample_resume.pdf"
    jd_path = "sample_job_description.txt"

    # Resume parsing
    resume_text = extract_text_from_pdf(resume_path)
    sections = split_into_sections(resume_text)

    # Load job description
    with open(jd_path, "r", encoding="utf-8") as f:
        jd_text = f.read()

    # 🔍 Extract and filter keywords
    bert_keywords = extract_keywords_with_keybert(jd_text, top_n=30)
    #print("\n🧠 KeyBERT Extracted Keywords:", bert_keywords)

    filtered_keywords = filter_keywords(bert_keywords)
    jd_keywords_text = " ".join(filtered_keywords)

    # Match & missing
    matched, total, matched_keywords = match_keywords(resume_text, jd_keywords_text)
    match_percent = round((matched / total) * 100, 2) if total else 0
    missing_keywords = get_missing_keywords(resume_text, jd_keywords_text)

    # Prioritize
    high_priority, _ = get_high_priority_keywords(jd_keywords_text, missing_keywords)

    # Location suggestions
    locations = suggest_keyword_locations(missing_keywords, sections)

    # AI Resume lines
    print(f"\n📊 Resume–JD Match: {match_percent}%")
    print(f"✅ Matched Keywords ({len(matched_keywords)}): {matched_keywords}")
    print(f"\n❌ Missing Keywords ({len(missing_keywords)}): {missing_keywords}")

    print("\n🔥 High-Priority Keywords (frequent in JD):")
    for word, count in high_priority:
        print(f" - {word} (mentioned {count} times)")

    print("\n📌 Suggested Technical Skills And Where To Add:")
    for word in missing_keywords:
        section = locations.get(word, "Other")
        print(f" • '{word}' → {section}")

    print("\n✍️ AI-Generated Resume Lines:")
    suggested_lines = []
    for word, _ in high_priority:
        line = generate_resume_line(word)  # should now generate more technical content
        section = locations.get(word, "General / Customize per context")
        print(f" • {line}  [{section}]")
        suggested_lines.append((word, line, section))

    # Categorize
    categorized = categorize_keywords(missing_keywords)

    # Generate PDF
    write_suggestions_to_pdf(
        categorized_keywords=categorized,
        high_priority=high_priority,
        locations=locations,
        suggested_lines=suggested_lines,
        match_percent=match_percent,
        matched_keywords=matched_keywords,
        missing_keywords=missing_keywords
    )

    print("\n📄 Suggestions saved to resume_suggestions.pdf")
