#encoding = utf-8

import math
from sys import argv
import os

import numpy as np
import pickle
import jieba

from utils import remove_punc
from timer import timer

# abs_path  = os.path.abspath('.')
# raise Exception(abs_path)

def count_frequency(corpus):

    dic = {}
    for sentence in corpus:
        for word in sentence:
            if word in dic:
                dic[word] += 1
            else:
                dic[word] = 1

    idx_to_word = []
    for k, v in dic.items():
        if v > 2:
            idx_to_word.append(k)

    word_freq = {k:0 for k in idx_to_word}
    for word in idx_to_word:
        for sentence in corpus:
            if word in sentence:
                word_freq[word] += 1

    return word_freq

def tf_idf(question, corpus, word_freq):

    tfidf_matrix = []


    question = remove_punc(question)

    jieba.load_userdict('./data/food.txt')
    jieba.load_userdict('./data/place.txt')
    jieba.load_userdict('./data/store.txt')
    jieba.load_userdict('./data/other.txt')

    question = list(jieba.cut(question))

    for sentence in corpus:

        tf = []
        idf = []
        for word in question:
            tf.append(sentence.count(word)/len(question))
            idf.append(math.log(float(len(corpus))/(word_freq.get(word, 0)+1)))

        tfidf_matrix.append(np.multiply(tf, idf))

    tfidf_matrix = np.array(tfidf_matrix)
    res = np.sum(tfidf_matrix, axis = 1)
    return res

def main():

    sentences = pickle.load(open('./data/cut_qa_combine.pkl', 'rb'))
    answer = pickle.load(open('./data/qa.pkl', 'rb'))

    try:
        word_freq = pickle.load(open('./data/word_freq.pkl', 'rb'))
    except FileNotFoundError:
        word_freq = count_frequency(sentences)
        pickle.dump(word_freq, open('./data/word_freq.pkl', 'wb'))


    q = '台南有什麼好吃的?' if len(argv) < 2 else argv[1]
    res = tf_idf(q, sentences, word_freq)
    idx = np.argmax(res)

    print(answer[idx][0], answer[idx][1])


def test():

    with timer('load cut_qa_combine.pkl'):
        sentences = pickle.load(open('./data/cut_qa_combine.pkl', 'rb'))

    with timer('load cut_question.pkl'):
        questions = pickle.load(open('./data/cut_question.pkl', 'rb'))

    with timer('load cut_answer.pkl'):
        answer = pickle.load(open('./data/cut_answer.pkl', 'rb'))

    with timer('calc word_freq'):
        word_freq = count_frequency(sentences)

    q = questions[100] if len(argv) < 2 else argv[1]

    with timer('final result'):
        print(q)
        res = tf_idf(q, sentences, word_freq)
        idx = np.argmax(res)
        print(idx, questions[idx], answer[idx])


if '__main__' == __name__:

    main()

