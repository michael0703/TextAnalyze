import jieba
import sys
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfVectorizer
from glob import glob
import os
import pandas as pd
import re
# import jpype
# from jpype import startJVM, JClass, getDefaultJVMPath






def ArticleSeg(reports):
	clean_reports = []
	for report in reports:
		proc_report, clean_report = [], []
		proc_report = [report[i].strip() for i in range(len(report))]
		proc_report = [proc_report[i].replace(" ", "") for i in range(len(proc_report))]
		for line in proc_report:
			line=line.replace("\n","")
			line=line.replace("-","")   
			line=line.replace("\u3000","") 
			line=line.replace("[","")
			line=line.replace("]","")
			line=re.sub(r'[A-Za-z]', "", line)
			line=re.sub(r'[：！;？｡＂§＃＄％ Ş＆＇±（）＊＋Ü，ß－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.。、。0123456789→@*^&()，.？,{}●►❖★=!/(=)…（）『』％%《》$「」∪･ω∪:?=<>"／♡˙︶.&#"_【】Ｉ~│|╱＿─－〉•〈➡＝◎�❤+]','',line)
			if line == "":
				continue
			clean_report.append(line)
			#         print(clean_report)
		clean_reports.append(clean_report)
	return clean_reports



def MakeWordMatrix(clean_report, word_matrix):
	for line in clean_report:
		seg_list = jieba.cut(line) 
		string_list = "|".join(seg_list).split('|')
		for s in string_list:
			if not (s in word_matrix.keys()):
				word_matrix[s] = 1
			else:
				word_matrix[s] += 1
	# return word_matrix


class NerService():

	def __init__(self):
		
		self.raw_reports = []
		self.clean_reports = []
		self.analyze_report = []
		self.NerDict = {}

		hanlp_lib_path = "./lib/"
		java_class_path = hanlp_lib_path + 'hanlp-1.7.0.jar' + ':' + hanlp_lib_path
		startJVM(getDefaultJVMPath(), '-Djava.class.path=' + java_class_path, '-Xms1g', '-Xmx1g')
		print(java_class_path)

	def Assign(self, raw_reports):

		self.raw_reports = raw_reports
		self.clean_reports = ArticleSeg(self.raw_reports)

	def NerAnalyze(self):

		if not jpype.isThreadAttachedToJVM():
			jpype.attachThreadToJVM()

		# PerceptronLexicalAnalyzer = JClass('com.hankcs.hanlp.model.perceptron.PerceptronLexicalAnalyzer')
		# analyzer=PerceptronLexicalAnalyzer() 	
		# TraditionalChineseTokenizer=SafeJClass('com.hankcs.hanlp.tokenizer.TraditionalChineseTokenizer')
		# HanLP = JClass('com.hankcs.hanlp.HanLP')
		# NLPTokenizer = jpype.JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')
		PerceptronLexicalAnalyzer = JClass('com.hankcs.hanlp.model.perceptron.PerceptronLexicalAnalyzer')
		analyzer = PerceptronLexicalAnalyzer()
		analyze_report = []
		for report in self.clean_reports:
			tmp_report = []
			for line in report:
				NerList = str(analyzer.analyze(line)).split()
				# print(NerList)
				for term in NerList:
					term = term.split('/')
					tmp_report.append((term[0], term[1]))

			analyze_report.append(tmp_report)
		self.analyze_report = analyze_report

	def MakeNerDict(self):

		NerDict = {}
		NerDict['Noun'] = []
		NerDict['Verb'] = []
		NerDict['adjective'] = []
		for analyze_report in self.analyze_report:
			for item in analyze_report:
				print(item[1])
				if item[1][0] == 'n':
					NerDict['Noun'].append(item[0])
				elif item[1][0] == 'v':
					NerDict['Verb'].append(item[0])
				elif item[1][0] == 'a':
					NerDict['adjective'].append(item[0])
		self.NerDict = NerDict



'''
def NerAnalyze(clean_reports):

	analyze_report = []
	TraditionalChineseTokenizer=SafeJClass('com.hankcs.hanlp.tokenizer.TraditionalChineseTokenizer')
	for report in reports:
		tmp_report = []
		for line in report:
			NerList = TraditionalChineseTokenizer.segment(line)
			for term in NerList:
				tmp_report.append((term.word, "{}".format(term.nature)))

		analyze_report.append(tmp_report)

	# print(analyze_report)
	return analyze_report
'''

'''
def MakeNerDictionary(analyze_report):
	NerDict = {}
	NerDict['Noun'] = [], NerDict['Verb'] = [], NerDict['adjective'] = []
	for item in analyze_report:
		if item[1][0] == 'n':
			NerDict['Noun'].append(item[0])
		elif item[1][0] == 'v':
			NerDict['Verb'].append(item[0])
		elif item[1][0] == 'a':
			NerDict['adjective'].append(item[0])
	return NerDict
'''






