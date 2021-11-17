# Code credit:
# https://towardsdatascience.com/understand-text-summarization-and-create-your-own-summarizer-in-python-b26a9f09fc70

import numpy as np
import networkx as nx
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance


def read_article(content):

    article = content.split(". ")
    sentences = []

    for sentence in article:
        # print(sentence)
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    sentences.pop()

    return sentences


def sentence_similarity(sent1, sent2, func_stopwords=None):
    if func_stopwords is None:
        func_stopwords = []

    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]

    all_words = list(set(sent1 + sent2))

    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)

    # build the vector for the first sentence
    for w in sent1:
        if w in func_stopwords:
            continue
        vector1[all_words.index(w)] += 1

    # build the vector for the second sentence
    for w in sent2:
        if w in func_stopwords:
            continue
        vector2[all_words.index(w)] += 1

    return 1 - cosine_distance(vector1, vector2)


def build_similarity_matrix(sentences, stop_words):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))

    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2:  # ignore if both are same sentences
                continue
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

    return similarity_matrix


def generate_summary(content, top_n=15):
    stop_words = stopwords.words('english')
    summarize_text = []

    # Step 1 - Read text anc split it
    sentences = read_article(content)

    # Step 2 - Generate Similary Martix across sentences
    sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)

    # Step 3 - Rank sentences in similarity martix
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph)

    # Step 4 - Sort the rank and pick top sentences
    ranked_sentence = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    # print("Indexes of top ranked_sentence order are ", ranked_sentence)

    for i in range(top_n):
        try:
            summarize_text.append(" ".join(ranked_sentence[i][1]))
        except IndexError:
            break

    # Step 5 - Offcourse, output the summarize text
    summarize_text = ". ".join(summarize_text)
    summarize_text = summarize_text.strip()

    return summarize_text


if __name__ == '__main__':
    wiki_summary = '''The English Wikipedia was the first Wikipedia edition and has remained the largest. It has pioneered many ideas as conventions, policies or features which were later adopted by Wikipedia editions in some of the other languages. These ideas include "featured articles",[7] the neutral-point-of-view policy,[8] navigation templates,[9] the sorting of short "stub" articles into sub-categories,[10] dispute resolution mechanisms such as mediation and arbitration,[11] and weekly collaborations.[12]'''
    x = generate_summary(wiki_summary, 20)
    print('x: ', len(x), x)
