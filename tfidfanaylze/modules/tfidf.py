import jieba
import sys
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfVectorizer
from glob import glob
import os
import pandas as pd
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer 
from sklearn.decomposition import PCA
 

def ConcatWordMatrix(tmp_matrix, word_matrix_dataframe):
	tmp_df = pd.DataFrame(tmp_matrix, index=[0])
	# print(tmp_df)
	word_matrix_dataframe = pd.concat([word_matrix_dataframe,tmp_df],ignore_index=True, sort=False)
	return word_matrix_dataframe

def DoTFIDF(df, file_list):
	transformer = TfidfTransformer()  
	tfidf = transformer.fit_transform(df.values)
	# print(type(tfidf))
	df_tfidf = pd.DataFrame(tfidf.toarray(), columns = df.columns.tolist(), index=[filenm for filenm in file_list])
	return df_tfidf

def DoPCA(df):
	pca=PCA(n_components=2)
	pca_data = pca.fit_transform(df.T.values)
	return pca_data