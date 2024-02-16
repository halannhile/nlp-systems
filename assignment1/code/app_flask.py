from flask import Flask, request, render_template
import ner
import spacy

app = Flask(__name__)

# Load the spaCy English model for dependency parsing
nlp = spacy.load("en_core_web_sm")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        with open('input.txt', 'r', encoding='utf-8') as file:
            return render_template('form.html', input=file.read())
    
    else:
        text = request.form['text']
        
        # Entity parsing
        entity_doc = ner.SpacyDocument(text)
        markup = entity_doc.get_entities_with_markup()
        
        # Dependency parsing
        doc = nlp(text)
        parse_results = []
        for sent in doc.sents:
            sentence_text = sent.text
            parse_result = {"sentence_text": sentence_text, "result": ""}
            for token in sent:
                parse_result["result"] += f"{token.text} {token.dep_} {token.head.text}\n"
            parse_results.append(parse_result)
        
        return render_template('result.html', markup=markup, parse_results=parse_results)

if __name__ == '__main__':
    app.run(debug=True)
