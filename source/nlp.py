from transformers import pipeline
import requests

from models import *
from sbert_dist import sbert_embeddings, cosine_similarity

# Babel for text to entity, relation triples: https://huggingface.co/Babelscape/rebel-large
triplet_extractor = pipeline('text2text-generation', model='Babelscape/rebel-large', tokenizer='Babelscape/rebel-large')

text = "Eiffel Tower is located in Paris" # "Punta Cana is a resort town in the municipality of Higuey, in La Altagracia Province, the eastern most province of the Dominican Republic"

# We need to use the tokenizer manually since we need special tokens.
extracted_text = triplet_extractor.tokenizer.batch_decode([triplet_extractor(text, return_tensors=True, return_text=False)[0]["generated_token_ids"]])
print(extracted_text[0])
# Function to parse the generated text and extract the triplets
def extract_triplets(text):
    triplets = []
    relation, subject, relation, object_ = '', '', '', ''
    text = text.strip()
    current = 'x'
    for token in text.replace("<s>", "").replace("<pad>", "").replace("</s>", "").split():
        if token == "<triplet>":
            current = 't'
            if relation != '':
                triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
                relation = ''
            subject = ''
        elif token == "<subj>":
            current = 's'
            if relation != '':
                triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
            object_ = ''
        elif token == "<obj>":
            current = 'o'
            relation = ''
        else:
            if current == 't':
                subject += ' ' + token
            elif current == 's':
                object_ += ' ' + token
            elif current == 'o':
                relation += ' ' + token
    if subject != '' and relation != '' and object_ != '':
        triplets.append({'head': subject.strip(), 'type': relation.strip(),'tail': object_.strip()})
    return triplets
extracted_triplets = extract_triplets(extracted_text[0])
print(extracted_triplets)

# exit()

# Wikidata API to look-up terms and map to standard ontology: https://towardsdatascience.com/extract-knowledge-from-text-end-to-end-information-extraction-pipeline-with-spacy-and-neo4j-502b2b1e0754
def find_wikidata_entity(item):
  try:
    url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={item}&language=en&format=json"
    data = requests.get(url).json()
    # Return the first id (Could upgrade this in the future)

    if 'search' in data and len(data['search']) > 0:
        # Find closest match between [d['label'] for d in data['search']] and item, instead of reporting 1st result
        embs = sbert_embeddings([item] + [d['label'] for d in data['search']])
        emb0 = embs[0]

        sims = []
        for i in range(1, len(embs)):
            sims.append(cosine_similarity(emb0, embs[i]))

        best_match = sims.index(max(sims))

        return KnowledgeTripletItem(
            item=item,
            info=data['search'][best_match]['description'],
            url='https:' + data['search'][best_match]['url']
        )
    else:
        return None
  except:
    return None
    
for triple in extracted_triplets:
    std_data = {}
    for k, v in triple.items():
        if k in ('head', 'tail'):
            std_data[k] = find_wikidata_entity(v)
        if k == 'type':
            pass
    
    kt = KnowledgeTriplet(
        subject=KnowledgeTripletItem(item=triple['subject']),
        object=KnowledgeTripletItem(item=triple['object'])
    )
