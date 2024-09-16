from typing import List

from transformers import pipeline

from models import *
from sbert_dist import sbert_embeddings
from utils import nearest_vector
from wikidata_tools import search_entity, get_typeof, get_entity

class KnowledgeExtractor:
    def __init__(self) -> None:
        self.rebel = None

    def load_babel(self):
        # Babel for text to entity, relation triples: https://huggingface.co/Babelscape/rebel-large
        self.rebel = pipeline('text2text-generation', model='Babelscape/rebel-large', tokenizer='Babelscape/rebel-large')

    def run_babel(self, text: str):
        # We need to use the tokenizer manually since we need special tokens.
        extracted_text = self.rebel.tokenizer.batch_decode([self.rebel(text, return_tensors=True, return_text=False)[0]["generated_token_ids"]])
        # print(extracted_text[0])
        return extracted_text

        # Parse the generated text and extract the triplets

    def babel_extract_2_triple(self, text: str):
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
    
    def normalize_entity(self, item: str):
        # Convert to lowercase
        item = item.lower()

        # Wikidata API to look-up terms and map to standard ontology: https://towardsdatascience.com/extract-knowledge-from-text-end-to-end-information-extraction-pipeline-with-spacy-and-neo4j-502b2b1e0754
        try:
            # Search item in wikidata
            data = search_entity(item)

            if 'search' in data and len(data['search']) > 0:
                # First do an exact text match in labels from qurry result
                q_lbls = [d['label'].lower() for d in data['search']]
                if item in q_lbls:
                    best_match = q_lbls.index(item)
                else:
                    # Find closest match between various labels from search results and item
                    embs = sbert_embeddings([item] + q_lbls)
                    best_match = nearest_vector(embs[0], embs[1:])

                entity = data['search'][best_match]

                # TODO: How to select type from inst_of / subclass_of?
                inst_of = get_typeof(entity['id'])
                if len(inst_of) > 0:
                    inst_of = get_entity(','.join(inst_of))

                subclass_of = get_typeof(entity['id'], subclass=True)
                if len(subclass_of) > 0:
                    subclass_of = get_entity(','.join(subclass_of))

                return KnowledgeTripletItem(
                    item=entity['label'],
                    info=entity['description'],
                    url=entity['concepturi'],
                    type_=inst_of
                )
            else:
                return KnowledgeTripletItem(item=item)
        except:
            return KnowledgeTripletItem(item=item)

    def extract(self, text: str) -> List[KnowledgeTriplet]:
        extracted_triplets_text = self.run_babel(text)

        # TODO: For each extracted text
        # Convert to Triple
        triplets = self.babel_extract_2_triple(extracted_triplets_text[0])
    
        kt_list = []
        for triple in triplets:
            std_data = {}
            for k, v in triple.items():
                if k in ('head', 'tail'):
                    std_data[k] = self.normalize_entity(v)
                if k == 'type':
                    pass
            
            kt = KnowledgeTriplet(
                subject=std_data['head'],
                object=std_data['tail'],
                relation=KnowledgeTripletItem(item=triple['type'])
            )

            kt_list.append(kt)

        return kt_list

engine = KnowledgeExtractor()

# Load and Run Babel
engine.load_babel()

texts = ["Eiffel Tower is located in Paris",
         "Punta Cana is a resort town in the municipality of Higuey, in La Altagracia Province, the eastern most province of the Dominican Republic",
         "Dog is a mammal",
         "Cleopatra was very beautiful",
         "Mahatma Gandhi was born on 2nd October"]

result = {}
for text in texts:
    result[text] = engine.extract(text)

print('done')

########

class Entity:
    subclassOf: str
    instOf: str

subj = Entity()
obj = Entity()
relation = 'relation'

def Map_Relation_Type():
    if subj is not None:
        if obj is not None:
            if subj.subclassOf is None:
                # Subj doesn't represent any type by itself (can we reconfirm this by check if subj root is a PROPN?)
                if subj.instOf is not None:
                    if relation is 'instanceOf':
                        assert subj.instOf == obj
                        print('subj isa obj')
                    else:
                        if obj is None:
                            # obj is value of a property of subj
                            print('subj has attribute relation with value obj')
                        else:
                            # TODO: is it required that obj is instance and not subclass?
                            print('subj relation obj')
                else:
                    # is this possible?
                    raise NotImplementedError()
            else:
                # Subj could be a type by itself, e.g. Film is a work of art
                raise NotImplementedError()
        else:
            # Can't map obj to a std entity
            if relation is not None:
                # TODO: obj might be a property value
                pass
            else:
                raise NotImplementedError()