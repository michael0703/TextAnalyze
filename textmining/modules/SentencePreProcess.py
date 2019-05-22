import re
import time
import io
import os
import json
import pandas as pd
import jieba
import jieba.analyse
from optparse import OptionParser
from pandas import DataFrame, read_csv
from nltk.tokenize import word_tokenize


# path='../data/'
# artpath = './'



# print(context)
class SentenceAnalyze():
	
	def __init__(self):

		# only for testing
		# init some data
		path='../data/'
		artpath = './'

		# build delete words 
		deletewordsraw = open("./textmining/jiebadict"+"/deletewords.txt", 'r', encoding='utf-8').read()
		self.deletewords=deletewordsraw.replace("\ufeff","").split()



	def CheckContainChinese(self, check_str):

		for c in check_str:
			if '\u4e00' <= c <= '\u9fa5':
				return True
		return False

	def RemoveSymbol(self, article_list):

		for idx, con in enumerate(article_list):
		    
		    #去除特殊符號
		    con=con.replace("\n","")
		    con=con.replace("-","")   
		    con=con.replace("\u3000","") 
		    con=con.replace("[","")
		    con=con.replace("]","")
		    con=con.replace("'","")
		    con = re.sub(r'[：0123456789→@*^&(),{}●►❖★=!/(=)…（）『』%《》$「」∪･ω∪:?=<>"／♡˙︶.&#"_【】Ｉ~│|╱＿─－〉•〈➡＝◎�❤+]','',con)
		    if self.CheckContainChinese(con):
		    	con = re.sub(r'[a-zA-Z]','',con)
		    	con = con.replace(" ","")
		    	con = re.sub(r'\W', '', con)	## 刪除全部標點符號

		    article_list[idx] = con

	def Cut_TC(self, content):

		#結巴斷詞
		# jieba.set_dictionary(path+"/dict.txt.big.txt")  
		# 增加自訂新詞 （補充前者之不足）
		# jieba.load_userdict(path+"userdict.txt")

		# 結巴分詞
		con = jieba.cut(content)  
		con = [w for w in con if w not in self.deletewords]

		return con

	def Cut_EN(self, content):

		return word_tokenize(content)

	def TextCut(self, article_list):

		
		# 刪除特殊符號
		self.RemoveSymbol(article_list)

		# 斷詞
		token = []
		for article in article_list:
			if self.CheckContainChinese(article):
				token.append(self.Cut_TC(article))
			else:
				token.append(self.Cut_EN(article))
		return token

if __name__ == '__main__':
	Alist = ['中美貿易戰遲遲談不攏，北美倒是率先有了新進展。\n川普宣布與墨西哥達成新協議，雙方同意徹底改革北美貿易協定(NAFTA)，究竟是否要加入的壓力跑到加拿大身上，同意新的汽車製造貿易條款以及解決爭端仍然是三國需要協議的。\n',
		'為什麼近年美國經濟成長強勁的情況下，通貨膨脹卻保持在相對低的水位呢？也許「亞馬遜效應」，也就是這類網路零售商，方便的比價及調整價格，甚至進而影響傳統零售商，打破了傳統的價格僵固性，零售商對其他因素變動的反應也更加靈敏。',
		"新北八年的故事，是一個「從邊陲成為主體」的故事。 過去的台北縣，即便坐擁豐沛的自然資源、遼闊的城鄉腹地，但在都會發展脈絡上，長期以來扮演台北市的附庸邊陲，也是許多中南部民眾北上求職求學，負擔不起台北房價時的暫居地帶\n\n\n\n。同樣是說住「台北」，一水之隔的縣區民眾總不免覺得矮人一截——政府資源比不上台北市、 街廓狹窄、公共設施匱乏，連縣區間的交通也往往需要先借道台北市。那時許多縣民的工作、就學、消費、休閒都要到台北；許多人也期盼，自己有能力時能搬到河的另一邊。",
		"「這個想法的實踐，要有良好的交通建設為基礎。」朱立倫提到。要有完善綿密的交通網絡，把台北縣原來分散的鄉鎮城區串聯起來，才能促成地區功能的分工整合，提升整個城市運作的效能。也因此，朱市長在競選之初\t，便以捷運「三環三線」為施政主軸\b，把若干興建中與研究規劃中的路線，串成簡單明瞭的圖象。",
		"Later that day, when the Princess was sitting at the table, something was heard coming up the marble stairs. Splish, splosh, splish splosh! The sound came nearer and nearer, and a voice cried, Let me in, youngest daughter of the King."
		]
	A = ["How much do you love avocados? Could you eat one, and only one, each and every day for six months straight? If you think you're up to the challenge, and have a little extra weight around your middle, researchers want to pay you $300 to participate in the Habitual Diet and Avocado Trial, or HAT as they're calling it.The research is being conducted at several universities in the United States, including Loma Linda University in California, University of California at Los Angeles, Tufts University in Massachusetts, Pennsylvania State University and Wake Forest University in North Carolina.Loma Linda University's website offers details about the incentives to participate in the study, including:$300 for successfully completing the studyOther small gifts over the six months Free avocados The results of some of your lab test work Lab results? Yes, the purpose of the study is to discover whether eating one avocado each day for six months has an impact on the amount and distribution of fat in the body. Out of the eight onsite clinics that participants will be required to attend, three of them will include the participants to have an MRI, have blood drawn, and have their bodies measured. Participants will also need to take a memory test at the beginning and the end of the study."]


	# 用法: 把字串 or 字串的list 丟進去Textcut()
	D = DataCut()
	print(D.TextCut(Alist))




