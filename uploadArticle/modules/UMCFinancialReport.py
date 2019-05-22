
# coding: utf-8

# In[1]:



# import package 
#-*- coding:utf-8 -*-
import jieba
import sys
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfVectorizer
from glob import glob
import os
import pandas as pd
import re


# In[2]:


# file_list = glob('./finacialreports/*.txt')
# print(file_list)


# In[3]:


# t 為儲存每一篇文章的list， ttolines為儲存文章中每一句話的list
reports = []
for file in file_list:
    with open(file ,'r', encoding = 'utf-8') as f:
        report = []
        for line in f:
            report.append(line)
    reports.append(report)
# print(reports[0])


# In[4]:


def ProcReport(reports):
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
    return word_matrix


# In[5]:


clean_reports = ProcReport(reports)
# print(clean_reports[2])


# In[6]:


Report_Word_Matrix={}
df = None
for i in range(len(clean_reports)):
    tmp_matrix = {}
    MakeWordMatrix(clean_reports[i], tmp_matrix)
    tmp_df = pd.DataFrame(tmp_matrix, index=[0])
    df = pd.concat([df,tmp_df],ignore_index=True)
df = df.fillna(0)
df


# In[7]:



#對標點符號以外詞組做TF-IDF
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer 
transformer = TfidfTransformer()  
tfidf = transformer.fit_transform(df.values)
# print(type(tfidf))
df_tfidf = pd.DataFrame(tfidf.toarray(), columns = df.columns.tolist(), index=[filenm.split('/')[2] for filenm in file_list])


# In[203]:


#把斷詞從矩陣中刪掉
deletewordsraw = open("./deletewords.txt", 'r', encoding='utf-8').read()
deletewords=deletewordsraw.replace("\ufeff","").split()


df_tfidf = df_tfidf[df_tfidf>0.005].dropna(axis=1)

# type(df_tfidf)
# df_tfidf>0.03
for label in range(len(df_tfidf.columns)):
    if label in deletewords:
#         print(label)
        df_tfidf = df_tfidf[label].drop(axis=1)
df_tfidf


# In[204]:


#再觀察一次文字雲並手動刪除不適合的資訊
from wordcloud import WordCloud
import matplotlib.pyplot as plt
tfidf_dict = df_tfidf.to_dict('records')
# print(tfidf_dict)
wordcloud = WordCloud(font_path = '../../week_4/simfang.ttf', background_color="white",width=1000, height=860, margin=2)


# In[205]:


remove_list = ['年月日','之','及','。','於','或'
               ,'與','係','本','為','一','合','公司','民國','年度','月','日','註','其他','年','應','資產',
               '有限公司' , '董事', '千元', '損益', '金融', '財務', '以', '的', '無', '無以'
                , '動', '九', '投資', '季', '單位', '每股', '子公司', 'o', 'O', '0','臺', '台', '聯華電子', '']

for i in range(len(tfidf_dict)):
    for item in remove_list:
        tfidf_dict[i].pop(item, None)
    for item in deletewords:
        tfidf_dict[i].pop(item, None)
wordcloud = WordCloud(font_path = '../../week_4/simfang.ttf', background_color="white",width=1000, height=860, margin=2, max_words=100)

for i in range(len(file_list)):
    wordcloud.fit_words(tfidf_dict[i])
    plt.imshow(wordcloud)
    plt.show()


# In[206]:


# print(type(tfidf_dict), type(df_tfidf))
# print(df_tfidf.shape)


# In[211]:


#### df_tfidf.T.to_csv('聯電2010-2011.csv', index=file_list)


# In[212]:


#### df_tfidf

