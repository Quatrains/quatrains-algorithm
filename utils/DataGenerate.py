# -*- coding:utf8 -*-
import re
import jieba
import jieba.analyse
from utils import *

def concatStr(s1, s2):
  if not s1 and not s2:
    return ''
  if not s1:
    return s2
  if not s2:
    return s1
  return s1 + s2

# def removePuncation(seg):
#   new_seg = []
#   puncation = '·*-;■囗〇－，。！？：；“”‘’、|（）〔〕【】《》「」『』\'[]\r\n\t'
#   for s in seg:
#     if s in puncation:
#       continue
#     new_seg.append(s)
#   return new_seg

def splitPoem(content):
  content = content.replace('\r\n', '')
  content = re.split(r'[。]', content)     
  return content[:-1]      

def generateData(poem_path, txt_path, json_path):
  poem_data = readJsonFile(poem_path)
  print('Poem num: %d' %len(poem_data))                  # 12081

  idx_keyword_dic = {}
  for i, poem in enumerate(poem_data):
    print(i)
    content_list = splitPoem(poem['content'])
    if len(content_list) > 20:
      continue
    sentences = concatStr(poem['background'], poem['translation']) + poem['content']
    if not sentences:
      continue
    s_cut = jieba.cut(sentences)
    s = ' '.join(s_cut)
    writeTXT(txt_path, s+'\n')
    
    key_words = jieba.analyse.extract_tags(sentences, topK=10)
    idx_keyword_dic[poem['idx']] = key_words
  writeJsonFile(json_path, idx_keyword_dic)  

def check(json_path):
  idx_keyword_dic = readJsonFile(json_path)
  print(len(idx_keyword_dic))
  for idx, keyword in idx_keyword_dic.items():
    print(idx, keyword)
    import pdb; pdb.set_trace()


if __name__ == '__main__':
  file_dir = '../poem_data/json/poems_4_alg.json'
  txt_dir = './data/poemCorpus_background+translation+content.txt'
  json_dir = './data/poemIdx_contentKeyWord_dic.json'
  generateData(file_dir, txt_dir, json_dir)
  # check(json_dir)
