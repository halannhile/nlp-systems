import json
from fastapi import FastAPI, Response
from pydantic import BaseModel
import spacy

app = FastAPI()

class Item(BaseModel):
    text: str = ''

@app.route("/", methods=["GET", "POST"])
def index(pretty: bool = False):
    content = "Content-Type: application/json"
    url = "http://127.0.0.1:8000/"
    answer = {
        "description": "Interface to the spaCy entity extractor and dependency parser",
        "usage_ner": 'curl -X POST -H "%s" -d@input.txt %s/ner' % (content, url),
        "usage_dep": 'curl -X POST -H "%s" -d@input.txt %s/dep' % (content, url),
    }
    if pretty:
        answer = prettify(answer)
    return answer

@app.post('/ner')
def process_ner(item: Item, pretty: bool = False):
    doc = nlp(item.text)
    entities = [{'start': ent.start_char, 'end': ent.end_char, 'label': ent.label_, 'text': ent.text} for ent in doc.ents]
    answer = {"input": item.text, "output": entities}
    if pretty:
        answer = prettify(answer)
    return answer

@app.post('/dep')
def process_dep(item: Item, pretty: bool = False):
    doc = nlp(item.text)
    dependencies = [{'token': token.text, 'dep': token.dep_, 'head': token.head.text} for token in doc]
    answer = {"input": item.text, "output": dependencies}
    if pretty:
        answer = prettify(answer)
    return answer

def prettify(result: dict):
    json_str = json.dumps(result, indent=2)
    return Response(content=json_str, media_type='application/json')

# Load spaCy model
nlp = spacy.load("en_core_web_sm")
