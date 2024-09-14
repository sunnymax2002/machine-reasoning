import requests

WIKIDATA_LANG = 'en'

PREFIX_E = 'wd:'
PREFIX_P = 'wdt:'

# Important wikidata properties
P_SUBCLASS_OF = 'P279'
P_INSTANCE_OF = 'P31'

def wikidata_actions_api(params: dict):
    # REF: https://www.jcchouinard.com/wikidata-api-python/
    API_ENDPOINT = "https://www.wikidata.org/w/api.php"
    r = requests.get(API_ENDPOINT, params = params).json()
    return r

def wikidata_sparql_api(query: str):
    # You can experiment with SPARQL query at https://query.wikidata.org/

    # REF: https://stackoverflow.com/questions/55961615/how-to-integrate-wikidata-query-in-python
    API_ENDPOINT = 'https://query.wikidata.org/sparql'
# query = '''
# SELECT ?item ?itemLabel ?linkcount WHERE {
#     ?item wdt:P31/wdt:P279* wd:Q35666 .
#     ?item wikibase:sitelinks ?linkcount .
# FILTER (?linkcount >= 1) .
# SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" . }
# }
# GROUP BY ?item ?itemLabel ?linkcount
# ORDER BY DESC(?linkcount)
# '''
    r = requests.get(API_ENDPOINT, params = {'format': 'json', 'query': query}).json()
    return r

def search_entity(item: str):
    # Wikidata API to look-up terms and map to standard ontology: https://towardsdatascience.com/extract-knowledge-from-text-end-to-end-information-extraction-pipeline-with-spacy-and-neo4j-502b2b1e0754
    # url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={item}&language=en&format=json"
    params = {
        'action': 'wbsearchentities',
        'format': 'json',
        'language': WIKIDATA_LANG,
        'search': item
    }    
    data = wikidata_actions_api(params=params)

    return data

def get_entity(item: str):
    params = {
        'action': 'wbgetentities',
        'format': 'json',
        'languages': WIKIDATA_LANG,
        'ids': item,
        'props': 'labels|descriptions'
    }    
    data = wikidata_actions_api(params=params)

    return data

def get_typeof(item: str, subclass=False):
    """If subclass=True, Returns the uri(s) of all the wikidata entities whose subclass the item (Q...) is,
    else, returns instanceOf...
    """

    rel_type = P_SUBCLASS_OF if subclass else P_INSTANCE_OF
    try:
        r = wikidata_sparql_api(f'''SELECT ?class
    WHERE
    {{
    {PREFIX_E}{item} {PREFIX_P}{rel_type} ?class
    }}''')
        
        res = []
        for c in r['results']['bindings']:
            res.append(c['class']['value'])
        return res
    except:
        return []

# res = get_typeof('Q11748378')

# print('done')