#encoding = utf-8

import pickle
import re

import jieba
import numpy as np
from openpyxl import load_workbook

from utils import remove_punc

def load_txt(file_name):

    contents = []
    with open(f"./data/{file_name}", 'r') as file_p:
        contents = file_p.readlines()
        contents = list(map(lambda x: x.strip(), contents))
        contents = np.array(contents)
    return contents

def main():

    # load data
    wb = load_workbook('./data/QA_12543.xlsx')
    data = [[str(row[0].value), str(row[1].value)]for row in wb['工作表1'].rows]

    place = load_txt('place.txt')
    store = load_txt('store.txt')
    food = load_txt('food.txt')

    data_t = [[remove_punc(content[0]), remove_punc(content[1])] for content in data]

    print('loading')

    jieba.load_userdict('./data/dict_tw.txt')
    jieba.load_userdict('./data/food.txt')
    jieba.load_userdict('./data/place.txt')
    jieba.load_userdict('./data/store.txt')
    jieba.load_userdict('./data/other.txt')

    #transform data
    cut_q_res = []
    cut_a_res = []
    for QA in data_t:
        cut_q_res.append(list(jieba.cut(QA[0])))
        cut_a_res.append(list(jieba.cut(QA[1])))

    q_res, a_res = zip(*data)

    cut_qa_combine = np.array(cut_q_res) + np.array(cut_a_res)
    pickle.dump(data, open('./data/qa.pkl', 'wb'))
    pickle.dump(q_res, open('./data/question.pkl', 'wb'))
    pickle.dump(a_res, open('./data/answer.pkl', 'wb'))
    pickle.dump(cut_q_res, open('./data/cut_question.pkl', 'wb'))
    pickle.dump(cut_a_res, open('./data/cut_answer.pkl', 'wb'))
    pickle.dump(cut_qa_combine, open('./data/cut_qa_combine.pkl', 'wb'))

if '__main__' == __name__:

    main()
