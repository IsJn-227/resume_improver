import spacy

# Load spaCy's small English model
nlp = spacy.load("en_core_web_sm")

def filter_keywords(keywords):
    """
    Filters a list of keywords, keeping only meaningful ones (nouns/proper nouns)
    """
    filtered = []
    for phrase in keywords:
        doc = nlp(phrase)
        # Keep phrase if it has any noun or proper noun and isn't too short
        if any(token.pos_ in ("NOUN", "PROPN") for token in doc) and len(phrase) > 2:
            filtered.append(phrase)
    return filtered
