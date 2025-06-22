from collections import Counter
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from fuzzywuzzy import fuzz
from nltk import pos_tag
from nltk.corpus.reader.wordnet import NOUN, VERB, ADJ, ADV

# Download necessary NLTK resources
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('omw-1.4', quiet=True)

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Extended domain-specific stopwords
custom_stopwords = {
    "experience", "responsible", "proficient", "proficiency", "strong", "skills", "skill", "tools", "tool", "tools"
    "systems", "system", "platform", "platforms", "knowledge", "working", "ability", "role", "team", "individual", " proficiency"
    "good", "capable", "interested", "familiarity", "foundation", "application", "apps", "learn", "like", "new", "passionate"
    "solution", "solutions", "write", "using", "clean", "maintain", "background", "bonus", "communication", "experience"
    "collaborative", "building", "understand", "require", "support", "design", "develop", "handle", "clear", "basic", "ability"
}
stop_words.update(custom_stopwords)

# Mapping NLTK POS tags to WordNet POS
def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return ADJ
    elif tag.startswith('V'):
        return VERB
    elif tag.startswith('N'):
        return NOUN
    elif tag.startswith('R'):
        return ADV
    else:
        return NOUN

def clean_text(text):
    """
    Cleans and lemmatizes input text.
    Keeps only nouns. Removes punctuation, stopwords, and converts to lowercase.
    """
    text = re.sub(r'[^\w\s]', '', text.lower())
    words = text.split()
    tagged = pos_tag(words)
    filtered = [
        lemmatizer.lemmatize(w, get_wordnet_pos(tag))
        for w, tag in tagged
        if tag.startswith('N') and lemmatizer.lemmatize(w, get_wordnet_pos(tag)) not in stop_words and len(w) > 2
    ]
    return filtered

from nltk.tokenize import word_tokenize

def match_keywords(resume_text, jd_text, threshold=85):
    """
    Looser keyword matching: tokenizes raw text and avoids over-cleaning.
    """
    resume_tokens = set(word_tokenize(resume_text.lower()))
    jd_tokens = set(word_tokenize(jd_text.lower()))

    matched = []
    for jd_word in jd_tokens:
        for res_word in resume_tokens:
            if jd_word == res_word or fuzz.partial_ratio(jd_word, res_word) >= threshold:
                matched.append(jd_word)
                break

    return len(matched), len(jd_tokens), list(set(matched))


def get_missing_keywords(resume_text, jd_text, threshold=85):
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
