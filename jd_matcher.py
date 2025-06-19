from collections import Counter
import re  # used here for text cleaning with regular expressions
from nltk.corpus import stopwords

def clean_text(text):
    """
    Cleans input text by removing punctuation, converting to lowercase,
    and removing stopwords (common words + custom irrelevant resume words).
    """
    # Remove punctuation and convert to lowercase
    text = re.sub(r'[^\w\s]', '', text.lower())

    # Get default stopwords and add custom words often found in resumes
    stop_words = set(stopwords.words('english'))
    custom_stopwords = {
        "experience", "responsible", "proficient", "strong", "skills",
        "knowledge", "working", "ability", "role", "team", "individual",
        "good", "capable", "interested"
    }
    stop_words.update(custom_stopwords)

    # Tokenize and filter
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    return ' '.join(filtered_words)

def match_keywords(resume_text, jd_text):
    """
    Compares words in resume and job description (JD).
    Returns:
        - matched_keywords_count: how many keywords overlap
        - total_jd_keywords: how many meaningful words in JD
        - list_of_matched_words: actual common words
    """
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(jd_text)

    resume_words = Counter(resume_clean.split())
    jd_words = Counter(jd_clean.split())

    matched = jd_words & resume_words  # intersection of both
    matched_keywords = list(matched.keys())  # matched qualities or requirements (keywords) in JD and resume

    return sum(matched.values()), sum(jd_words.values()), matched_keywords

def get_missing_keywords(resume_text, jd_text):
    """
    Identifies which JD keywords are missing from the resume.
    Filters out very short tokens.
    """
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(jd_text)

    resume_words = set(resume_clean.split())
    jd_words = set(jd_clean.split())

    missing_keywords = jd_words - resume_words

    # Optional: remove anything shorter than 3 characters (e.g. "in", "to")
    missing_keywords = [word for word in missing_keywords if len(word) > 2]

    return sorted(missing_keywords)

def categorize_keywords(keywords):
    """
    Classifies missing keywords into categories:
        - skills: tech tools, frameworks, languages
        - concepts: CS or engineering fundamentals
        - roles: position-related terms
        - others: everything else
    """
    keyword_map = {
        "skills": {"python", "sql", "git", "rest", "apis", "flask", "django"},
        "concepts": {"control", "structures", "version", "problemsolving"},
        "roles": {"developer"},
    }

    categorized = {"skills": [], "concepts": [], "roles": [], "others": []}

    for word in keywords:
        word = word.lower()
        found = False
        for category, group in keyword_map.items():
            if word in group:
                categorized[category].append(word)
                found = True
                break
        if not found:
            categorized["others"].append(word)

    return categorized

def get_high_priority_keywords(jd_text, missing_keywords, min_occurrences=2):
    """
    From JD, identify which of the missing keywords are high-priority based on frequency.
    """
    clean_jd = clean_text(jd_text)
    jd_words = clean_jd.split()
    freq = Counter(jd_words)

    high_priority = []
    normal = []

    for word in missing_keywords:
        if freq[word] >= min_occurrences:
            high_priority.append((word, freq[word]))  # include count
        else:
            normal.append(word)

    return high_priority, normal

def suggest_keyword_locations(missing_keywords, resume_sections):
    """
    Suggests where (which section) to insert missing keywords in the resume.
    Example: 'python' → Skills, 'teamwork' → Experience, etc.
    """
    suggestions = {}

    for keyword in missing_keywords:
        keyword_lower = keyword.lower()

        # Heuristics based on keyword nature
        if keyword_lower in {"python", "sql", "flask", "django", "git", "excel", "tableau"}:
            suggestions[keyword] = "Skills / Technical Skills"
        elif keyword_lower in {"communication", "teamwork", "leadership", "collaboration", "management"}:
            suggestions[keyword] = "Experience / Projects"
        elif keyword_lower in {"internship", "developer", "analyst", "designer"}:
            suggestions[keyword] = "Work Experience"
        elif keyword_lower in {"algorithms", "structures", "data", "problem-solving"}:
            suggestions[keyword] = "Projects / Education"
        else:
            # Fallback: check if a section has similar context
            assigned = False
            for section, content in resume_sections.items():
                if keyword_lower in content.lower():
                    suggestions[keyword] = section
                    assigned = True
                    break
            if not assigned:
                suggestions[keyword] = "General / Customize per context"

    return suggestions
