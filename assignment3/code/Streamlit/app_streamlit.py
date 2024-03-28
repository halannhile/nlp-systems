from collections import Counter
import networkx as nx
import graphviz
from PIL import Image

import streamlit as st
import pandas as pd
import altair as alt

import ner

example = ("Sebastian Tharun started working on selfdriving cars at Google in 2007. Sue did not.")

st.set_page_config(
    page_title='spaCy NER and Dependency Parsing',
    layout='wide')

# Sidebar
st.sidebar.title('Settings')
view_option = st.sidebar.radio('Select View', ['Entities', 'Dependencies'], index=0)

# Main content
st.title('spaCy Named Entity Recognition and Dependency Parsing')

text = st.text_area('Text to process', value=example, height=100)

doc = ner.SpacyDocument(text)

# Named Entity Recognition (NER)
entities = doc.get_entities()

# Dependency Parsing
parse_results = []
for sent in doc.doc.sents:
    sentence_text = sent.text
    parse_result = {"sentence_text": sentence_text, "dependency_parse": ""}
    for token in sent:
        parse_result["dependency_parse"] += f"{token.text} {token.dep_} {token.head.text}\n"
    parse_results.append(parse_result)

# Word Frequencies
counter = Counter(doc.get_tokens())
words = list(sorted(counter.most_common(30)))

# Data for Word Frequencies Chart
chart = pd.DataFrame({
    'frequency': [w[1] for w in words],
    'word': [w[0] for w in words]
})

# Display based on selected view
if view_option == 'Entities':
    # Entities view
    entity_tab = st.radio('Select Tab', ['Entities', 'Tokens'], index=0)
    if entity_tab == 'Entities':
        # Named Entity Recognition Table
        st.markdown(f'Total number of tokens: {len(doc.get_tokens())}<br/>'
                    f'Total number of types: {len(counter)}', unsafe_allow_html=True)
        st.markdown('### Named Entity Recognition Results:')
        st.table(entities)
    elif entity_tab == 'Tokens':
        # Word Frequencies Table
        st.markdown('### Word Frequencies:')
        bar_chart = alt.Chart(chart).mark_bar().encode(x='word', y='frequency')
        # Set width and height to adjust the size of the chart
        bar_chart = bar_chart.properties(width=800, height=400)
        st.altair_chart(bar_chart)
        st.table(chart)

elif view_option == 'Dependencies':
    # Dependencies view
    dependency_tab = st.radio('Select Tab', ['Table', 'Graph'], index=0)
    if dependency_tab == 'Table':
        # Table view
        st.subheader('Table View')
        for parse_result in parse_results:
            st.markdown(f"**Sentence:** {parse_result['sentence_text']}")
            table_data = []
            for token_info in parse_result['dependency_parse'].split('\n'):
                if token_info:
                    token, dep, head = token_info.split()
                    table_data.append({'Token': token, 'Dependency': dep, 'Head': head})
            st.table(pd.DataFrame(table_data))
    elif dependency_tab == 'Graph':
        # Graph view
        st.subheader('Graph View')

        # Overall graph for the entire text
        overall_graph = nx.DiGraph()
        for sent in doc.doc.sents:
            for token in sent:
                overall_graph.add_node(token.text)
                overall_graph.add_edge(token.head.text, token.text, label=token.dep_)

        overall_graph_chart = graphviz.Digraph(format='png')
        for node in overall_graph.nodes():
            overall_graph_chart.node(node)
        for edge in overall_graph.edges():
            overall_graph_chart.edge(edge[0],
                                     edge[1],
                                     label=overall_graph[edge[0]][edge[1]]['label'])

        overall_graph_path = "temp_overall_graph"
        overall_graph_chart.render(overall_graph_path, format='png', cleanup=True)
        overall_graph_image = Image.open(f"{overall_graph_path}.png")
        st.image(overall_graph_image)

        # Display graph for each sentence
        for sent_idx, sent in enumerate(doc.doc.sents):
            st.subheader(f'Graph for Sentence {sent_idx + 1}')
            st.markdown(f"**Sentence Text:** {sent.text}")
            sentence_graph = nx.DiGraph()
            for token in sent:
                sentence_graph.add_node(token.text)
                sentence_graph.add_edge(token.head.text, token.text, label=token.dep_)

            sentence_graph_chart = graphviz.Digraph(format='png')
            for node in sentence_graph.nodes():
                sentence_graph_chart.node(node)
            for edge in sentence_graph.edges():
                sentence_graph_chart.edge(edge[0],
                                          edge[1],
                                          label=sentence_graph[edge[0]][edge[1]]['label'])

            sentence_graph_path = f"temp_sentence_graph_{sent_idx + 1}"
            sentence_graph_chart.render(sentence_graph_path, format='png', cleanup=True)
            sentence_graph_image = Image.open(f"{sentence_graph_path}.png")
            st.image(sentence_graph_image)
