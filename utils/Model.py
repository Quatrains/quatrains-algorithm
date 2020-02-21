# -*- coding:utf8 -*-
import os
import re
import gensim
import jieba
from collections import defaultdict
from utils import *

# class MySentences(object):
#   def __init__(self, file_path):
#     self.file_path = file_path

#   def __iter__(self):
#     for line in open(self.file_path):
#       if line:
#         yield line.split()

def splitPoem(content):
  content = content.replace('\r\n', '')
  content = re.split(r'[，。！；？]', content)     
  return content[:-1]  

def poem_cut(poem):
  data = []
  sentences = poem.replace('\r\n', '').replace('\n', '')
  s_cut = jieba.cut(sentences)  
  for s in list(s_cut):
    if s == ' ' or s in data or s in '，。！；？':
      continue
    data.append(s)
  return data

def train(file_path, model_path):
  # sentences = MySentences(file_path) 
  print('training model...')
  sentences = gensim.models.word2vec.LineSentence(file_path) 
  model = gensim.models.Word2Vec(sentences, sg=1, hs=1, min_count=1,window=3,size=100)
  model.save(model_path)
  print(model.most_similar(['月']))

def loadModel(model_path):
  model = gensim.models.Word2Vec.load(model_path)
  print(type(model['月亮']))
  print(len(model['月亮']))  # 100
  print(model['月亮'])       # 100维的向量

class analizePoem(object):
  def __init__(self, model_dir, poem_dir, idx_keyword_dict_dir, file_save_path):
    self.model_dir = model_dir
    self.poem_dir = poem_dir
    self.idx_keyword_dict_dir = idx_keyword_dict_dir
    self.file_save_path = file_save_path
    self.data = {}

  def loadModel(self):
    print('loading model...')
    self.model = gensim.models.Word2Vec.load(self.model_dir)
  
  def loadPoemData(self):
    print('loading poem data...')
    self.poem_data = readJsonFile(self.poem_dir)
    self.idx_keyword_dict = readJsonFile(self.idx_keyword_dict_dir)

  def calculateSimilarity(self):
    print('calculating similarity...')
    idx_mostsimiliar_dict = {}
    for idx, keyword in self.idx_keyword_dict.items():
      print('similarity, idx: ', idx)
      idx_similarity_dic = {}
      for idx2, keyword2 in self.idx_keyword_dict.items():
        if idx == idx2 or not (keyword and keyword2):
          continue
        similarity = self.model.n_similarity(keyword, keyword2)
        idx_similarity_dic[idx2] = similarity
      idx_similarity_list = sorted(idx_similarity_dic.items(), key=lambda item:item[1], reverse=True)  
      idx_mostsimiliar_dict[int(idx)] = [int(item[0]) for item in idx_similarity_list[:10]]
    self.data['similarity'] = idx_mostsimiliar_dict

  def calculatePopularity(self):
    print('calculating popularity...')
    idx_likescount_dict = {}
    for i, poem in enumerate(self.poem_data):
      print('popularity, idx: ', i)
      content_list = splitPoem(poem['content'])
      if len(content_list) > 20:
        continue
      idx_likescount_dict[poem['idx']] = poem['likesCount']
    idx_likescount_list = sorted(idx_likescount_dict.items(), key=lambda item:item[1], reverse=True)
    self.data['popularity'] = [item[0] for item in idx_likescount_list[:300]]  # 存排名前300的试

  def classifyType(self):
    print('classify poem by type...')
    type_idx_dict = defaultdict(list)
    for i, poem in enumerate(self.poem_data):
      print('type, idx: ', i)
      content_list = splitPoem(poem['content'])
      if len(content_list) > 20:
        continue
      for _type in poem['interest']:
        type_idx_dict[_type].append(poem['idx'])
    self.data['type'] = type_idx_dict 

  def saveData(self):
    print('writing data...')
    writeJsonFile(self.file_save_path, self.data)

  def execute(self):
    self.loadModel()
    self.loadPoemData()
    self.calculateSimilarity()
    self.calculatePopularity()
    self.classifyType()
    self.saveData()

if __name__ == '__main__':
  corpus_path = './data/poemCorpus_background+translation+content.txt'
  poem_path = '../poem_data/json/poems_4_alg.json'
  model_path = './model/model_background+translation+content'
  idx_keyword_dict_path = './data/poemIdx_contentKeyWord_dic.json'
  data_save_path = './data/dict_SimilariyPopularityType.json'
  
  # train(corpus_path, model_path)
  # loadModel(model_path)
  s = analizePoem(model_path, poem_path, idx_keyword_dict_path, data_save_path)
  s.execute()


