#!/usr/bin/python
# -*- coding: utf8 -*-
from collections import Counter
import re
import numpy as np
import networkx as nx
import nltk.stem 

class _graphStatistics():
	
	def __init__(self,graph): 
		self.graph= graph
	
	def statistics(self):
		res ={}
		graph = self.graph
		res['number_of_nodes'] = graph.number_of_nodes()
		res['number_of_edges'] = graph.number_of_edges()
		res['PE'] =  (np.array(list(Counter(graph.edges()).itervalues()))>1).sum()
		res['LCC'] =  nx.algorithms.components.number_weakly_connected_components(graph)
		res['LSC'] =  nx.algorithms.components.number_strongly_connected_components(graph)
		
		degrees = list(graph.degree().itervalues())
		res['degree_average'] =  np.mean(degrees)
		res['degree_std'] =  np.std(degrees)
		
		
		adj_matrix = nx.linalg.adj_matrix(graph).toarray()
		adj_matrix2 = np.dot( adj_matrix , adj_matrix)
		adj_matrix3 = np.dot( adj_matrix2 , adj_matrix)
		
		res['L1'] =  np.trace(adj_matrix)
		res['L2'] =  np.trace(adj_matrix2)
		res['L3'] =  np.trace(adj_matrix3)
		
		return res

		
class naiveGraph():
	def __init__(self): pass
	
	def _text2graph(self, text, word_tokenizer=lambda x: x.split(" ") ): 
		cleaned_text= re.sub("[^\w ]+"," ",text.lower().strip())
		words = [w for w in word_tokenizer(cleaned_text) if len(w)>0]
		gr = nx.MultiDiGraph()
		gr.add_edges_from( zip(words[:-1], words[1:]))
		return gr
		
	def analyzeText(self, text):
		dgr = self._text2graph(text)
		return _graphStatistics(dgr).statistics()

class stemGraph():
	
	def __init__(self): pass
	
	def _text2graph(self, text, word_tokenizer=lambda x: x.split(" ")  , stemmer =  lambda x: nltk.stem.snowball.EnglishStemmer().stem(x)):
		cleaned_text= re.sub("[^\w ]+"," ",text.lower().strip())
		words = [w for w in word_tokenizer(cleaned_text) if len(w)>0]
		stemmead_words=[stemmer(w) for w in words]
		gr = nx.MultiDiGraph()
		gr.add_edges_from( zip(stemmead_words[:-1], stemmead_words[1:]))
		return gr
		
	def analyzeText(self, text):
		dgr = self._text2graph(text)
		return _graphStatistics(dgr).statistics()
		
class posGraph():
	
	def __init__(self): pass
	
	def _text2graph(self, text, word_tokenizer=lambda x: x.split(" ")  , sentence_tokenizer=lambda x: x.split(".") , stemmer =  lambda x: nltk.stem.snowball.EnglishStemmer().stem(x)):
		sentences= sentence_tokenizer(text)
		tags= []
		for s in sentences:
			cleaned_text= re.sub("[^\w ]+"," ",s.lower().strip())
			tags+=list(zip(*nltk.pos_tag(word_tokenizer(cleaned_text)))[1])
		gr = nx.MultiDiGraph()
		gr.add_edges_from( zip(tags[:-1], tags[1:]))
		return gr
		
	def analyzeText(self, text):
		dgr = self._text2graph(text)
		return _graphStatistics(dgr).statistics()
		
		
