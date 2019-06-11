#! /usr/bin/env python3
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
    #word freq
    for sentence in corpus:
        for word in sentence:
            if word in dic:
                dic[word] += 1
            else:
                dic[word] = 1

    for k, v in dic.items():
        if v < 3:
            continue
        word_freq[k] = 0
        for sentence in corpus:
            if k in sentence:
                word_freq[k] += 1

    #df
    word_freq = {k:0 for k in idx_to_word}
    for word in idx_to_word:
        for sentence in corpus:
            if word in sentence:
                word_freq[word] += 1

    return word_freq

def tf_idf(question, corpus, word_freq):

    res = []

    question = remove_punc(question)

    jieba.load_userdict('./data/food.txt')
    jieba.load_userdict('./data/place.txt')
    jieba.load_userdict('./data/store.txt')
    jieba.load_userdict('./data/other.txt')

    question = list(jieba.cut(question))

    len_q = float(len(question))
    N = float(len(corpus))
    for sentence in corpus:
        sum_val = 0
        for word in question:
            sum_val += (sentence.count(word)/len_q) * math.log(N/(word_freq.get(word, 0)+1))

        res.append(sum_val)

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


if '__main__' == __name__:

    main()

