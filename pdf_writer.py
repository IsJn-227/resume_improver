from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
import textwrap

def write_suggestions_to_pdf(
    categorized_keywords,
    high_priority=None,
    locations=None,
    suggested_lines=None,
    match_percent=None,
    matched_keywords=None,
    missing_keywords=None,
    output_path="resume_suggestions.pdf"
):
    c = canvas.Canvas(output_path, pagesize=LETTER)
    width, height = LETTER
    y = height - 72

    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, y, "Resume Improvement Suggestions")
    y -= 40

    # 📊 Resume-JD Match Stats
    if match_percent is not None:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(72, y, f"📊 Resume–JD Match: {match_percent}%")
        y -= 30  # spacing after match %
        c.setFont("Helvetica", 12)
        if matched_keywords:
            matched_text = f"✅ Matched Keywords ({len(matched_keywords)}): {', '.join(matched_keywords)}"
            for line in textwrap.wrap(matched_text, width=90):
                c.drawString(72, y, line)
                y -= 15
        if missing_keywords:
            missing_text = f"❌ Missing Keywords ({len(missing_keywords)}): {', '.join(missing_keywords)}"
            for line in textwrap.wrap(missing_text, width=90):
                c.drawString(72, y, line)
                y -= 15
        y -= 30  # ✅ add spacing before next section

    # 🔥 High Priority Section
    if high_priority:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(72, y, "🔥 High-Priority Keywords (frequent in JD):")
        y -= 20
        c.setFont("Helvetica", 12)
        for word, count in high_priority:
            c.drawString(90, y, f"- {word} (mentioned {count} times)")
            y -= 15
            if y < 72:
                c.showPage()
                y = height - 72
        y -= 20

    # 🧠 Categorized Keywords
    def draw_section(title, items):
        nonlocal y
        if not items:
            return
        c.setFont("Helvetica-Bold", 14)
        c.drawString(72, y, title)
        y -= 20
        c.setFont("Helvetica", 12)
        for word in items:
            c.drawString(90, y, f"- {word}")
            y -= 15
            if y < 72:
                c.showPage()
                y = height - 72
        y -= 20

    draw_section("🧠 Suggested Technical Skills to Add:", categorized_keywords.get("skills", []))
    # draw_section("📚 CS Concepts or Fundamentals:", categorized_keywords.get("concepts", []))
    # draw_section("🎯 Role/Industry Terms:", categorized_keywords.get("roles", []))
    # draw_section("🔍 Other Possibly Relevant Terms:", categorized_keywords.get("others", []))

    # 📌 Suggested Insertion Points
    if locations:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(72, y, "📌 Where to Add These:")
        y -= 20
        c.setFont("Helvetica", 12)
        for word, section in locations.items():
            c.drawString(90, y, f"• '{word}' → {section}")
            y -= 15
            if y < 72:
                c.showPage()
                y = height - 72
        y -= 30  # ✅ spacing after this section

    # ✍️ Suggested Lines
    if suggested_lines:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(72, y, "✍️ AI-Generated Resume Lines:")
        y -= 30  # ✅ spacing for heading
        c.setFont("Helvetica", 12)
        for word, line, section in suggested_lines:
            wrapped_lines = textwrap.wrap(f"• {line}  [{section}]", width=100)
            for wrap in wrapped_lines:
                c.drawString(90, y, wrap)
                y -= 13  # ✅ tighter spacing between lines
                if y < 72:
                    c.showPage()
                    y = height - 72
        y -= 30  # ✅ spacing before next section

    # 💡 General Resume Tips
    c.setFont("Helvetica-Bold", 14)
    c.drawString(72, y, "💡 General Resume Tips:")
    y -= 20
    for tip in [
        "• Tailor your resume to the job description.",
        "• Use numbers and impact: 'Increased accuracy by 20%'",
        "• Keep it 1 page (if <2 years experience).",
    ]:
        c.setFont("Helvetica", 12)
        c.drawString(90, y, tip)
        y -= 15

    c.save()

