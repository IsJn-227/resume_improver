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

    # 🔧 Reduced margins
    left_margin = 36   # Half inch
    right_margin = 36
    top_margin = 36
    bottom_margin = 36

    y = height - top_margin

    # ✏️ Reduced font sizes
    header_font = 14
    subheader_font = 12
    normal_font = 11
    line_spacing = 13

    c.setFont("Helvetica-Bold", header_font)
    title = "Resume Improvement Suggestions"
    text_width = c.stringWidth(title, "Helvetica-Bold", header_font)
    x_center = (width - text_width) / 2
    c.drawString(x_center, y, title)

    underline_y = y - 2  # slightly below the text baseline
    c.line(x_center, underline_y, x_center + text_width, underline_y)


    y -= 2 * line_spacing

    if match_percent is not None:
        c.setFont("Helvetica-Bold", subheader_font)
        c.drawString(left_margin, y, f"📊 Resume–JD Match: {match_percent}%")
        y -= 2 * line_spacing

        c.setFont("Helvetica", normal_font)
        if matched_keywords:
            matched_text = f"✅ Matched Keywords ({len(matched_keywords)}): {', '.join(matched_keywords)}"
            for line in textwrap.wrap(matched_text, width=100):
                c.drawString(left_margin, y, line)
                y -= line_spacing

        if missing_keywords:
            missing_text = f"❌ Missing Keywords ({len(missing_keywords)}): {', '.join(missing_keywords)}"
            for line in textwrap.wrap(missing_text, width=100):
                c.drawString(left_margin, y, line)
                y -= line_spacing
        y -= line_spacing

    if high_priority:
        c.setFont("Helvetica-Bold", subheader_font)
        c.drawString(left_margin, y, "🔥 High-Priority Keywords (frequent in JD):")
        y -= line_spacing * 2

        c.setFont("Helvetica", normal_font)
        for word, count in high_priority:
            c.drawString(left_margin + 15, y, f"- {word} (mentioned {count} times)")
            y -= line_spacing
            if y < bottom_margin:
                c.showPage()
                y = height - top_margin
                c.setFont("Helvetica", normal_font)
        y -= line_spacing

    def draw_section(title, items):
        nonlocal y
        if not items:
            return
        c.setFont("Helvetica-Bold", subheader_font)
        c.drawString(left_margin, y, title)
        y -= line_spacing

        c.setFont("Helvetica", normal_font)
        for word in items:
            c.drawString(left_margin + 15, y, f"- {word}")
            y -= line_spacing
            if y < bottom_margin:
                c.showPage()
                y = height - top_margin
                c.setFont("Helvetica", normal_font)
        y -= line_spacing

    if locations:
        c.setFont("Helvetica-Bold", subheader_font)
        c.drawString(left_margin, y, "🧠 Suggested Technical Skills And Where To Add:")
        y -= line_spacing * 2

        c.setFont("Helvetica", normal_font)
        for word, section in locations.items():
            c.drawString(left_margin + 15, y, f"• '{word}' → {section}")
            y -= line_spacing
            if y < bottom_margin:
                c.showPage()
                y = height - top_margin
                c.setFont("Helvetica", normal_font)
        y -= line_spacing

    if suggested_lines:
        c.setFont("Helvetica-Bold", subheader_font)
        c.drawString(left_margin, y, "✍️ AI-Generated Resume Lines:")
        y -= line_spacing * 2

        c.setFont("Helvetica", normal_font)
        for word, line, section in suggested_lines:
            wrapped_lines = textwrap.wrap(f"• {line}  [{section}]", width=105)
            for wrap in wrapped_lines:
                c.drawString(left_margin + 15, y, wrap)
                y -= line_spacing
                if y < bottom_margin:
                    c.showPage()
                    y = height - top_margin
                    c.setFont("Helvetica", normal_font)
        y -= line_spacing

    c.save()

