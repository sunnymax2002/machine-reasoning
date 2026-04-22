import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

def get_compound_phrase(token):
    """
    Reconstructs multi-word noun phrases (e.g., 'Microsoft Research Lab').
    """
    parts = [tok.text for tok in token.subtree]
    return " ".join(parts)

def extract_triplets(sentence):
    """
    Extract subject–predicate–object triplets from a sentence using spaCy.
    Handles direct objects, prepositional objects, indirect objects, and passive voice.
    """
    doc = nlp(sentence)
    triplets = []

    for token in doc:
        # Active voice subject
        if token.dep_ == "nsubj":
            subject = get_compound_phrase(token)
            relation = token.head.lemma_

            for child in token.head.children:
                if child.dep_ == "dobj":
                    triplets.append((subject, relation, get_compound_phrase(child)))
                if child.dep_ == "iobj":
                    triplets.append((subject, relation, get_compound_phrase(child)))
                if child.dep_ == "prep":
                    for pobj in child.children:
                        if pobj.dep_ == "pobj":
                            triplets.append((subject, relation + " " + child.text, get_compound_phrase(pobj)))

        # Passive voice subject
        if token.dep_ == "nsubjpass":
            subject = get_compound_phrase(token)
            relation = token.head.lemma_

            # Look for agent (the "by"-phrase)
            for child in token.head.children:
                if child.dep_ == "agent":
                    for pobj in child.children:
                        if pobj.dep_ == "pobj":
                            triplets.append((subject, relation + " by", get_compound_phrase(pobj)))

    return triplets


# -------------------------------
# Test examples
sentences = [
#     "The cat chased the mouse.",
#     "Alice works at Microsoft.",
#     "Power washing removes dirt from parking lots.",
#     "Alice works at Microsoft Research Lab.",
#     "John gave Mary a book.",
#     "The mouse was chased by the cat.",
#     "Trump attacked Iran for oil",
#     "The black cat jumped over the fence"
      "Mia is a girl"
 ]

for s in sentences:
    print(f"Sentence: {s}")
    print("Triplets:", extract_triplets(s))
    print("-" * 40)
