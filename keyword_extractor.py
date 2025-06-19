from keybert import KeyBERT

def extract_keywords_with_keybert(text, top_n=20):
    """
    Uses BERT embeddings to extract top keywords from input text.
    Returns: A list of important keywords/phrases.
    """
    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 2),
        stop_words='english',
        top_n=top_n
    )
    return [kw[0] for kw in keywords]
