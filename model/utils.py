#encoding = utf-8

import string

#remove punctuation
def remove_punc(sentence, exclude = ''):
    """
    remove full/helf space and punctuation

    Arguments:
        sentence (string): the origin sentence to remove punctuation
        exclude (string): the charactor(s) not to be removed

    Returns:
        string: the final sentence

    Example:
        sentence = 'aabbb!@#%&$###@@'
        remove_punc(senctence, '#')
        >> 'aabbb####'
    """

    punctuation = '＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､\u3000、〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔·！？｡。'

    punc = string.punctuation + punctuation + " "
    for c in exclude:
        punc = punc.replace(i, '')
    table = str.maketrans('', '', punc)

    return sentence.translate(table)
