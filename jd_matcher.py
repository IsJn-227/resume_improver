from collections import Counter
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from fuzzywuzzy import fuzz

import nltk
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

lemmatizer = WordNetLemmatizer()

def clean_text(text):
    """
    Cleans and lemmatizes input text.
    Removes punctuation, stopwords, and converts to lowercase.
    """
    text = re.sub(r'[^\w\s]', '', text.lower())
    stop_words = set(stopwords.words('english'))
    custom_stopwords = {
        "experience", "responsible", "proficient", "strong", "skills",
        "knowledge", "working", "ability", "role", "team", "individual",
        "good", "capable", "interested"
    }
    stop_words.update(custom_stopwords)

    words = text.split()
    filtered = [lemmatizer.lemmatize(w) for w in words if w not in stop_words]
    return filtered

def match_keywords(resume_text, jd_text, threshold=85):
    """
    Compares resume and JD using lemmatization + fuzzy matching.
    Returns match count, total JD keywords, and matched keyword list.
    """
    resume_tokens = clean_text(resume_text)
    jd_tokens = clean_text(jd_text)

    matched = []
    for jd_word in jd_tokens:
        for res_word in resume_tokens:
            if jd_word == res_word or fuzz.partial_ratio(jd_word, res_word) >= threshold:
                matched.append(jd_word)
                break

    return len(matched), len(set(jd_tokens)), list(set(matched))

def get_missing_keywords(resume_text, jd_text, threshold=85):
    """
    Returns list of missing JD keywords not found in resume.
    Uses fuzzy matching to allow flexible matching.
    """
    resume_tokens = clean_text(resume_text)
    jd_tokens = clean_text(jd_text)

    missing = []
    for jd_word in set(jd_tokens):
        matched = any(
            jd_word == res_word or fuzz.partial_ratio(jd_word, res_word) >= threshold
            for res_word in resume_tokens
        )
        if not matched and len(jd_word) > 2:
            missing.append(jd_word)

    return sorted(missing)

def categorize_keywords(keywords):
    """
    Classifies missing keywords into categories:
    - skills: tech tools, frameworks, languages
    - concepts: CS or engineering fundamentals
    - roles: position-related terms
    - others: everything else
    """
    keyword_map = {
        "skills": {"python", "sql", "git", "rest", "apis", "flask", "django", "docker", "aws"},
        "concepts": {"control", "structures", "version", "algorithms", "problem-solving"},
        "roles": {"developer", "engineer", "internship"},
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
    Identifies high-priority missing keywords based on frequency in the JD.
    """
    jd_tokens = clean_text(jd_text)
    freq = Counter(jd_tokens)

    high_priority = []
    normal = []

    for word in missing_keywords:
        if freq[word] >= min_occurrences:
            high_priority.append((word, freq[word]))
        else:
            normal.append(word)

    return high_priority, normal

def suggest_keyword_locations(missing_keywords, resume_sections):
    """
    Suggests which resume section each missing keyword should go in.
    """
    suggestions = {}

    for keyword in missing_keywords:
        keyword_lower = keyword.lower()

        if keyword_lower in {"python", "sql", "flask", "django", "git", "excel", "tableau", "docker", "aws"}:
            suggestions[keyword] = "Skills / Technical Skills"
        elif keyword_lower in {"communication", "teamwork", "leadership", "collaboration", "management"}:
            suggestions[keyword] = "Experience / Projects"
        elif keyword_lower in {"internship", "developer", "analyst", "designer"}:
            suggestions[keyword] = "Work Experience"
        elif keyword_lower in {"algorithms", "structures", "data", "problem-solving"}:
            suggestions[keyword] = "Projects / Education"
        else:
            assigned = False
            for section, content in resume_sections.items():
                if keyword_lower in content.lower():
                    suggestions[keyword] = section
                    assigned = True
                    break
            if not assigned:
                suggestions[keyword] = "General / Customize per context"

    return suggestions
