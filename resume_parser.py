import pdfplumber

def extract_text_from_pdf(path):
    """
    Extracts text from a PDF file using pdfplumber.
    Returns the full extracted text as a single string.
    """
    text = ""
    #opens the resume pdf
    with pdfplumber.open(path) as pdf:

        #gives the list of pages
        for page in pdf.pages:

            #this extract text function reads the text from each page and then we use text+= to concatenate all texts into one big string.
            page_text = page.extract_text()

            if page_text:  # ignore blank pages
                text += page_text + "\n"
    
    return text.strip()


import re #using re module for regular expressions (to match section headers like "Skills:", "Education", etc.)

def split_into_sections(resume_text):
    """
    Splits resume text into sections based on common headers.
    Returns a dictionary with section names as keys.
    """
    section_keywords = [
        "summary", "objective", "education", "experience", "work experience", 
        "skills", "projects", "certifications", "achievements", "publications",
        "internships" , "technical skills" , "awards"
    ]

    sections = {}
    current_section = "Other"
    sections[current_section] = []

    #parsing resume line by line and converting to lower case words in lines for comparison
    for line in resume_text.splitlines():
        line_lower = line.strip().lower()
        matched = False

        # to check if a line is exactly equal to a known section title and if yes, changes current_section to that section
        #this is similar to a dict, here we are making the section headings as keys and their description as values
        for keyword in section_keywords:
            if re.match(rf"^{keyword}[:\s]*$", line_lower):
                current_section = keyword.capitalize()
                sections[current_section] = []
                matched = True
                break
        #above we found which are the keys

        #now we will find the values of the respective keys, that is lowercase lines which are not section headings
        if not matched and line.strip():
            sections[current_section].append(line.strip())
        #if the line is not a section title and its not empty, we add it to the current section

    # Clean up sections by concatenating all lines of a particular section into a string
    for key in sections:
        sections[key] = "\n".join(sections[key])

    return sections

