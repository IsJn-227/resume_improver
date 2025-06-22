from keybert import KeyBERT

def extract_keywords_with_keybert(text, top_n=20):
    """
    Uses BERT to extract top keywords and removes substring redundancies.
    """
    kw_model = KeyBERT(model='all-MiniLM-L6-v2')
    
    keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 2),
        stop_words='english',
        top_n=top_n
    )
    
    raw_keywords = [kw[0] for kw in keywords]

    # Remove keywords that are substrings of other longer ones
    def remove_substrings(words):
        words = sorted(set(words), key=len, reverse=True)
        unique = []
        for w in words:
            if not any(w in longer and w != longer for longer in unique):
                unique.append(w)
        return unique

    return remove_substrings(raw_keywords)
