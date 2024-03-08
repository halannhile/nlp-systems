from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import ner
import spacy
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Entity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100))
    
    # Establish the relationship to the Relation model
    relations = db.relationship('Relation', backref='entity', lazy=True)

class Relation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    relation_text = db.Column(db.String(100))
    entity_id = db.Column(db.Integer, db.ForeignKey('entity.id'), nullable=False)


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
        # print("markup: ", markup)

        # Parse entities from markup using BeautifulSoup
        soup = BeautifulSoup(markup, 'html.parser')
        entities = [entity.text for entity in soup.find_all('entity')]
        print("entities: ", entities)

        # Store entities in the database
        entities_dict = {}
        sub_entities = set()  # Keep track of sub-entities

        for entity in entities:
            # Check if the entity is not a character from "entity markup"
            if len(entity) > 1:
                entities_dict[entity] = {"relations": []}
                # Split the entity into individual words and add them to sub_entities
                sub_entities.update(entity.split())

        # Dependency parsing
        doc = nlp(text)

        # Initialize parse_results list
        parse_results = []

        # Parse dependency relations and store in the dictionary
        for sent in doc.sents:
            sentence_text = sent.text
            parse_result = {"sentence_text": sentence_text, "result": ""}

            for token in sent:
                if token.dep_ != 'punct':
                    relation_text = f"{token.text} {token.dep_} {token.head.text}"
                    head_entity_text = token.head.text
                    entity_text = token.text

                    # Check if the token's head is part of any recognized entities
                    matching_entity_heads = [entity for entity in entities_dict if head_entity_text in entity.split()]

                    if matching_entity_heads:
                        # Use the first matching entity as the key
                        entity_key = matching_entity_heads[0]

                        # Add the head entity to the relations dictionary
                        relation_data = {"relation_text": relation_text}
                        entities_dict[entity_key]["relations"].append(relation_data)

                    # Check if the token's text is part of any recognized entities
                    matching_entities = [entity for entity in entities_dict if entity_text in entity.split()]
                    if matching_entities:
                        # Use the first matching entity as the key
                        entity_key = matching_entities[0]

                        # Add the head entity to the relations dictionary
                        relation_data = {"relation_text": relation_text}
                        entities_dict[entity_key]["relations"].append(relation_data)

                    # Update the parse result for rendering
                    parse_result["result"] += f"{token.head.text} {token.dep_} {token.text}\n"

            parse_results.append(parse_result)

        print("dict: ", entities_dict)

        # Store entities and relations in the database
        for entity_text, data in entities_dict.items():
            db_entity = Entity(text=entity_text)
            db.session.add(db_entity)

            for relation_data in data["relations"]:
                relation_text = relation_data["relation_text"]

                # Check if the relation already exists
                db_relation = Relation.query.filter_by(relation_text=relation_text).first()

                if not db_relation:
                    # If the relation does not exist, create it
                    db_relation = Relation(relation_text=relation_text)

                # Associate the relation with the entity
                db_entity.relations.append(db_relation)

        # Commit changes to the database
        db.session.commit()

        # Retrieve entities and relations for rendering
        entities = Entity.query.all()

        # Prepare data for rendering
        render_data = []
        for entity in entities:
            render_entity = {"text": entity.text, "relations": []}
            for relation in entity.relations:
                render_entity["relations"].append(relation.relation_text)
            render_data.append(render_entity)

        return render_template('result.html', markup=markup, parse_results=parse_results, render_data=render_data)

@app.route('/database')
def database():
    # Retrieve entities and relations from the database
    entities = Entity.query.all()
    return render_template('database.html', entities=entities)


@app.route('/clear_database', methods=['POST'])
def clear_database():
    # Clear all data from the Entity and Relation tables
    Entity.query.delete()
    Relation.query.delete()
    db.session.commit()

    return redirect(url_for('database'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
