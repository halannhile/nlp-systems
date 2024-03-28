from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
import en_core_web_sm
import ner


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class Entity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100))
    relations = db.relationship('Relation', backref='entity', lazy=True)


class Relation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    relation_text = db.Column(db.String(100))
    entity_id = db.Column(
        db.Integer,
        db.ForeignKey('entity.id'),
        nullable=False
        )


# Load the spaCy English model for dependency parsing
nlp = en_core_web_sm.load()


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

        # Parse entities from markup using BeautifulSoup
        soup = BeautifulSoup(markup, 'html.parser')
        entities = [entity.text for entity in soup.find_all('entity')]

        # Store entities in the database
        entities_dict = {}
        sub_entities = set()

        for entity in entities:
            if len(entity) > 1:
                entities_dict[entity] = {"relations": []}
                sub_entities.update(entity.split())

        # Dependency parsing
        doc = nlp(text)
        parse_results = []

        for sent in doc.sents:
            sentence_text = sent.text
            parse_result = {"sentence_text": sentence_text, "result": ""}

            for token in sent:
                if token.dep_ != 'punct':
                    relation_text = f"{token.text} {token.dep_} {token.head.text}"
                    head_entity_text = token.head.text
                    entity_text = token.text

                    matching_entity_heads = [
                        entity for entity in entities_dict
                        if head_entity_text in entity.split()]

                    if matching_entity_heads:
                        entity_key = matching_entity_heads[0]
                        relation_data = {"relation_text": relation_text}
                        entities_dict[entity_key]["relations"].append(relation_data)

                    matching_entities = [
                        entity for entity in entities_dict
                        if entity_text in entity.split()]

                    if matching_entities:
                        entity_key = matching_entities[0]
                        relation_data = {"relation_text": relation_text}
                        entities_dict[entity_key]["relations"].append(relation_data)

                    parse_result["result"] += f"{token.head.text} {token.dep_} {token.text}\n"

            parse_results.append(parse_result)

        # Store entities and relations in the database
        for entity_text, data in entities_dict.items():
            db_entity = Entity(text=entity_text)
            db.session.add(db_entity)

            for relation_data in data["relations"]:
                relation_text = relation_data["relation_text"]
                db_relation = Relation.query.filter_by(relation_text=relation_text).first()

                if not db_relation:
                    db_relation = Relation(relation_text=relation_text)

                db_entity.relations.append(db_relation)

        db.session.commit()

        # Retrieve entities and relations for rendering
        entities = Entity.query.all()
        render_data = []

        for entity in entities:
            render_entity = {"text": entity.text, "relations": []}
            for relation in entity.relations:
                render_entity["relations"].append(relation.relation_text)
            render_data.append(render_entity)

        return render_template('result.html',
                               markup=markup,
                               parse_results=parse_results,
                               render_data=render_data)


@app.route('/database')
def database():
    entities = Entity.query.all()
    return render_template('database.html', entities=entities)


@app.route('/clear_database', methods=['POST'])
def clear_database():
    Entity.query.delete()
    Relation.query.delete()
    db.session.commit()

    return redirect(url_for('database'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
